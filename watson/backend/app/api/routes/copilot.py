"""Copiloto global do associado, independente de uma compra selecionada."""
from __future__ import annotations

import json
import logging
import re

from fastapi import APIRouter

from app.api.deps import AssociadoUser
from app.api.errors import ApiError
from app.api.schemas.copilot import CopilotReplyResponse, CopilotRequest, CopilotStatusResponse
from app.db.session import get_engine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/copilot", tags=["copilot"])
_HTML_RE = re.compile(r"<[^>]+>")


def _normalize_copilot_content(raw: str) -> str:
    """Extrai texto útil e remove delimitadores estruturais vazados pelo modelo."""
    content = raw.strip()

    # Alguns modelos devolvem um envelope JSON mesmo quando a saída esperada é
    # texto. Aceitamos os nomes mais comuns sem expor o envelope na interface.
    candidate = content
    if candidate.startswith("```json") and candidate.endswith("```"):
        candidate = candidate[7:-3].strip()
    if candidate.startswith("{"):
        try:
            payload = json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            payload = None
        if isinstance(payload, dict):
            for key in ("content", "message", "reply", "response"):
                if isinstance(payload.get(key), str):
                    content = payload[key].strip()
                    break

    # Evita artefatos como "]}" no fim de uma resposta Markdown. Só remove
    # fechamentos realmente desbalanceados, preservando pontuação legítima.
    for opening, closing in (("{", "}"), ("[", "]")):
        while content.endswith(closing) and content.count(closing) > content.count(opening):
            content = content[:-1].rstrip()

    return content


def _configured() -> bool:
    from app.config import get_settings
    return bool(get_settings().groq_api_key)


@router.get("", response_model=CopilotStatusResponse)
def get_copilot_status(persona: AssociadoUser) -> CopilotStatusResponse:
    first_name = persona.display_name.split(" ")[0]
    return CopilotStatusResponse(
        greeting=(
            f"Olá, {first_name}. Sou seu copiloto para acompanhar compras, consultar status, "
            "montar um resumo e pedir revisão quando você precisar."
        ),
        capabilities=[
            "Pesquisar suas compras",
            "Explicar uma transação",
            "Gerar resumo da conta",
            "Solicitar revisão humana",
        ],
        agent_available=_configured(),
        simulation=True,
    )


@router.post("/chat", response_model=CopilotReplyResponse)
def post_copilot_chat(
    body: CopilotRequest,
    persona: AssociadoUser,
) -> CopilotReplyResponse:
    if _HTML_RE.search(body.message):
        raise ApiError(400, "INVALID_REQUEST", "A mensagem não pode conter HTML.")
    if not _configured():
        raise ApiError(
            503,
            "AGENT_UNAVAILABLE",
            "O copiloto está indisponível agora. As compras e os botões da tela continuam funcionando.",
        )

    from app.domain.copilot import CopilotDeps, copilot_agent

    tools_used: list[str] = []
    try:
        result = copilot_agent.run_sync(
            body.message,
            deps=CopilotDeps(customer_id=persona.customer_id, db=get_engine()),
            timeout=30.0,
        )
        for message in result.all_messages():
            for part in getattr(message, "parts", []):
                if getattr(part, "part_kind", None) == "tool-call":
                    tool_name = getattr(part, "tool_name", None)
                    if tool_name and tool_name not in tools_used:
                        tools_used.append(tool_name)
    except Exception as exc:
        logger.warning("Copiloto indisponível: %s", exc)
        raise ApiError(
            503,
            "AGENT_UNAVAILABLE",
            "O copiloto está indisponível agora. Tente novamente em alguns instantes.",
        ) from exc

    return CopilotReplyResponse(
        content=_normalize_copilot_content(result.output),
        tools_used=tools_used,
        action_taken="solicitar_revisao" in tools_used,
        simulation=True,
    )
