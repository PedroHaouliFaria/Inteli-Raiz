"""Seed inicial do banco de dados (§11 do contrato).

Com o banco vazio, cria cada compra em AGUARDANDO_ASSOCIADO (ou REVISAO_PENDENTE em falha),
a confirmação com prazo de agora + CONFIRMATION_TTL_SECONDS e um evento SEED,
numa única transação por fixture.

Ana e Bruno viram os clientes internos C-ANA e C-BRUNO.

Fixtures com case_id=null são ignoradas pelo seed — entram só pela demo.
"""
from __future__ import annotations

import json
import logging
import pathlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.tables.purchases import Purchase
from app.domain.cases.intake import receive_and_evaluate_purchase

logger = logging.getLogger(__name__)

FIXTURES_PATH = pathlib.Path(__file__).resolve().parents[1] / "fixtures" / "purchases.json"


def _load_fixtures() -> list[dict]:
    with open(FIXTURES_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def run_seed(session: Session, ttl_seconds: int = 900, model_path: str | None = None) -> None:
    """Cria as fixtures iniciais se o banco estiver vazio. Idempotente.

    Fixtures com case_id=null são puladas (só entram via demo).
    """
    if model_path is None:
        from app.config import get_settings
        model_path = get_settings().risk_model_path

    fixtures = _load_fixtures()
    for fixture in fixtures:
        # Pula fixtures sem case_id fixo (só demo, ex.: falha_modelo)
        if not fixture.get("case_id"):
            continue

        # Verifica se já existe (idempotência)
        existing = session.execute(
            select(Purchase).where(Purchase.case_id == fixture["case_id"])
        ).scalar_one_or_none()
        if existing is not None:
            continue

        receive_and_evaluate_purchase(
            session=session,
            fixture=fixture,
            customer_id=fixture["owner"],
            ttl_seconds=ttl_seconds,
            model_path=model_path,
            case_id=fixture["case_id"],
            challenge_id=fixture["challenge_id"],
            is_seed=True,
        )

    session.commit()
