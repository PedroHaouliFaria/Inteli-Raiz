"""Endpoints de revisão (§8 do contrato).

POST /api/purchases/{case_id}/review   — associado ou agente pede revisão
GET  /api/reviews                      — analista lista revisões abertas
"""
from __future__ import annotations

import math
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import AnalistaUser, AssociadoUser
from app.api.errors import ApiError
from app.api.schemas.reviews import (
    AnalystFlowCustomer,
    AnalystFlowPurchase,
    AnalystFlowResponse,
    AnalysisSummary,
    ReviewDecisionRequest,
    ReviewDecisionResponse,
    ReviewDetailResponse,
    ReviewListItem,
    ReviewListResponse,
    ReviewOut,
)
from app.db.repositories.purchases import PurchaseRepository
from app.db.session import get_session
from app.db.tables.purchases import Confirmation, Event, Purchase, Review
from app.domain.personas import PERSONAS
from app.domain.reviews import create_or_get_review
from app.domain.signals.rules import compute_signals, mcc_label
from app.domain.cases.purchases import _STATUS_LABELS

router = APIRouter(tags=["reviews"])


# ---------------------------------------------------------------------------
# POST /api/purchases/{case_id}/review — associado solicita revisão
# ---------------------------------------------------------------------------

class _ReviewRequest:
    def __init__(self, reason: str, details: str | None = None):
        self.reason = reason
        self.details = details


@router.post("/api/purchases/{case_id}/review", status_code=201, response_model=ReviewOut)
def request_review(
    case_id: str,
    body: Annotated[dict, Body()],
    persona: AssociadoUser,
    session: Session = Depends(get_session),
):
    """Associado pede revisão de uma compra (§8).

    201 quando cria nova revisão; 200 quando já existe uma ABERTA.
    Não muda o status da compra.
    """
    reason = body.get("reason", "")
    details = body.get("details")

    repo = PurchaseRepository(session)
    result = repo.get_by_owner(persona.customer_id, case_id)
    if result is None:
        raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")
    purchase, _ = result

    review_dict, status_code = create_or_get_review(
        session=session,
        purchase=purchase,
        reason=reason,
        details=details,
        created_by="ASSOCIADO",
    )

    from fastapi.responses import JSONResponse
    from app.api.schemas.common import _serialize_utc
    # Formata o created_at como string UTC
    created_at = review_dict.pop("created_at", None)
    if created_at is not None:
        review_dict["created_at"] = _serialize_utc(created_at)

    return JSONResponse(
        content={**review_dict, "simulation": True},
        status_code=status_code,
    )


# ---------------------------------------------------------------------------
# GET /api/reviews — analista lista exceções
# ---------------------------------------------------------------------------

def _cents_to_str(cents: int) -> str:
    value = Decimal(cents) / Decimal(100)
    return format(value.quantize(Decimal("0.01")), "f")


