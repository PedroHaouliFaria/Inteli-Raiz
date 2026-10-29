"""Esquemas de resposta para os endpoints de revisão (§8 do contrato)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from app.api.schemas.common import Money, SimulationTrue, UtcDatetime
from app.api.schemas.purchases import PurchaseStatus


ReviewKind = Literal["DUVIDA", "PROTECAO", "FALHA_AVALIACAO"]
ReviewStatus = Literal["ABERTA", "FECHADA"]
ReviewCreatedBy = Literal["ASSOCIADO", "AGENTE", "SISTEMA"]


class ReviewOut(BaseModel):
    """Revisão criada ou já existente (POST /api/purchases/{case_id}/review)."""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "review_id": "REV-13",
                "protocol": "RZ-20261028-0013",
                "case_id": "T-007",
                "kind": "DUVIDA",
                "reason": "NAO_RECONHECE_ESTABELECIMENTO",
                "status": "ABERTA",
                "created_at": "2026-10-28T03:13:14Z",
                "created_by": "AGENTE",
                "case_status": "AGUARDANDO_ASSOCIADO",
                "message": "Um analista vai olhar esta compra. Enquanto isso, você ainda pode responder se reconhece a compra.",
                "simulation": True,
            }
        },
    }

    review_id: str
    protocol: str
    case_id: str
    kind: ReviewKind
    reason: str
    status: ReviewStatus
    created_at: UtcDatetime
    created_by: ReviewCreatedBy
    case_status: PurchaseStatus
    message: str
    simulation: SimulationTrue


class AnalysisSummary(BaseModel):
    model_config = {"extra": "forbid"}
    score: float | None
    score_source: str | None
    model_version: str | None


class ReviewListItem(BaseModel):
    """Item da lista de revisões (GET /api/reviews)."""

    model_config = {"extra": "forbid"}

    review_id: str
    protocol: str
    case_id: str
    kind: ReviewKind
    reason: str
    status: ReviewStatus
    created_by: ReviewCreatedBy
    created_at: UtcDatetime
    case_status: PurchaseStatus
    customer_display_name: str
    amount: Money
    analysis: AnalysisSummary


class ReviewListResponse(BaseModel):
    """GET /api/reviews (analista)."""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "reviews": [
                    {
                        "review_id": "REV-12",
                        "protocol": "RZ-20261028-0012",
                        "case_id": "T-007",
                        "kind": "PROTECAO",
                        "reason": "OUTRO",
                        "status": "ABERTA",
                        "created_by": "SISTEMA",
                        "created_at": "2026-10-28T03:15:42Z",
                        "case_status": "RECUSADA_SIMULACAO",
                        "customer_display_name": "Ana Souza (fictícia)",
                        "amount": {"value": "149.58", "currency": "BRL"},
                        "analysis": {"score": 0.9917, "score_source": "modelo_local", "model_version": "rf-2026-10-27"},
                    }
                ],
                "simulation": True,
            }
        },
    }

    reviews: list[ReviewListItem]
    simulation: SimulationTrue
