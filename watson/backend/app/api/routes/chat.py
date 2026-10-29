"""Endpoints de chat (§7 e §10 do contrato).

GET  /api/purchases/{case_id}/chat  — histórico da conversa
POST /api/purchases/{case_id}/chat  — envia mensagem ao agente
"""
from __future__ import annotations

import logging
import math
import re

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import AssociadoUser
from app.api.errors import ApiError
from app.api.schemas.chat import (
    ChatHistoryResponse,
    ChatMessageOut,
    ChatPostResponse,
    ChatRequest,
    ChatReplyMessageOut,
    ChatUserMessageOut,
)
from app.db.repositories.chat import ChatRepository
from app.db.repositories.purchases import PurchaseRepository
from app.db.session import get_session

logger = logging.getLogger(__name__)

# Regex para HTML mínimo — rejeita qualquer tag HTML
_HTML_RE = re.compile(r"<[^>]+>")

# Saudação inicial (§7 do contrato — exemplo da spec)
_GREETING_TEMPLATE = (
    "Olá, {name}. Posso explicar por que pedimos sua confirmação ou tirar dúvidas sobre "
    "esta compra. Para autorizar ou recusar, use os botões da tela."
)

router = APIRouter(tags=["chat"])

_SAFE_SCORE_MSG = (
    "Não posso fornecer o score desta compra. "
    "Para dúvidas, use os botões da tela ou peça uma revisão."
)


def _scrub_score(text: str, score: float | None) -> str:
    """Remove o valor numérico do score da resposta do LLM.

    Se o score gravado aparecer na resposta (ex.: por injeção de prompt),
    substitui toda a resposta por uma mensagem segura e registra aviso.
    Verifica o valor com até 4 casas decimais e representações percentuais.
    """
    if score is None:
        return text

    # Gera padrões a verificar: "0.9917", "99.17", "99%", "99,17%", etc.
    patterns = set()
    # Valor direto com até 4 casas
    patterns.add(f"{score:.4f}")
    patterns.add(f"{score:.3f}")
    patterns.add(f"{score:.2f}")
    # Como percentual
    pct = score * 100
    patterns.add(f"{pct:.2f}")
    patterns.add(f"{pct:.1f}")
    patterns.add(f"{math.floor(pct)}%")
    patterns.add(f"{round(pct)}%")

    for pat in patterns:
        if pat in text:
            logger.warning(
                "Resposta do LLM continha o valor do score (%s) — substituída por mensagem segura.", pat
            )
            return _SAFE_SCORE_MSG

    return text


def _is_agent_configured() -> bool:
    """Verifica se há GROQ_API_KEY configurada."""
    from app.config import get_settings
    s = get_settings()
    return bool(s.groq_api_key)


def _get_open_review_protocol(purchase) -> str | None:
    for rev in purchase.reviews:
        if rev.status == "ABERTA":
            return rev.protocol
    return None


# ---------------------------------------------------------------------------
# GET /api/purchases/{case_id}/chat
# ---------------------------------------------------------------------------

@router.get("/api/purchases/{case_id}/chat", response_model=ChatHistoryResponse)
def get_chat(
    case_id: str,
    persona: AssociadoUser,
    session: Session = Depends(get_session),
) -> ChatHistoryResponse:
    """Histórico da conversa da compra (R10: reabre no mesmo ponto)."""
    repo = PurchaseRepository(session)
    result = repo.get_by_owner(persona.customer_id, case_id)
    if result is None:
        raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")
    purchase, _ = result

    chat_repo = ChatRepository(session)
    messages = chat_repo.list_messages(purchase)

    # Se não há mensagens, grava a saudação do assistente
    if not messages:
        display_name = persona.display_name.split(" (")[0]  # "Ana Souza"
        greeting = _GREETING_TEMPLATE.format(name=display_name)
        greeting_msg = chat_repo.save_message(
            purchase=purchase,
            role="assistant",
            content=greeting,
            tools_used=[],
        )
        session.commit()
        session.refresh(greeting_msg)
        messages = [greeting_msg]

    out_messages = [
        ChatMessageOut(
            message_id=m.message_id,
            role=m.role,
            content=m.content,
            created_at=m.created_at,
            tools_used=m.tools_used_json or [],
        )
        for m in messages
    ]

    return ChatHistoryResponse(
        case_id=case_id,
        messages=out_messages,
        agent_available=_is_agent_configured(),
        simulation=True,
    )


