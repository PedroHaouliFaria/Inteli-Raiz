"""Testes dos esquemas Pydantic de resposta (§2, §4 e §5 do contrato)."""
import pytest
from pydantic import ValidationError

from app.api.schemas.common import Money, SimulationTrue
from app.api.schemas.purchases import (
    PurchaseListResponse,
    PurchaseDetailResponse,
    PurchaseStatusResponse,
)
from app.api.schemas.confirmations import ConfirmationResponseOut
from app.api.schemas.reviews import ReviewOut, ReviewListResponse


# ---------------------------------------------------------------------------
# Money
# ---------------------------------------------------------------------------

def test_money_accepts_valid_decimal_string():
    m = Money(value="149.58", currency="BRL")
    assert m.value == "149.58"


def test_money_rejects_incomplete_decimal():
    with pytest.raises(ValidationError):
        Money(value="149.5", currency="BRL")  # não tem dois dígitos de centavos


def test_money_rejects_float():
    with pytest.raises(ValidationError):
        Money(value=149.58, currency="BRL")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# PurchaseListResponse — exemplo da spec §5
# ---------------------------------------------------------------------------

PURCHASE_LIST_EXAMPLE = {
    "purchases": [
        {
            "case_id": "T-007",
            "merchant_display": "Supermercado (nome do estabelecimento não disponível)",
            "amount": {"value": "149.58", "currency": "BRL"},
            "occurred_at": "2026-10-25T06:12:00Z",
            "status": "AGUARDANDO_ASSOCIADO",
            "status_label": "Aguardando sua resposta",
            "expires_at": "2026-10-28T03:27:00Z",
        },
        {
            "case_id": "T-003",
            "merchant_display": "Farmácia (nome do estabelecimento não disponível)",
            "amount": {"value": "15.68", "currency": "BRL"},
            "occurred_at": "2026-10-19T21:40:00Z",
            "status": "LIBERADA_SIMULACAO",
            "status_label": "Compra liberada (simulação)",
            "expires_at": None,
        },
    ],
    "simulation": True,
}


def test_purchase_list_example_validates_and_roundtrips():
    obj = PurchaseListResponse(**PURCHASE_LIST_EXAMPLE)
    dumped = obj.model_dump(mode="json")
    assert dumped["simulation"] is True
    assert dumped["purchases"][0]["case_id"] == "T-007"
    assert dumped["purchases"][0]["amount"]["value"] == "149.58"


def test_feedback_label_rejected_in_purchase_list():
    bad = {**PURCHASE_LIST_EXAMPLE}
    bad["purchases"] = [{**PURCHASE_LIST_EXAMPLE["purchases"][0], "feedback_label": "fraude"}]
    with pytest.raises(ValidationError):
        PurchaseListResponse(**bad)


# ---------------------------------------------------------------------------
# PurchaseDetailResponse — exemplo §5
# ---------------------------------------------------------------------------

PURCHASE_DETAIL_AWAITING = {
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
            {"code": "MADRUGADA", "label": "Feita de madrugada, às 3h.", "source": "regra"},
            {"code": "PRIMEIRA_COMPRA_CARTAO", "label": "Primeira compra registrada com este cartão.", "source": "regra"},
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


def test_purchase_detail_awaiting_validates_and_roundtrips():
    obj = PurchaseDetailResponse(**PURCHASE_DETAIL_AWAITING)
    dumped = obj.model_dump(mode="json")
    assert dumped["simulation"] is True
    assert dumped["version"] == 2
    assert dumped["confirmation"]["challenge_id"] == "CH-007"
    assert len(dumped["alert"]["signals"]) == 3


def test_purchase_detail_rejects_forbidden_fields():
    bad = {**PURCHASE_DETAIL_AWAITING, "customer_id": "CUST_SYN_0001"}
    with pytest.raises(ValidationError):
        PurchaseDetailResponse(**bad)


# ---------------------------------------------------------------------------
# PurchaseStatusResponse — exemplo §5
# ---------------------------------------------------------------------------

PURCHASE_STATUS_EXAMPLE = {
    "case_id": "T-007",
    "version": 2,
    "status": "AGUARDANDO_ASSOCIADO",
    "status_label": "Aguardando sua resposta",
    "expires_at": "2026-10-28T03:27:00Z",
    "seconds_remaining": 642,
    "allowed_responses": ["AUTHORIZE", "DENY", "UNSURE"],
    "review_protocol": None,
    "next_steps": [
        "Responda se reconhece a compra antes do prazo.",
        "Se tiver dúvida, pergunte no chat ou escolha \"Estou em dúvida\".",
    ],
    "simulation": True,
}


def test_purchase_status_example_validates():
    obj = PurchaseStatusResponse(**PURCHASE_STATUS_EXAMPLE)
    dumped = obj.model_dump(mode="json")
    assert dumped["simulation"] is True
    assert dumped["seconds_remaining"] == 642


# ---------------------------------------------------------------------------
# ConfirmationResponseOut — exemplo §6
# ---------------------------------------------------------------------------

CONFIRM_RESPONSE_EXAMPLE = {
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


def test_confirmation_response_example_validates():
    obj = ConfirmationResponseOut(**CONFIRM_RESPONSE_EXAMPLE)
    dumped = obj.model_dump(mode="json")
    assert dumped["simulation"] is True
    assert dumped["replayed"] is False
    assert dumped["response"] == "AUTHORIZE"


# ---------------------------------------------------------------------------
# ReviewOut — exemplo §8
# ---------------------------------------------------------------------------

REVIEW_OUT_EXAMPLE = {
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


def test_review_out_example_validates():
    obj = ReviewOut(**REVIEW_OUT_EXAMPLE)
    dumped = obj.model_dump(mode="json")
    assert dumped["simulation"] is True
    assert dumped["kind"] == "DUVIDA"
