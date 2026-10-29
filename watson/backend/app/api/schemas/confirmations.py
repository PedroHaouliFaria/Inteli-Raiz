"""Esquemas de resposta para o endpoint de confirmação (§6 do contrato)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from app.api.schemas.common import SimulationTrue, UtcDatetime
from app.api.schemas.purchases import AssociateResponse, PurchaseStatus, ResultInfo


class ConfirmationResponseOut(BaseModel):
    """POST /api/confirmations/{challenge_id}/response — 200."""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "challenge_id": "CH-007",
                "case_id": "T-007",
                "response": "AUTHORIZE",
                "answered_at": "2026-10-28T03:15:42Z",
                "version": 3,
                "status": "LIBERADA_SIMULACAO",
                "status_label": "Compra liberada (simulação)",
                "review_protocol": None,
                "result": {
                    "title": "Compra autorizada na simulação",
                    "description": "Registramos que você reconhece e autoriza esta compra. Nenhuma transação real foi feita.",
                    "next_steps": [],
                },
                "replayed": False,
                "simulation": True,
            }
        },
    }

    challenge_id: str
    case_id: str
    response: AssociateResponse
    answered_at: UtcDatetime
    version: int
    status: PurchaseStatus
    status_label: str
    review_protocol: str | None
    result: ResultInfo
    replayed: bool
    simulation: SimulationTrue
