"""Seed inicial do banco de dados (§11 do contrato).

Com o banco vazio, cria cada compra em AGUARDANDO_ASSOCIADO, version 1,
a confirmação com prazo de agora + CONFIRMATION_TTL_SECONDS e um evento SEED,
numa única transação por fixture.

Ana e Bruno viram os clientes internos C-ANA e C-BRUNO.
"""
from __future__ import annotations

import json
import logging
import pathlib
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.tables.purchases import Confirmation, Event, Purchase
from app.domain.signals.rules import amount_to_cents, card_last4

logger = logging.getLogger(__name__)

FIXTURES_PATH = pathlib.Path(__file__).resolve().parents[1] / "fixtures" / "purchases.json"

# Canais normalizados para o contrato
_CHANNEL_MAP = {
    "cartao_nao_presente": "CARTAO_NAO_PRESENTE",
    "cartao_presente": "CARTAO_PRESENTE",
}

_CHANNEL_LABELS = {
    "CARTAO_NAO_PRESENTE": "Compra online ou por telefone",
    "CARTAO_PRESENTE": "Compra presencial",
}


def _load_fixtures() -> list[dict]:
    with open(FIXTURES_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _try_score_fixture(features: dict, model_path: str) -> dict:
    """Tenta calcular o score do modelo local. Retorna dict com os campos de análise.

    Se o modelo não carregar ou falhar, retorna campos nulos (nunca inventa score).
    """
    try:
        from pathlib import Path
        from app.risk.features import normalize
        from app.risk.models import LocalRiskModel
        model = LocalRiskModel(Path(model_path))
        normalized = normalize(features)
        scores = model.predict([normalized])
        score = scores[0]
        now = datetime.now(UTC).replace(tzinfo=None)
        return {
            "analysis_score": score,
            "analysis_score_source": "modelo_local",
            "analysis_model_version": model.name,
            "analysis_decision": "SOLICITAR_CONFIRMACAO",
            "analysis_policy_version": "confirmacao-v2",
            "analysis_gaps_json": ["Nome do estabelecimento não disponível na base sintética."],
            "analysis_evaluated_at": now,
        }
    except Exception as exc:
        logger.warning("Falha ao calcular score no seed: %s", exc)
        return {
            "analysis_score": None,
            "analysis_score_source": None,
            "analysis_model_version": None,
            "analysis_decision": None,
            "analysis_policy_version": None,
            "analysis_gaps_json": None,
            "analysis_evaluated_at": None,
        }


def run_seed(session: Session, ttl_seconds: int = 900, model_path: str | None = None) -> None:
    """Cria as fixtures iniciais se o banco estiver vazio. Idempotente."""
    if model_path is None:
        from app.config import get_settings
        model_path = get_settings().risk_model_path

    fixtures = _load_fixtures()
    for fixture in fixtures:
        # Verifica se já existe (idempotência)
        existing = session.execute(
            select(Purchase).where(Purchase.case_id == fixture["case_id"])
        ).scalar_one_or_none()
        if existing is not None:
            continue

        features: dict = fixture["features"]
        raw_channel = features.get("modalidade_transacao", "cartao_presente")
        channel = _CHANNEL_MAP.get(raw_channel, raw_channel.upper())

        occurred_at = datetime.fromisoformat(fixture["occurred_at"].replace("Z", ""))
        now = datetime.now(UTC).replace(tzinfo=None)

        analysis = _try_score_fixture(features, model_path)

        purchase = Purchase(
            case_id=fixture["case_id"],
            customer_id=fixture["owner"],
            fixture_id=fixture["fixture_id"],
            status="AGUARDANDO_ASSOCIADO",
            version=1,
            amount_cents=amount_to_cents(features["amount"]),
            currency="BRL",
            occurred_at=occurred_at,
            mcc=features["mcc"],
            card_brand=features["card_brand"],
            card_type=features["card_type"],
            card_last4=card_last4(fixture["card_id"]),
            channel=channel,
            features_json=features,
            created_at=now,
            updated_at=now,
            **analysis,
        )
        session.add(purchase)
        session.flush()  # preenche purchase.id

        confirmation = Confirmation(
            challenge_id=fixture["challenge_id"],
            purchase_id=purchase.id,
            expires_at=now + timedelta(seconds=ttl_seconds),
        )
        session.add(confirmation)

        event = Event(
            purchase_id=purchase.id,
            event_type="SEED",
            payload={"fixture_id": fixture["fixture_id"]},
            created_at=now,
        )
        session.add(event)

    session.commit()
