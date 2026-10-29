"""Endpoints de revisão (§8 do contrato).

POST /api/purchases/{case_id}/review   — associado ou agente pede revisão
GET  /api/reviews                      — analista lista revisões abertas
"""
from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import AnalistaUser, AssociadoUser
from app.api.errors import ApiError
from app.api.schemas.reviews import AnalysisSummary, ReviewListItem, ReviewListResponse, ReviewOut
from app.db.repositories.purchases import PurchaseRepository
from app.db.session import get_session
from app.db.tables.purchases import Purchase, Review
from app.domain.personas import PERSONAS
from app.domain.reviews import create_or_get_review

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


def _customer_display(customer_id: str) -> str:
    for persona in PERSONAS.values():
        if persona.customer_id == customer_id:
            return persona.display_name
    return customer_id


@router.get("/api/reviews", response_model=ReviewListResponse)
def list_reviews(
    analista: AnalistaUser,
    session: Session = Depends(get_session),
):
    """Lista revisões abertas para o analista (§8).

    Associado recebe 403 FORBIDDEN_ROLE.
    """
    stmt = select(Review).order_by(Review.id.desc())
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
            )
        )

    return ReviewListResponse(reviews=items, simulation=True)
