"""Recebe e avalia uma compra a partir de uma fixture (§9 do contrato).

Função única usada pelo seed e pelo endpoint POST /api/demo/purchases.
Garante que seed e demo seguem o mesmo caminho: modelo local → sinais → política conservadora.
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.tables.purchases import Confirmation, Event, Purchase, Review
from app.domain.signals.rules import amount_to_cents, card_last4

logger = logging.getLogger(__name__)

# Canais normalizados para o contrato
_CHANNEL_MAP = {
    "cartao_nao_presente": "CARTAO_NAO_PRESENTE",
    "cartao_presente": "CARTAO_PRESENTE",
}


def _now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _next_case_id(session: Session) -> str:
    """Gera T-<n> a partir do próximo int livre acima de 100 (reserva 1–99 para o seed)."""
    count = session.execute(select(func.count()).select_from(Purchase)).scalar() or 0
    # Seed ocupa os IDs fixos; demo começa em T-101
    n = 101 + count
    return f"T-{n}"


def _next_challenge_id(session: Session) -> str:
    count = session.execute(select(func.count()).select_from(Confirmation)).scalar() or 0
    n = 101 + count
    return f"CH-{n}"


def _score_features(features: dict, model_path: str) -> dict:
    """Pontua as features com o modelo local.

    Retorna dict com campos de análise preenchidos, ou campos nulos se o modelo falhar.
    Nunca inventa score.
    """
    try:
        from pathlib import Path
        from app.risk.features import normalize
        from app.risk.models import LocalRiskModel

        model = LocalRiskModel(Path(model_path))
        normalized = normalize(features)
        scores = model.predict([normalized])
        score = scores[0]
        now = _now()
        return {
            "analysis_score": score,
            "analysis_score_source": "modelo_local",
            "analysis_model_version": model.name,
            "analysis_decision": "SOLICITAR_CONFIRMACAO",
            "analysis_policy_version": "confirmacao-v2",
            "analysis_gaps_json": ["Nome do estabelecimento não disponível na base sintética."],
            "analysis_evaluated_at": now,
            "_score_failed": False,
        }
    except Exception as exc:
        logger.warning("Falha ao calcular score: %s", exc)
        return {
            "analysis_score": None,
            "analysis_score_source": None,
            "analysis_model_version": None,
            "analysis_decision": None,
            "analysis_policy_version": "confirmacao-v2",
            "analysis_gaps_json": None,
            "analysis_evaluated_at": None,
            "_score_failed": True,
        }


def receive_and_evaluate_purchase(
    *,
    session: Session,
    fixture: dict,
    customer_id: str,
    ttl_seconds: int,
    model_path: str,
    case_id: str | None = None,
    challenge_id: str | None = None,
    is_seed: bool = False,
) -> tuple[Purchase, Confirmation | None, bool]:
    """Cria compra, roda modelo e aplica política conservadora.

    Política conservadora: todo caso avaliado vai para AGUARDANDO_ASSOCIADO.
    Falha do modelo: REVISAO_PENDENTE + revisão FALHA_AVALIACAO created_by SISTEMA, score null.

    Retorna (purchase, confirmation_or_None, score_failed).
    confirmation é None quando a compra foi para REVISAO_PENDENTE por falha de modelo
    (§5 do contrato: confirmation null quando a política mandou para revisão sem pedir confirmação).
    """
    features: dict = fixture["features"]
    raw_channel = features.get("modalidade_transacao", "cartao_presente")
    channel = _CHANNEL_MAP.get(raw_channel, raw_channel.upper())

    occurred_at = datetime.fromisoformat(fixture["occurred_at"].replace("Z", ""))
    now = _now()

    try:
        analysis = _score_features(features, model_path)
    except Exception as exc:
        logger.warning("Exceção inesperada ao pontuar: %s", exc)
        analysis = {
            "analysis_score": None,
            "analysis_score_source": None,
            "analysis_model_version": None,
            "analysis_decision": None,
            "analysis_policy_version": "confirmacao-v2",
            "analysis_gaps_json": None,
            "analysis_evaluated_at": None,
            "_score_failed": True,
        }
    score_failed = analysis.pop("_score_failed")

    # IDs: usa os fixos (seed) ou gera novos (demo)
    if case_id is None:
        case_id = _next_case_id(session)

    if score_failed:
        # Política de falha: REVISAO_PENDENTE imediatamente; sem confirmação (§5)
        status = "REVISAO_PENDENTE"
    else:
        # Política conservadora: todo caso avaliado → AGUARDANDO_ASSOCIADO
        status = "AGUARDANDO_ASSOCIADO"
        if challenge_id is None:
            challenge_id = _next_challenge_id(session)

    purchase = Purchase(
        case_id=case_id,
        customer_id=customer_id,
        fixture_id=fixture["fixture_id"],
        status=status,
        version=1,
        amount_cents=amount_to_cents(features["amount"]) if "amount" in features else 0,
        currency="BRL",
        occurred_at=occurred_at,
        mcc=features.get("mcc", ""),
        card_brand=features.get("card_brand", ""),
        card_type=features.get("card_type", ""),
        card_last4=card_last4(fixture["card_id"]),
        channel=channel,
        features_json=features,
        created_at=now,
        updated_at=now,
        **{k: v for k, v in analysis.items()},
    )
    session.add(purchase)
    session.flush()  # preenche purchase.id

    # Confirmação criada apenas quando a política solicita confirmação ao associado
    if score_failed:
        confirmation = None
    else:
        confirmation = Confirmation(
            challenge_id=challenge_id,
            purchase_id=purchase.id,
            expires_at=now + timedelta(seconds=ttl_seconds),
        )
        session.add(confirmation)

    if score_failed:
        # Revisão automática por falha do modelo
        from sqlalchemy import func as sa_func
        count = session.execute(select(sa_func.count()).select_from(Review)).scalar() or 0
        today = datetime.now(UTC).strftime("%Y%m%d")
        review = Review(
            review_id=f"REV-{count + 1}",
            purchase_id=purchase.id,
            protocol=f"RZ-{today}-{count + 1:04d}",
            kind="FALHA_AVALIACAO",
            reason="OUTRO",
            status="ABERTA",
            created_by="SISTEMA",
            details="Modelo indisponível ou feature ausente.",
            created_at=now,
        )
        session.add(review)

    event_type = "SEED" if is_seed else "DEMO"
    event = Event(
        purchase_id=purchase.id,
        event_type=event_type,
        payload={"fixture_id": fixture["fixture_id"]},
        created_at=now,
    )
    session.add(event)

    return purchase, confirmation, score_failed