def _utc_naive(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(UTC).replace(tzinfo=None)


def _customer_display(customer_id: str) -> str:
    for persona in PERSONAS.values():
        if persona.customer_id == customer_id:
            return persona.display_name
    return "Associado fictício"


def _persona_display(persona_id: str | None) -> str | None:
    if persona_id is None:
        return None
    persona = PERSONAS.get(persona_id)
    return persona.display_name if persona is not None else "Analista"


_CHANNEL_LABELS = {
    "CARTAO_NAO_PRESENTE": "Compra online ou por telefone",
    "CARTAO_PRESENTE": "Compra presencial",
}

_EVENT_LABELS = {
    "SEED": "Compra registrada",
    "ANSWER": "Resposta do associado registrada",
    "EXPIRE": "Prazo de confirmação encerrado",
    "REVIEW_REQUESTED": "Revisão humana solicitada",
    "ANALYST_DECISION": "Decisão da analista registrada",
    "MODEL_EVALUATED": "Análise do modelo registrada",
}


@router.get("/api/reviews", response_model=ReviewListResponse)
def list_reviews(
    analista: AnalistaUser,
    session: Session = Depends(get_session),
    status: str = Query("ABERTA", pattern="^(ABERTA|FECHADA)$"),
    decision: str | None = Query(None, pattern="^(AUTHORIZE|DENY)$"),
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """Lista revisões pendentes ou encerradas com filtros e paginação.

    Associado recebe 403 FORBIDDEN_ROLE.
    """
    filters = [Review.status == status]
    if decision is not None:
        filters.append(Review.decision == decision)

    date_column = Review.decided_at if status == "FECHADA" else Review.created_at
    if from_date is not None:
        filters.append(date_column >= _utc_naive(from_date))
    if to_date is not None:
        filters.append(date_column <= _utc_naive(to_date))

    total = session.execute(
        select(func.count()).select_from(Review).where(*filters)
    ).scalar_one()
    order = Review.created_at.asc() if status == "ABERTA" else Review.decided_at.desc()
    stmt = (
        select(Review)
        .where(*filters)
        .order_by(order, Review.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    reviews = session.execute(stmt).scalars().all()

    items = []
    for rev in reviews:
        purchase = session.get(Purchase, rev.purchase_id)
        if purchase is None:
            continue

        analysis = AnalysisSummary(
            score=purchase.analysis_score,
            score_source=purchase.analysis_score_source,
            model_version=purchase.analysis_model_version,
        )

        items.append(
            ReviewListItem(
                review_id=rev.review_id,
                protocol=rev.protocol,
                case_id=purchase.case_id,
                kind=rev.kind,
                reason=rev.reason,
                status=rev.status,
                created_by=rev.created_by,
                created_at=rev.created_at,
                case_status=purchase.status,
                customer_display_name=_customer_display(purchase.customer_id),
                amount={"value": _cents_to_str(purchase.amount_cents), "currency": purchase.currency},
                analysis=analysis,
                decision=rev.decision,
                decision_reason=rev.decision_reason,
                decided_by=_persona_display(rev.decided_by),
                decided_at=rev.decided_at,
            )
        )

    return ReviewListResponse(
        reviews=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=math.ceil(total / page_size) if total else 0,
        simulation=True,
    )


@router.get("/api/analyst/purchases", response_model=AnalystFlowResponse)
def list_analyst_purchase_flow(
    analista: AnalistaUser,
    session: Session = Depends(get_session),
    customer_id: str | None = Query(None),
    status: str | None = Query(None),
):
    """Lista todas as compras para acompanhamento, sem misturá-las à fila.

    A fila de pendências continua vindo exclusivamente de ``/api/reviews``.
    Esta rota é somente leitura e permite à analista acompanhar o fluxo por
    associado e estado atual.
    """
    all_purchases = session.execute(
        select(Purchase).order_by(Purchase.occurred_at.desc(), Purchase.id.desc())
    ).scalars().all()

    customer_totals: dict[str, int] = {}
    for purchase in all_purchases:
        customer_totals[purchase.customer_id] = customer_totals.get(purchase.customer_id, 0) + 1

    summary_purchases = [
        purchase
        for purchase in all_purchases
        if customer_id is None or purchase.customer_id == customer_id
    ]
    status_counts: dict[str, int] = {}
    for purchase in summary_purchases:
        status_counts[purchase.status] = status_counts.get(purchase.status, 0) + 1

    filtered = [
        purchase
        for purchase in all_purchases
        if (customer_id is None or purchase.customer_id == customer_id)
        and (status is None or purchase.status == status)
    ]

    items: list[AnalystFlowPurchase] = []
    for purchase in filtered:
        latest_review = session.execute(
            select(Review)
            .where(Review.purchase_id == purchase.id)
            .order_by(Review.id.desc())
        ).scalars().first()
        items.append(
            AnalystFlowPurchase(
                case_id=purchase.case_id,
                customer_id=purchase.customer_id,
                customer_display_name=_customer_display(purchase.customer_id),
                merchant_display=f"{mcc_label(purchase.mcc)} (nome não disponível)",
                amount={"value": _cents_to_str(purchase.amount_cents), "currency": purchase.currency},
                occurred_at=purchase.occurred_at,
                status=purchase.status,
                status_label=_STATUS_LABELS.get(purchase.status, purchase.status),
                review_protocol=latest_review.protocol if latest_review else None,
                review_status=latest_review.status if latest_review else None,
            )
        )

    customers = [
        AnalystFlowCustomer(
            customer_id=identifier,
            display_name=_customer_display(identifier),
            purchase_count=count,
        )
        for identifier, count in sorted(
            customer_totals.items(),
            key=lambda item: _customer_display(item[0]),
        )
    ]
    return AnalystFlowResponse(
        purchases=items,
        customers=customers,
        status_counts=status_counts,
        total=len(filtered),
        simulation=True,
    )


@router.get("/api/reviews/{review_id}", response_model=ReviewDetailResponse)
def get_review(
    review_id: str,
    analista: AnalistaUser,
    session: Session = Depends(get_session),
) -> ReviewDetailResponse:
    """Retorna o detalhe sanitizado antes da decisão da analista."""
    review = session.execute(
        select(Review).where(Review.review_id == review_id)
    ).scalar_one_or_none()
    if review is None:
        raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")

    purchase = session.get(Purchase, review.purchase_id)
    if purchase is None:
        raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")

    confirmation = session.execute(
        select(Confirmation)
        .where(Confirmation.purchase_id == purchase.id)
        .order_by(Confirmation.id.desc())
    ).scalars().first()
    associate_response = None
    if confirmation and confirmation.answered_response and confirmation.answered_at:
        associate_response = {
            "response": confirmation.answered_response,
            "answered_at": confirmation.answered_at,
        }

    events = session.execute(
        select(Event).where(Event.purchase_id == purchase.id).order_by(Event.id.asc())
    ).scalars().all()
    timeline = [
        {
            "event_type": event.event_type,
            "label": _EVENT_LABELS.get(event.event_type, "Atualização do processo"),
            "from_status": event.from_status,
            "to_status": event.to_status,
            "created_at": event.created_at,
        }
        for event in events
    ]

    signals = compute_signals(purchase.features_json or {})
    return ReviewDetailResponse(
        review_id=review.review_id,
        protocol=review.protocol,
        kind=review.kind,
        reason=review.reason,
        details=review.details,
        status=review.status,
        created_by=review.created_by,
        created_at=review.created_at,
        decision=review.decision,
        decision_reason=review.decision_reason,
        decided_by=_persona_display(review.decided_by),
        decided_at=review.decided_at,
        purchase={
            "case_id": purchase.case_id,
            "customer_display_name": _customer_display(purchase.customer_id),
            "amount": {"value": _cents_to_str(purchase.amount_cents), "currency": purchase.currency},
            "occurred_at": purchase.occurred_at,
            "status": purchase.status,
            "status_label": _STATUS_LABELS.get(purchase.status, purchase.status),
            "merchant_category": mcc_label(purchase.mcc),
            "channel": purchase.channel,
            "channel_label": _CHANNEL_LABELS.get(purchase.channel, "Canal não informado"),
            "card_last4": purchase.card_last4,
        },
        analysis={
            "score": purchase.analysis_score,
            "score_source": purchase.analysis_score_source,
            "model_version": purchase.analysis_model_version,
        },
        signals=[{"code": signal.code, "label": signal.label} for signal in signals],
        associate_response=associate_response,
        timeline=timeline,
        simulation=True,
    )


@router.post(
    "/api/reviews/{review_id}/decision",
    response_model=ReviewDecisionResponse,
)
def decide_review(
    review_id: str,
    body: ReviewDecisionRequest,
    analista: AnalistaUser,
    session: Session = Depends(get_session),
) -> ReviewDecisionResponse:
    """Analista libera ou recusa a compra e encerra a revisão na simulação."""
    from app.domain.reviews import resolve_review

    result = resolve_review(
        session=session,
        review_id=review_id,
        decision=body.decision,
        justification=body.justification,
        analyst_id=analista.persona_id,
    )
    result["decided_by"] = analista.display_name
    return ReviewDecisionResponse(**result, simulation=True)
