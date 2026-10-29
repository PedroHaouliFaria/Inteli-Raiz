"""Esquemas de resposta para os endpoints de compras (§5 do contrato)."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.api.schemas.common import Money, SimulationTrue, UtcDatetime


# Enum de status da compra conforme §3 do contrato
PurchaseStatus = Literal[
    "RECEBIDA",
    "EM_AVALIACAO",
    "AGUARDANDO_ASSOCIADO",
    "LIBERADA_SIMULACAO",
    "RECUSADA_SIMULACAO",
    "REVISAO_PENDENTE",
    "CONFIRMACAO_EXPIRADA",
]

# Resposta do associado à confirmação (§6)
AssociateResponse = Literal["AUTHORIZE", "DENY", "UNSURE"]

# Canal da compra (§5): T-003 e T-011 são presenciais
PurchaseChannel = Literal["CARTAO_PRESENTE", "CARTAO_NAO_PRESENTE"]

# Origem dos sinais (§5)
SignalSource = Literal["regra"]


# ---------------------------------------------------------------------------
# Sub-modelos compartilhados
# ---------------------------------------------------------------------------

class MerchantCategory(BaseModel):
    model_config = {"extra": "forbid"}
    mcc: str
    label: str


class CardInfo(BaseModel):
    model_config = {"extra": "forbid"}
    brand: str
    type: str
    last4: str


class PurchaseInfo(BaseModel):
    model_config = {"extra": "forbid"}
    merchant_name: str | None
    merchant_category: MerchantCategory
    merchant_display: str
    amount: Money
    occurred_at: UtcDatetime
    channel: PurchaseChannel
    channel_label: str
    card: CardInfo


class Signal(BaseModel):
    model_config = {"extra": "forbid"}
    code: str
    label: str
    source: SignalSource


class Alert(BaseModel):
    model_config = {"extra": "forbid"}
    headline: str
    signals: list[Signal]
    disclaimer: str


class AllowedResponse(BaseModel):
    model_config = {"extra": "forbid"}
    response: AssociateResponse
    label: str


class AnsweredInfo(BaseModel):
    model_config = {"extra": "forbid"}
    response: AssociateResponse
    answered_at: UtcDatetime


class ConfirmationInfo(BaseModel):
    model_config = {"extra": "forbid"}
    challenge_id: str
    question: str
    allowed_responses: list[AllowedResponse]
    expires_at: UtcDatetime
    answered: AnsweredInfo | None


class ReviewSummary(BaseModel):
    model_config = {"extra": "forbid"}
    review_id: str
    protocol: str
    kind: Literal["DUVIDA", "PROTECAO", "FALHA_AVALIACAO"]
    status: Literal["ABERTA", "FECHADA"]


class ResultInfo(BaseModel):
    model_config = {"extra": "forbid"}
    title: str
    description: str
    next_steps: list[str]


# ---------------------------------------------------------------------------
# PurchaseListItem — item da lista de compras
# ---------------------------------------------------------------------------

class PurchaseListItem(BaseModel):
    model_config = {"extra": "forbid"}
    case_id: str
    merchant_display: str
    amount: Money
    occurred_at: UtcDatetime
    status: PurchaseStatus
    status_label: str
    expires_at: UtcDatetime | None


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------

class PurchaseListResponse(BaseModel):
    """GET /api/purchases."""

    model_config = {"extra": "forbid"}

    purchases: list[PurchaseListItem]
    simulation: SimulationTrue

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "purchases": [
                    {
                        "case_id": "T-007",
                        "merchant_display": "Supermercado (nome do estabelecimento não disponível)",
                        "amount": {"value": "149.58", "currency": "BRL"},
                        "occurred_at": "2026-10-25T06:12:00Z",
                        "status": "AGUARDANDO_ASSOCIADO",
                        "status_label": "Aguardando sua resposta",
                        "expires_at": "2026-10-28T03:27:00Z",
                    }
                ],
                "simulation": True,
            }
        },
    }


class PurchaseDetailResponse(BaseModel):
    """GET /api/purchases/{case_id}."""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "case_id": "T-007",
                "version": 2,
                "status": "AGUARDANDO_ASSOCIADO",
                "status_label": "Aguardando sua resposta",
                "purchase": {
                    "merchant_name": None,
                    "merchant_category": {"mcc": "5411", "label": "Supermercado"},
                    "merchant_display": "Supermercado (nome do estabelecimento não disponível)",
                    "amount": {"value": "149.58", "currency": "BRL"},
                    "occurred_at": "2026-10-25T06:12:00Z",
                    "channel": "CARTAO_NAO_PRESENTE",
                    "channel_label": "Compra online ou por telefone",
                    "card": {"brand": "BANDEIRA_A", "type": "credito", "last4": "2938"},
                },
                "alert": {
                    "headline": "Esta compra tem características diferentes do seu uso habitual.",
                    "signals": [
                        {"code": "CARTAO_NAO_PRESENTE", "label": "Feita sem o cartão físico (online ou por telefone).", "source": "regra"},
                    ],
                    "disclaimer": "Os motivos acima são regras sobre os dados da compra. Eles não explicam sozinhos a avaliação do modelo.",
                },
                "confirmation": {
                    "challenge_id": "CH-007",
                    "question": "Você reconhece e autoriza esta compra?",
                    "allowed_responses": [
                        {"response": "AUTHORIZE", "label": "Reconheço e autorizo"},
                        {"response": "DENY", "label": "Não reconheço"},
                        {"response": "UNSURE", "label": "Estou em dúvida"},
                    ],
                    "expires_at": "2026-10-28T03:27:00Z",
                    "answered": None,
                },
                "review": None,
                "result": None,
                "policy_version": "confirmacao-v2",
                "simulation": True,
            }
        },
    }

    case_id: str
    version: int
    status: PurchaseStatus
    status_label: str
    purchase: PurchaseInfo
    alert: Alert
    confirmation: ConfirmationInfo | None
    review: ReviewSummary | None
    result: ResultInfo | None
    policy_version: str
    simulation: SimulationTrue


class PurchaseStatusResponse(BaseModel):
    """GET /api/purchases/{case_id}/status."""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "case_id": "T-007",
                "version": 2,
                "status": "AGUARDANDO_ASSOCIADO",
                "status_label": "Aguardando sua resposta",
                "expires_at": "2026-10-28T03:27:00Z",
                "seconds_remaining": 642,
                "allowed_responses": ["AUTHORIZE", "DENY", "UNSURE"],
                "review_protocol": None,
                "next_steps": ["Responda se reconhece a compra antes do prazo."],
                "simulation": True,
            }
        },
    }

    case_id: str
    version: int
    status: PurchaseStatus
    status_label: str
    expires_at: UtcDatetime | None
    seconds_remaining: int
    allowed_responses: list[AssociateResponse]
    review_protocol: str | None
    next_steps: list[str]
    simulation: SimulationTrue
