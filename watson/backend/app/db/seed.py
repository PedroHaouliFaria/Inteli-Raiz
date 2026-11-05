"""Seed inicial do banco de dados (§11 do contrato).

Cria cada compra em AGUARDANDO_ASSOCIADO (ou REVISAO_PENDENTE em falha),
a confirmação com prazo de agora + CONFIRMATION_TTL_SECONDS e um evento SEED.
Fixtures com ``seed_review`` também garantem uma revisão demonstrativa idempotente,
inclusive quando a compra já existe em um volume persistente.

Ana e Bruno viram os clientes internos C-ANA e C-BRUNO.

Fixtures com case_id=null são ignoradas pelo seed — entram só pela demo.
"""
from __future__ import annotations

import copy
import json
import logging
import pathlib
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.tables.purchases import Confirmation, Event, Purchase
from app.domain.cases.intake import receive_and_evaluate_purchase

logger = logging.getLogger(__name__)

FIXTURES_PATH = pathlib.Path(__file__).resolve().parents[1] / "fixtures" / "purchases.json"


def _load_fixtures() -> list[dict]:
    with open(FIXTURES_PATH, encoding="utf-8") as fh:
        return json.load(fh)


_EXTRA_SEED_STATUSES = (
    "AGUARDANDO_ASSOCIADO",
    "AGUARDANDO_ASSOCIADO",
    "AGUARDANDO_ASSOCIADO",
    "AGUARDANDO_ASSOCIADO",
    "LIBERADA_SIMULACAO",
    "LIBERADA_SIMULACAO",
    "RECUSADA_SIMULACAO",
    "RECUSADA_SIMULACAO",
    "REVISAO_PENDENTE",
    "REVISAO_PENDENTE",
)


def _expanded_seed_fixtures(fixtures: list[dict]) -> list[dict]:
    """Acrescenta dez compras determinísticas por associado para a demonstração.

    As cópias usam apenas dados sintéticos já presentes nas fixtures. Estados
    encerrados representam respostas fictícias pré-carregadas, nunca decisões da IA.
    """
    expanded = list(fixtures)
    for owner, number_base in (("C-ANA", 100), ("C-BRUNO", 200)):
        templates = [item for item in fixtures if item.get("case_id") and item["owner"] == owner]
        for index, status in enumerate(_EXTRA_SEED_STATUSES, start=1):
            item = copy.deepcopy(templates[(index - 1) % len(templates)])
            number = number_base + index
            item["fixture_id"] = f"volume_demo_{owner.lower().replace('-', '_')}_{index:02d}"
            item["case_id"] = f"T-{number}"
            item["challenge_id"] = f"CH-{number}"
            item["card_id"] = f"CARD_SYN_DEMO_{number:04d}"
            item["seed_status"] = status
            item.pop("seed_review", None)
            occurred_at = datetime.fromisoformat(item["occurred_at"].replace("Z", "+00:00"))
            item["occurred_at"] = (occurred_at - timedelta(days=index)).isoformat().replace("+00:00", "Z")
            if status == "REVISAO_PENDENTE":
                item["seed_review"] = {
                    "reason": "DUVIDA_PROCESSO",
                    "details": "Revisão fictícia pré-carregada para a demonstração.",
                    "created_by": "ASSOCIADO",
                }
            expanded.append(item)
    return expanded


def _refresh_expired_seed_confirmation(
    session: Session,
    purchase: Purchase,
    fixture: dict,
    ttl_seconds: int,
) -> None:
    """Renova somente desafios fictícios vencidos e ainda não respondidos.

    O volume do Docker é persistente, então apenas reiniciar a aplicação não
    recria as fixtures. Sem esta renovação, toda a demonstração fica expirada
    depois do TTL original. Respostas e decisões já tomadas são preservadas.
    """
    confirmation = session.execute(
        select(Confirmation).where(
            Confirmation.challenge_id == fixture["challenge_id"]
        )
    ).scalar_one_or_none()
    if confirmation is None or confirmation.answered_response is not None:
        return

    now = datetime.now(UTC).replace(tzinfo=None)
    expires_at = confirmation.expires_at
    if expires_at.tzinfo is not None:
        expires_at = expires_at.replace(tzinfo=None)
    if expires_at >= now:
        return
    if purchase.status not in {"AGUARDANDO_ASSOCIADO", "CONFIRMACAO_EXPIRADA"}:
        return

    previous_status = purchase.status
    confirmation.expires_at = now + timedelta(seconds=ttl_seconds)
    purchase.status = "AGUARDANDO_ASSOCIADO"
    purchase.version += 1
    purchase.updated_at = now
    session.add(
        Event(
            purchase_id=purchase.id,
            event_type="SEED_REFRESH",
            from_status=previous_status,
            to_status="AGUARDANDO_ASSOCIADO",
            payload={"ttl_seconds": ttl_seconds},
            created_at=now,
        )
    )


def run_seed(session: Session, ttl_seconds: int = 900, model_path: str | None = None) -> None:
    """Cria as fixtures iniciais se o banco estiver vazio. Idempotente.

    Fixtures com case_id=null são puladas (só entram via demo).
    """
    if model_path is None:
        from app.config import get_settings
        model_path = get_settings().risk_model_path

    fixtures = _expanded_seed_fixtures(_load_fixtures())
    for fixture in fixtures:
        # Pula fixtures sem case_id fixo (só demo, ex.: falha_modelo)
        if not fixture.get("case_id"):
            continue

        # Verifica se já existe (idempotência)
        existing = session.execute(
            select(Purchase).where(Purchase.case_id == fixture["case_id"])
        ).scalar_one_or_none()
        if existing is None:
            purchase, confirmation, _ = receive_and_evaluate_purchase(
                session=session,
                fixture=fixture,
                customer_id=fixture["owner"],
                ttl_seconds=ttl_seconds,
                model_path=model_path,
                case_id=fixture["case_id"],
                challenge_id=fixture["challenge_id"],
                is_seed=True,
            )
            seed_status = fixture.get("seed_status")
            if seed_status and seed_status != purchase.status:
                now = datetime.now(UTC).replace(tzinfo=None)
                previous_status = purchase.status
                purchase.status = seed_status
                purchase.version += 1
                purchase.updated_at = now
                if confirmation is not None and seed_status != "AGUARDANDO_ASSOCIADO":
                    confirmation.answered_response = {
                        "LIBERADA_SIMULACAO": "AUTHORIZE",
                        "RECUSADA_SIMULACAO": "DENY",
                        "REVISAO_PENDENTE": "UNSURE",
                    }[seed_status]
                    confirmation.answered_at = now
                session.add(
                    Event(
                        purchase_id=purchase.id,
                        event_type="SEED_STATE",
                        from_status=previous_status,
                        to_status=seed_status,
                        payload={"source": "demo_fixture"},
                        created_at=now,
                    )
                )
        else:
            purchase = existing
            _refresh_expired_seed_confirmation(
                session=session,
                purchase=purchase,
                fixture=fixture,
                ttl_seconds=ttl_seconds,
            )

        review = fixture.get("seed_review")
        if review:
            from app.domain.reviews import create_or_get_review

            create_or_get_review(
                session=session,
                purchase=purchase,
                reason=review["reason"],
                details=review.get("details"),
                created_by=review.get("created_by", "SISTEMA"),
            )

    session.commit()