# ---------------------------------------------------------------------------
# POST /api/purchases/{case_id}/chat
# ---------------------------------------------------------------------------

@router.post("/api/purchases/{case_id}/chat", response_model=ChatPostResponse)
def post_chat(
    case_id: str,
    body: ChatRequest,
    persona: AssociadoUser,
    session: Session = Depends(get_session),
) -> ChatPostResponse:
    """Envia mensagem ao agente. 503 se LLM indisponível; 429 se rate-limit atingido."""
    from app.config import get_settings
    settings = get_settings()

    # Valida HTML
    if _HTML_RE.search(body.message):
        raise ApiError(400, "INVALID_REQUEST", "A mensagem não pode conter HTML.")

    repo = PurchaseRepository(session)
    result = repo.get_by_owner(persona.customer_id, case_id)
    if result is None:
        raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")
    purchase, _ = result

    chat_repo = ChatRepository(session)

    # Rate-limit: 20 mensagens por compra em 10 min (§7)
    recent = chat_repo.count_recent(purchase, window_seconds=settings.chat_rate_limit_window_seconds)
    if recent >= settings.chat_rate_limit_messages:
        raise ApiError(
            429,
            "RATE_LIMITED",
            "Você enviou muitas mensagens. Aguarde alguns minutos antes de tentar novamente.",
            {"retry_after_seconds": settings.chat_rate_limit_window_seconds},
        )

    # Salva a mensagem do usuário (sempre, mesmo se o LLM falhar)
    user_msg = chat_repo.save_message(
        purchase=purchase,
        role="user",
        content=body.message,
    )
    session.commit()
    session.refresh(user_msg)

    # Se o agente não está configurado → 503
    if not _is_agent_configured():
        raise ApiError(
            503,
            "AGENT_UNAVAILABLE",
            "O assistente está indisponível agora. Você ainda pode responder à compra pelos botões ou pedir revisão.",
            {"retry_after_seconds": 30},
        )

    # Chama o agente
    tools_used: list[str] = []
    reply_content: str
    try:
        from app.domain.agent import chat_agent, AgentDeps
        deps = AgentDeps(
            customer_id=persona.customer_id,
            case_id=case_id,
            db=session,
        )
        result_run = chat_agent.run_sync(
            body.message,
            deps=deps,
            timeout=30.0,
        )
        reply_content = result_run.output

        # Segunda camada de segurança: se o LLM escreveu o valor do score
        # na resposta (injeção de prompt), substitui por mensagem segura.
        reply_content = _scrub_score(reply_content, purchase.analysis_score)

        # Coleta tools_used a partir das mensagens do resultado
        for msg in result_run.all_messages():
            for part in getattr(msg, "parts", []):
                kind = getattr(part, "part_kind", None)
                if kind == "tool-call":
                    tool_name = getattr(part, "tool_name", None)
                    if tool_name and tool_name not in tools_used:
                        tools_used.append(tool_name)

    except Exception as exc:
        logger.warning("Agente indisponível: %s", exc)
        raise ApiError(
            503,
            "AGENT_UNAVAILABLE",
            "O assistente está indisponível agora. Você ainda pode responder à compra pelos botões ou pedir revisão.",
            {"retry_after_seconds": 30},
        ) from exc

    # Salva a resposta do assistente
    assistant_msg = chat_repo.save_message(
        purchase=purchase,
        role="assistant",
        content=reply_content,
        tools_used=tools_used,
    )
    session.commit()
    session.refresh(assistant_msg)

    # Verifica se o agente criou uma revisão nesta rodada
    session.refresh(purchase)
    review_protocol = _get_open_review_protocol(purchase)

    return ChatPostResponse(
        case_id=case_id,
        user_message=ChatUserMessageOut(
            message_id=user_msg.message_id,
            role=user_msg.role,
            content=user_msg.content,
            created_at=user_msg.created_at,
        ),
        reply=ChatReplyMessageOut(
            message_id=assistant_msg.message_id,
            role=assistant_msg.role,
            content=assistant_msg.content,
            created_at=assistant_msg.created_at,
            tools_used=tools_used,
        ),
        review_protocol=review_protocol,
        simulation=True,
    )
