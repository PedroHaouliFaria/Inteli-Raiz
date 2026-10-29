"""Agente de chat Pydantic AI (§7 e §10 do contrato).

O agente recebe customer_id e case_id por injeção de dependência (RunContext.deps),
nunca por texto do LLM. Isso impede que um prompt peça a compra de outra pessoa (R05, R09).

Ferramentas (sem argumentos de identidade):
  consultar_compra()    — purchase + alert do §5
  consultar_status()    — corpo do GET .../status
  avaliar_transacao()   — análise gravada (score do modelo)
  solicitar_revisao(reason, details) — POST .../review com created_by=AGENTE
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from pydantic_ai import Agent, RunContext

logger = logging.getLogger(__name__)

# Instruções fixas do §10 do contrato
_SYSTEM_PROMPT = """\
Você é um assistente do Sicredi que ajuda associados a entender compras marcadas para confirmação.

Regras fixas — nunca quebre nenhuma delas:
1. Não pressione o associado a autorizar ou a recusar. Só os botões da tela fazem isso.
2. Não peça senha, PIN, número completo do cartão nem dado pessoal.
3. Não invente o nome do estabelecimento; diga que a base só tem a categoria do MCC.
4. Não cite o score do modelo como porcentagem de fraude: ele é um indicador de ranqueamento, não probabilidade calibrada.
5. Não afirme que um sinal causou a avaliação; os sinais são características da compra, não determinantes isolados.
6. Somente os botões "Reconheço e autorizo", "Não reconheço" e "Estou em dúvida" autorizam ou recusam a compra.
7. Se o associado pedir para você autorizar, recusar ou qualquer ação que mude o estado da compra, explique que só os botões fazem isso.
8. Responda sempre em português do Brasil.
9. Esta conversa é sobre uma única compra — a que está nesta tela. Se pedirem outra compra, outro código (como T-011) ou dados de outra pessoa, diga que só pode falar desta compra e não exiba nada como se fosse a outra.
10. Nunca informe o valor do score ao associado, nem ofereça informar. O score serve apenas para análise interna.
11. Antes de responder qualquer coisa sobre a compra (estabelecimento, valor, data, motivo do alerta), chame consultar_compra. Para prazo e situação, chame consultar_status.
12. Mencione os motivos pelos rótulos (ex.: "compra sem presença física do cartão"), nunca pelos códigos internos (nada de CARTAO_NAO_PRESENTE na resposta).
13. A tela tem apenas os três botões e este chat. Não invente botões, menus ou passos adicionais (ex.: "Solicitar revisão", "selecionar o motivo"). Se o associado quiser revisão humana, ofereça solicitar por ele e use a ferramenta solicitar_revisao.
14. Você já sabe qual é a compra: nunca peça ao associado data, valor ou estabelecimento para identificá-la.
15. Respostas curtas: no máximo 5 frases, sem tabelas.
"""


@dataclass
class AgentDeps:
    customer_id: str   # da sessão — nunca do LLM
    case_id: str       # da URL do chat, já conferida contra o customer_id
    db: Any            # Session do SQLAlchemy


def _make_agent() -> Agent[AgentDeps, str]:
    """Cria o agente com as quatro ferramentas. Modelo configurável via settings."""
    from app.config import get_settings
    settings = get_settings()

    # Se não há GROQ_API_KEY, o agente fica sem modelo configurado.
    # A rota de chat detecta isso e retorna 503 AGENT_UNAVAILABLE.
    model_str = settings.llm_model if settings.groq_api_key else None

    agent: Agent[AgentDeps, str] = Agent(
        model=model_str,
        deps_type=AgentDeps,
        system_prompt=_SYSTEM_PROMPT,
        defer_model_check=True,
    )

    # -----------------------------------------------------------------------
    # Ferramenta 1: consultar_compra
    # -----------------------------------------------------------------------
    @agent.tool
    async def consultar_compra(ctx: RunContext[AgentDeps]) -> dict:
        """Retorna os dados da compra (purchase e alert) para que o assistente explique a situação."""
        from sqlalchemy.orm import Session
        from app.db.repositories.purchases import PurchaseRepository
        from app.domain.cases.purchases import build_purchase_detail

        session: Session = ctx.deps.db
        repo = PurchaseRepository(session)
        result = repo.get_by_owner(ctx.deps.customer_id, ctx.deps.case_id)
        if result is None:
            return {"error": "Compra não encontrada."}
        purchase, confirmation = result
        detail = build_purchase_detail(purchase, confirmation, session=session)
        # Retorna apenas purchase e alert — sem score
        return {"purchase": detail["purchase"], "alert": detail["alert"]}

    # -----------------------------------------------------------------------
    # Ferramenta 2: consultar_status
    # -----------------------------------------------------------------------
    @agent.tool
    async def consultar_status(ctx: RunContext[AgentDeps]) -> dict:
        """Retorna o status atual da compra para que o assistente informe o associado."""
        from sqlalchemy.orm import Session
        from app.db.repositories.purchases import PurchaseRepository
        from app.domain.cases.purchases import build_purchase_status

        session: Session = ctx.deps.db
        repo = PurchaseRepository(session)
        result = repo.get_by_owner(ctx.deps.customer_id, ctx.deps.case_id)
        if result is None:
            return {"error": "Compra não encontrada."}
        purchase, confirmation = result
        return build_purchase_status(purchase, confirmation, session=session)

    # -----------------------------------------------------------------------
    # Ferramenta 3: avaliar_transacao
    # -----------------------------------------------------------------------
    @agent.tool
    async def avaliar_transacao(ctx: RunContext[AgentDeps]) -> dict:
        """Retorna a análise do modelo de risco gravada para esta compra.

        ATENÇÃO: o score é um indicador de ranqueamento, não probabilidade de fraude.
        Não cite o score como porcentagem.
        """
        from sqlalchemy.orm import Session
        from sqlalchemy import select
        from app.db.tables.purchases import Purchase
        from app.domain.signals.rules import compute_signals

        session: Session = ctx.deps.db
        stmt = (
            select(Purchase)
            .where(
                Purchase.case_id == ctx.deps.case_id,
                Purchase.customer_id == ctx.deps.customer_id,
            )
        )
        purchase = session.execute(stmt).scalar_one_or_none()
        if purchase is None:
            return {"error": "Compra não encontrada."}

        # Determina o analysis_id: A-<n>-v1
        n = ctx.deps.case_id.replace("T-", "") if ctx.deps.case_id.startswith("T-") else ctx.deps.case_id
        analysis_id = f"A-{n}-v1"

        signals = []
        if purchase.features_json:
            try:
                computed = compute_signals(purchase.features_json)
                signals = [{"code": s.code, "label": s.label, "source": s.source} for s in computed]
            except Exception:
                pass

        evaluated_at = None
        if purchase.analysis_evaluated_at:
            from datetime import timezone
            dt = purchase.analysis_evaluated_at
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            evaluated_at = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        return {
            "analysis_id": analysis_id,
            "score": purchase.analysis_score,
            "score_source": purchase.analysis_score_source,
            "model_version": purchase.analysis_model_version,
            "decision": purchase.analysis_decision,
            "policy_version": purchase.analysis_policy_version,
            "signals": signals,
            "gaps": purchase.analysis_gaps_json or [],
            "evaluated_at": evaluated_at,
            "note": "Score de ranqueamento, não probabilidade calibrada. Não citar como porcentagem de fraude.",
        }

    # -----------------------------------------------------------------------
    # Ferramenta 4: solicitar_revisao
    # -----------------------------------------------------------------------
    @agent.tool
    async def solicitar_revisao(
        ctx: RunContext[AgentDeps],
        reason: str,
        details: str = "",
    ) -> dict:
        """Solicita revisão humana da compra.

        reason deve ser um de: NAO_RECONHECE_ESTABELECIMENTO, VALOR_DIFERENTE,
        DUVIDA_PROCESSO, OUTRO.
        Não muda o status da compra — o associado ainda pode responder pelos botões.
        """
        from sqlalchemy.orm import Session
        from app.db.repositories.purchases import PurchaseRepository
        from app.domain.reviews import create_or_get_review

        session: Session = ctx.deps.db
        repo = PurchaseRepository(session)
        result = repo.get_by_owner(ctx.deps.customer_id, ctx.deps.case_id)
        if result is None:
            return {"error": "Compra não encontrada."}
        purchase, _ = result

        # Normaliza reason: valores inválidos viram OUTRO (o LLM pode mandar valores fora do enum)
        _valid_reasons = {"NAO_RECONHECE_ESTABELECIMENTO", "VALOR_DIFERENTE", "DUVIDA_PROCESSO", "OUTRO"}
        normalized_reason = reason if reason in _valid_reasons else "OUTRO"
        review_dict, _ = create_or_get_review(
            session=session,
            purchase=purchase,
            reason=normalized_reason,
            details=details or None,
            created_by="AGENTE",
        )
        # Serializa created_at
        from app.api.schemas.common import _serialize_utc
        created_at = review_dict.pop("created_at", None)
        if created_at is not None:
            review_dict["created_at"] = _serialize_utc(created_at)
        return review_dict

    return agent


# Instância singleton do agente; criada na primeira importação.
chat_agent: Agent[AgentDeps, str] = _make_agent()
