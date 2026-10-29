"""Endpoints de compras (§5 do contrato).

GET /api/purchases              — lista de compras do associado
GET /api/purchases/{case_id}    — detalhe de uma compra
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import AssociadoUser
from app.api.errors import ApiError
from app.api.schemas.purchases import PurchaseDetailResponse, PurchaseListResponse
from app.db.repositories.purchases import PurchaseRepository
from app.db.session import get_session
from app.domain.cases.purchases import build_purchase_detail, build_purchase_list_item

router = APIRouter(prefix="/api/purchases", tags=["purchases"])


@router.get("", response_model=PurchaseListResponse)
def list_purchases(
    persona: AssociadoUser,
    session: Session = Depends(get_session),
) -> PurchaseListResponse:
    """Lista as compras do associado da sessão, da mais recente para a mais antiga."""
    repo = PurchaseRepository(session)
    rows = repo.list_by_owner(persona.customer_id)
    items = [build_purchase_list_item(p, c) for p, c in rows]
    return PurchaseListResponse(purchases=items, simulation=True)


@router.get("/{case_id}", response_model=PurchaseDetailResponse)
def get_purchase(
    case_id: str,
    persona: AssociadoUser,
    session: Session = Depends(get_session),
) -> PurchaseDetailResponse:
    """Detalhe de uma compra do associado da sessão.

    Compra de outra pessoa ou inexistente devolve 404 (R05).
    """
    repo = PurchaseRepository(session)
    result = repo.get_by_owner(persona.customer_id, case_id)
    if result is None:
        raise ApiError(
            status_code=404,
            code="NOT_FOUND",
            message="O recurso solicitado não foi encontrado.",
        )
    purchase, confirmation = result
    detail = build_purchase_detail(purchase, confirmation)
    return PurchaseDetailResponse(**detail, simulation=True)
