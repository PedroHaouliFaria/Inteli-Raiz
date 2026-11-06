"""Copiloto global do associado, com identidade sempre presa à sessão."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from pydantic_ai import Agent, RunContext


_SYSTEM_PROMPT = """\
Você é o Copiloto Raiz, assistente do associado para acompanhar todas as compras da sua conta.

Regras obrigatórias:
1. Responda em português do Brasil, de forma curta, clara e útil.
2. Use as ferramentas antes de afirmar dados sobre compras, valores, status ou revisões.
3. Nunca peça senha, PIN, cartão completo ou dados pessoais.
4. Nunca revele score interno, customer_id, card_id ou dados de outra pessoa.
5. Você pode listar compras, consultar uma compra, gerar um relatório e solicitar revisão humana.
6. Você não pode autorizar, recusar ou alterar diretamente uma compra. Essas decisões permanecem nos botões da tela.
7. Ao solicitar revisão, confirme o código da compra e o motivo no texto da resposta.
8. Não invente nome de estabelecimento: quando não existir, use apenas a categoria disponível.
9. O usuário pode mencionar códigos como T-007; consulte a compra e valide a propriedade pela ferramenta.
10. Respostas com no máximo 7 frases; use listas curtas quando ajudarem.
"""


def _money(cents: int) -> str:
    return format((Decimal(cents) / Decimal(100)).quantize(Decimal("0.01")), "f")


@dataclass
class CopilotDeps:
    customer_id: str
    db: Any


def _make_copilot() -> Agent[CopilotDeps, str]:
    from app.config import get_settings

    settings = get_settings()
    model = None
    if settings.groq_api_key:
        from pydantic_ai.models.groq import GroqModel
        from pydantic_ai.providers.groq import GroqProvider

        model = GroqModel(
            settings.llm_model.removeprefix("groq:"),
            provider=GroqProvider(api_key=settings.groq_api_key),
        )

    agent: Agent[CopilotDeps, str] = Agent(
        model=model,
        deps_type=CopilotDeps,
        system_prompt=_SYSTEM_PROMPT,
        defer_model_check=True,
    )

    @agent.tool
    async def listar_compras(
        ctx: RunContext[CopilotDeps],
        status: str = "",
    ) -> dict:
        """Lista as compras do associado; status é opcional e deve ser um status exato."""
        from sqlalchemy import select
        from sqlalchemy.orm import sessionmaker
        from app.db.tables.purchases import Purchase
        from app.domain.cases.purchases import _STATUS_LABELS
        from app.domain.signals.rules import mcc_label

        Session = sessionmaker(bind=ctx.deps.db)
        with Session() as session:
            purchases = session.execute(
                select(Purchase)
                .where(Purchase.customer_id == ctx.deps.customer_id)
                .order_by(Purchase.occurred_at.desc(), Purchase.id.desc())
            ).scalars().all()
            if status:
                purchases = [purchase for purchase in purchases if purchase.status == status]
            return {
                "total": len(purchases),
                "compras": [
                    {
                        "case_id": purchase.case_id,
                        "categoria": mcc_label(purchase.mcc),
                        "valor": _money(purchase.amount_cents),
                        "moeda": purchase.currency,
                        "data": purchase.occurred_at.isoformat(),
                        "status": _STATUS_LABELS.get(purchase.status, purchase.status),
                    }
                    for purchase in purchases[:30]
                ],
            }

    @agent.tool
    async def consultar_compra(
        ctx: RunContext[CopilotDeps],
        case_id: str,
    ) -> dict:
        """Consulta uma compra do associado pelo código, por exemplo T-007."""
        from sqlalchemy.orm import sessionmaker
        from app.db.repositories.purchases import PurchaseRepository
        from app.domain.cases.purchases import build_purchase_detail

        Session = sessionmaker(bind=ctx.deps.db)
        with Session() as session:
            result = PurchaseRepository(session).get_by_owner(ctx.deps.customer_id, case_id.upper())
            if result is None:
                return {"error": "Compra não encontrada para este associado."}
            purchase, confirmation = result
            detail = build_purchase_detail(purchase, confirmation, session=session)
            return {
                "case_id": detail["case_id"],
                "status": detail["status_label"],
                "purchase": detail["purchase"],
                "alert": detail["alert"],
                "review": detail["review"],
            }

    @agent.tool
    async def gerar_relatorio(ctx: RunContext[CopilotDeps]) -> dict:
        """Gera um resumo das compras, valores, status e revisões do associado."""
        from sqlalchemy import select
        from sqlalchemy.orm import sessionmaker
        from app.db.tables.purchases import Purchase, Review
        from app.domain.cases.purchases import _STATUS_LABELS

        Session = sessionmaker(bind=ctx.deps.db)
        with Session() as session:
            purchases = session.execute(
                select(Purchase).where(Purchase.customer_id == ctx.deps.customer_id)
            ).scalars().all()
            purchase_ids = [purchase.id for purchase in purchases]
            reviews = []
            if purchase_ids:
                reviews = session.execute(
                    select(Review).where(Review.purchase_id.in_(purchase_ids))
                ).scalars().all()
            counts: dict[str, int] = {}
            for purchase in purchases:
                label = _STATUS_LABELS.get(purchase.status, purchase.status)
                counts[label] = counts.get(label, 0) + 1
            total_cents = sum(purchase.amount_cents for purchase in purchases)
            return {
                "transacoes": len(purchases),
                "volume_total": _money(total_cents),
                "moeda": "BRL",
                "ticket_medio": _money(round(total_cents / len(purchases))) if purchases else "0.00",
                "por_status": counts,
                "revisoes_abertas": sum(review.status == "ABERTA" for review in reviews),
                "revisoes_encerradas": sum(review.status == "FECHADA" for review in reviews),
            }

    @agent.tool
    async def solicitar_revisao(
        ctx: RunContext[CopilotDeps],
        case_id: str,
        reason: str,
        details: str = "",
    ) -> dict:
        """Solicita revisão humana para uma compra do associado."""
        from sqlalchemy.orm import sessionmaker
        from app.db.repositories.purchases import PurchaseRepository
        from app.domain.reviews import create_or_get_review

        Session = sessionmaker(bind=ctx.deps.db)
        with Session() as session:
            result = PurchaseRepository(session).get_by_owner(ctx.deps.customer_id, case_id.upper())
            if result is None:
                return {"error": "Compra não encontrada para este associado."}
            purchase, _ = result
            valid = {
                "NAO_RECONHECE_ESTABELECIMENTO",
                "VALOR_DIFERENTE",
                "DUVIDA_PROCESSO",
                "OUTRO",
            }
            normalized = reason if reason in valid else "OUTRO"
            review, _ = create_or_get_review(
                session=session,
                purchase=purchase,
                reason=normalized,
                details=details or None,
                created_by="AGENTE",
            )
            return {
                "case_id": purchase.case_id,
                "protocol": review["protocol"],
                "status": review["status"],
                "reason": review["reason"],
            }

    return agent


copilot_agent: Agent[CopilotDeps, str] = _make_copilot()
