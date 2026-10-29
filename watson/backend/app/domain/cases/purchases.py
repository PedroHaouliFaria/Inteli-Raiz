"""Serviço de compras — monta as respostas do §5 a partir das entidades do banco.

Sem importações de FastAPI nem SQLAlchemy. Recebe entidades e devolve dicts prontos
para os schemas Pydantic.
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from app.db.tables.purchases import Confirmation, Purchase
from app.domain.signals.rules import compute_signals, mcc_label

# Rótulos de status do associado (§3 do contrato)
_STATUS_LABELS: dict[str, str] = {
    "RECEBIDA": "Compra recebida",
    "EM_AVALIACAO": "Em avaliação",
    "AGUARDANDO_ASSOCIADO": "Aguardando sua resposta",
    "LIBERADA_SIMULACAO": "Compra liberada (simulação)",
    "RECUSADA_SIMULACAO": "Compra recusada (simulação)",
    "REVISAO_PENDENTE": "Em revisão por um analista",
    "CONFIRMACAO_EXPIRADA": "Prazo encerrado, compra não autorizada",
}

# Rótulos de canal (§5 do contrato)
_CHANNEL_LABELS: dict[str, str] = {
    "CARTAO_NAO_PRESENTE": "Compra online ou por telefone",
    "CARTAO_PRESENTE": "Compra presencial",
}

# Headline de precaução quando não há sinais (§5)
_PRECAUTION_HEADLINE = (
    "Pedimos sua confirmação por precaução. "
    "Esta compra não tem um sinal de alerta específico."
)

# Headline padrão quando há sinais
_SIGNALS_HEADLINE = "Esta compra tem características diferentes do seu uso habitual."

# Disclaimer fixo
_DISCLAIMER = (
    "Os motivos acima são regras sobre os dados da compra. "
    "Eles não explicam sozinhos a avaliação do modelo."
)

# Respostas permitidas com rótulos
_ALLOWED_RESPONSES = [
    {"response": "AUTHORIZE", "label": "Reconheço e autorizo"},
    {"response": "DENY", "label": "Não reconheço"},
    {"response": "UNSURE", "label": "Estou em dúvida"},
]


def _cents_to_decimal_str(cents: int) -> str:
    """Converte centavos inteiros para string decimal com exatamente 2 casas."""
    value = Decimal(cents) / Decimal(100)
    return format(value.quantize(Decimal("0.01")), "f")


def _format_amount(purchase: Purchase) -> dict:
    return {"value": _cents_to_decimal_str(purchase.amount_cents), "currency": purchase.currency}


def _as_utc_naive(dt: datetime) -> datetime:
    """Normaliza datetime para naive UTC (sem tzinfo), como saem do banco SQLite."""
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def build_purchase_list_item(purchase: Purchase, confirmation: Confirmation | None) -> dict:
    """Monta o item da lista de compras (GET /api/purchases)."""
    # expires_at só quando AGUARDANDO_ASSOCIADO (§5)
    expires_at = None
    if purchase.status == "AGUARDANDO_ASSOCIADO" and confirmation is not None:
        expires_at = _as_utc_naive(confirmation.expires_at)

    return {
        "case_id": purchase.case_id,
        "merchant_display": f"{mcc_label(purchase.mcc)} (nome do estabelecimento não disponível)",
        "amount": _format_amount(purchase),
        "occurred_at": _as_utc_naive(purchase.occurred_at),
        "status": purchase.status,
        "status_label": _STATUS_LABELS.get(purchase.status, purchase.status),
        "expires_at": expires_at,
    }


def build_purchase_detail(purchase: Purchase, confirmation: Confirmation | None) -> dict:
    """Monta o detalhe da compra (GET /api/purchases/{case_id}).

    A expiração na leitura (verificar se venceu e gravar CONFIRMACAO_EXPIRADA)
    entra na próxima sessão.
    TODO(sessão 2): verificar expiração na leitura e gravar transição de estado
    """
    features = purchase.features_json or {}
    signals = compute_signals(features)

    # alert
    headline = _SIGNALS_HEADLINE if signals else _PRECAUTION_HEADLINE
    alert = {
        "headline": headline,
        "signals": [{"code": s.code, "label": s.label, "source": s.source} for s in signals],
        "disclaimer": _DISCLAIMER,
    }

    # channel_label
    channel_label = _CHANNEL_LABELS.get(purchase.channel, purchase.channel)

    # purchase info
    purchase_info = {
        "merchant_name": None,
        "merchant_category": {"mcc": purchase.mcc, "label": mcc_label(purchase.mcc)},
        "merchant_display": f"{mcc_label(purchase.mcc)} (nome do estabelecimento não disponível)",
        "amount": _format_amount(purchase),
        "occurred_at": _as_utc_naive(purchase.occurred_at),
        "channel": purchase.channel,
        "channel_label": channel_label,
        "card": {
            "brand": purchase.card_brand,
            "type": purchase.card_type,
            "last4": purchase.card_last4,
        },
    }

    # confirmation block
    if confirmation is not None:
        allowed = _ALLOWED_RESPONSES if purchase.status == "AGUARDANDO_ASSOCIADO" else []
        answered = None
        if confirmation.answered_response is not None and confirmation.answered_at is not None:
            answered = {
                "response": confirmation.answered_response,
                "answered_at": _as_utc_naive(confirmation.answered_at),
            }
        confirmation_block = {
            "challenge_id": confirmation.challenge_id,
            "question": "Você reconhece e autoriza esta compra?",
            "allowed_responses": allowed,
            "expires_at": _as_utc_naive(confirmation.expires_at),
            "answered": answered,
        }
    else:
        confirmation_block = None

    return {
        "case_id": purchase.case_id,
        "version": purchase.version,
        "status": purchase.status,
        "status_label": _STATUS_LABELS.get(purchase.status, purchase.status),
        "purchase": purchase_info,
        "alert": alert,
        "confirmation": confirmation_block,
        "review": None,  # TODO(sessão 2): buscar revisão aberta
        "result": None,  # TODO(sessão 2): montar result para status terminais
        "policy_version": "confirmacao-v2",
    }
