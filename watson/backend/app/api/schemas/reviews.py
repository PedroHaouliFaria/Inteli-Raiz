"""Esquemas de resposta para os endpoints de revisão (§8 do contrato)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.api.schemas.common import Money, SimulationTrue, UtcDatetime
from app.api.schemas.purchases import PurchaseStatus


ReviewKind = Literal["DUVIDA", "PROTECAO", "FALHA_AVALIACAO", "RISCO_ALTO"]
ReviewStatus = Literal["ABERTA", "FECHADA"]
ReviewCreatedBy = Literal["ASSOCIADO", "AGENTE", "SISTEMA"]
ReviewDecision = Literal["AUTHORIZE", "DENY"]


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
    decision: ReviewDecision | None
    decision_reason: str | None
    decided_by: str | None
    decided_at: UtcDatetime | None


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
                        "decision": None,
                        "decision_reason": None,
                        "decided_by": None,
                        "decided_at": None,
                    }
                ],
                "page": 1,
                "page_size": 20,
                "total": 1,
                "total_pages": 1,
                "simulation": True,
            }
        },
    }

    reviews: list[ReviewListItem]
    page: int
    page_size: int
    total: int
    total_pages: int
    simulation: SimulationTrue


class ReviewDecisionRequest(BaseModel):
    """Decisão da analista sobre uma revisão aberta."""

    model_config = {"extra": "forbid"}
    decision: ReviewDecision
    justification: str = Field(min_length=10, max_length=500)

    @field_validator("justification", mode="before")
    @classmethod
    def strip_justification(cls, value):
        return value.strip() if isinstance(value, str) else value


class ReviewDecisionResponse(BaseModel):
    """Resultado da decisão simulada da analista."""

    model_config = {"extra": "forbid"}

    review_id: str
    case_id: str
    decision: ReviewDecision
    justification: str
    decided_by: str
    decided_at: UtcDatetime
    review_status: Literal["FECHADA"]
    case_status: PurchaseStatus
    message: str
    simulation: SimulationTrue


class ReviewPurchaseDetail(BaseModel):
    model_config = {"extra": "forbid"}

    case_id: str
    customer_display_name: str
    amount: Money
    occurred_at: UtcDatetime
    merchant_category: str
    channel: str
    channel_label: str
    card_last4: str


class ReviewSignal(BaseModel):
    model_config = {"extra": "forbid"}

    code: str
    label: str


class ReviewAssociateResponse(BaseModel):
    model_config = {"extra": "forbid"}

    response: str
    answered_at: UtcDatetime


class ReviewAuditEvent(BaseModel):
    model_config = {"extra": "forbid"}

    event_type: str
    label: str
    from_status: str | None
    to_status: str | None
    created_at: UtcDatetime


class ReviewDetailResponse(BaseModel):
    """GET /api/reviews/{review_id}, sanitizado para a analista."""

    model_config = {"extra": "forbid"}

    review_id: str
    protocol: str
    kind: ReviewKind
    reason: str
    details: str | None
    status: ReviewStatus
    created_by: ReviewCreatedBy
    created_at: UtcDatetime
    decision: ReviewDecision | None
    decision_reason: str | None
    decided_by: str | None
    decided_at: UtcDatetime | None
    purchase: ReviewPurchaseDetail
    analysis: AnalysisSummary
    signals: list[ReviewSignal]
    associate_response: ReviewAssociateResponse | None
    timeline: list[ReviewAuditEvent]
    simulation: SimulationTrue
