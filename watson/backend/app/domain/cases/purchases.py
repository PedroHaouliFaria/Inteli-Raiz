"""Serviço de compras — monta as respostas do §5 a partir das entidades do banco.

Sem importações de FastAPI nem SQLAlchemy. Recebe entidades e devolve dicts prontos
para os schemas Pydantic.
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db.tables.purchases import Confirmation, Event, Purchase, Review
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

# Textos de result por estado terminal
_RESULT_BY_RESPONSE = {
    "AUTHORIZE": {
        "title": "Compra autorizada na simulação",
        "description": (
            "Registramos que você reconhece e autoriza esta compra. "
            "Nenhuma transação real foi feita."
        ),
        "next_steps": [],
    },
    "DENY": {
        "title": "Compra recusada na simulação",
        "description": (
            "Registramos que você não reconhece esta compra. "
            "Um analista vai revisar o caso. O cartão não foi bloqueado."
        ),
        # next_steps será montado dinamicamente com o protocolo
    },
    "UNSURE": {
        "title": "Compra em revisão",
        "description": (
            "Registramos sua dúvida. Um analista vai analisar esta compra."
        ),
        # next_steps será montado dinamicamente com o protocolo
    },
}

_RESULT_EXPIRADA = {
    "title": "Prazo de resposta encerrado",
    "description": (
        "O prazo para responder a esta compra terminou. "
        "Ela não foi autorizada. Se ela for sua, peça uma revisão."
    ),
    "next_steps": ["A compra não foi autorizada.", "Se ela for sua, peça uma revisão."],
}


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


def _now_utc_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ---------------------------------------------------------------------------
# Expiração
# ---------------------------------------------------------------------------

def check_and_expire(
    purchase: Purchase,
    confirmation: Confirmation | None,
    session: Session,
) -> bool:
    """Verifica se a confirmação expirou e, se sim, grava a transição de estado.

    Retorna True se expirou (e a transição foi gravada); False caso contrário.
    A sessão SQL é modificada mas não commitada — quem chama deve commitar.
    """
    if purchase.status != "AGUARDANDO_ASSOCIADO":
        return False
    if confirmation is None:
        return False

    now = _now_utc_naive()
    expires_at = _as_utc_naive(confirmation.expires_at)
    if now <= expires_at:
        return False

    # Expirou: grava transição
    from_status = purchase.status
    purchase.status = "CONFIRMACAO_EXPIRADA"
    purchase.version += 1
    purchase.updated_at = now

    event = Event(
        purchase_id=purchase.id,
        event_type="EXPIRE",
        from_status=from_status,
        to_status="CONFIRMACAO_EXPIRADA",
        created_at=now,
    )
    session.add(event)
    return True


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def _build_review_summary(review: Review | None) -> dict | None:
    if review is None:
        return None
    return {
        "review_id": review.review_id,
        "protocol": review.protocol,
        "kind": review.kind,
        "status": review.status,
    }


def _build_result(purchase: Purchase, review: Review | None) -> dict | None:
    """Monta o bloco result para estados terminais."""
    if purchase.status == "LIBERADA_SIMULACAO":
        return {**_RESULT_BY_RESPONSE["AUTHORIZE"], "next_steps": []}

    if purchase.status == "RECUSADA_SIMULACAO":
        protocol = review.protocol if review else None
        next_steps = []
        if protocol:
            next_steps = [
                f"Guarde o protocolo {protocol}.",
                "Você pode acompanhar o status nesta tela.",
            ]
        return {
            "title": _RESULT_BY_RESPONSE["DENY"]["title"],
            "description": _RESULT_BY_RESPONSE["DENY"]["description"],
            "next_steps": next_steps,
        }

    if purchase.status == "REVISAO_PENDENTE":
        protocol = review.protocol if review else None
        next_steps = []
        if protocol:
            next_steps = [
                f"Guarde o protocolo {protocol}.",
                "Um analista vai analisar e entrar em contato.",
            ]
        return {
            "title": _RESULT_BY_RESPONSE["UNSURE"]["title"],
            "description": _RESULT_BY_RESPONSE["UNSURE"]["description"],
            "next_steps": next_steps,
        }

    if purchase.status == "CONFIRMACAO_EXPIRADA":
        return _RESULT_EXPIRADA.copy()

    return None


def _get_open_review(purchase: Purchase) -> Review | None:
    """Retorna a primeira revisão aberta, ou None."""
    for rev in purchase.reviews:
        if rev.status == "ABERTA":
            return rev
    return None


def build_purchase_list_item(
    purchase: Purchase,
    confirmation: Confirmation | None,
    session: Session | None = None,
) -> dict:
    """Monta o item da lista de compras (GET /api/purchases).

    Recebe session para poder gravar a transição de expiração, se necessário.
    """
    if session is not None:
        expired = check_and_expire(purchase, confirmation, session)
        if expired:
            session.commit()

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


def build_purchase_detail(
    purchase: Purchase,
    confirmation: Confirmation | None,
    session: Session | None = None,
) -> dict:
    """Monta o detalhe da compra (GET /api/purchases/{case_id})."""
    if session is not None:
        expired = check_and_expire(purchase, confirmation, session)
        if expired:
            session.commit()

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

    # review e result para estados terminais
    open_review = _get_open_review(purchase)
    review_summary = _build_review_summary(open_review)
    result = _build_result(purchase, open_review)

    return {
        "case_id": purchase.case_id,
        "version": purchase.version,
        "status": purchase.status,
        "status_label": _STATUS_LABELS.get(purchase.status, purchase.status),
        "purchase": purchase_info,
        "alert": alert,
        "confirmation": confirmation_block,
        "review": review_summary,
        "result": result,
        "policy_version": "confirmacao-v2",
    }


def build_purchase_status(
    purchase: Purchase,
    confirmation: Confirmation | None,
    session: Session | None = None,
) -> dict:
    """Monta o status leve da compra (GET /api/purchases/{case_id}/status)."""
    if session is not None:
        expired = check_and_expire(purchase, confirmation, session)
        if expired:
            session.commit()

    # seconds_remaining
    now = _now_utc_naive()
    seconds_remaining = 0
    expires_at = None
    if confirmation is not None:
        expires_at = _as_utc_naive(confirmation.expires_at)
        if purchase.status == "AGUARDANDO_ASSOCIADO":
            diff = (expires_at - now).total_seconds()
            seconds_remaining = max(0, math.floor(diff))
        elif purchase.status == "CONFIRMACAO_EXPIRADA":
            seconds_remaining = 0

    # allowed_responses: só quando aguardando
    allowed_responses: list[str] = []
    if purchase.status == "AGUARDANDO_ASSOCIADO":
        allowed_responses = ["AUTHORIZE", "DENY", "UNSURE"]

    # review_protocol
    open_review = _get_open_review(purchase)
    review_protocol = open_review.protocol if open_review else None

    # next_steps dependem do status
    next_steps: list[str]
    if purchase.status == "AGUARDANDO_ASSOCIADO":
        next_steps = [
            "Responda se reconhece a compra antes do prazo.",
            'Se tiver dúvida, pergunte no chat ou escolha "Estou em dúvida".',
        ]
    elif purchase.status == "CONFIRMACAO_EXPIRADA":
        next_steps = [
            "A compra não foi autorizada.",
            "Se ela for sua, peça uma revisão.",
        ]
    elif purchase.status == "LIBERADA_SIMULACAO":
        next_steps = []
    elif purchase.status in ("RECUSADA_SIMULACAO", "REVISAO_PENDENTE"):
        if review_protocol:
            next_steps = [f"Protocolo de revisão: {review_protocol}."]
        else:
            next_steps = ["Um analista vai analisar o caso."]
    else:
        next_steps = []

    return {
        "case_id": purchase.case_id,
        "version": purchase.version,
        "status": purchase.status,
        "status_label": _STATUS_LABELS.get(purchase.status, purchase.status),
        "expires_at": expires_at,
        "seconds_remaining": seconds_remaining,
        "allowed_responses": allowed_responses,
        "review_protocol": review_protocol,
        "next_steps": next_steps,
    }
