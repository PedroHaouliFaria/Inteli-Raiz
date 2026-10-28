"""Testes do seed de banco e das fixtures (§11 do contrato)."""
import json
import os
import tempfile

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.db.tables import Base
from app.db.tables.purchases import Purchase, Confirmation, Event
from app.db.seed import run_seed


@pytest.fixture()
def tmp_session(tmp_path):
    """Sessão SQLite em tmp_path para os testes de seed."""
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


def test_seed_creates_three_purchases(tmp_session):
    run_seed(tmp_session)
    purchases = tmp_session.execute(select(Purchase)).scalars().all()
    assert len(purchases) == 3


def test_seed_is_idempotent(tmp_session):
    """Rodar o seed duas vezes não duplica nada."""
    run_seed(tmp_session)
    run_seed(tmp_session)
    purchases = tmp_session.execute(select(Purchase)).scalars().all()
    assert len(purchases) == 3

    confirmations = tmp_session.execute(select(Confirmation)).scalars().all()
    assert len(confirmations) == 3

    events = tmp_session.execute(select(Event)).scalars().all()
    assert len(events) == 3  # um evento SEED por compra


def test_seed_t007_amount_and_card(tmp_session):
    """T-007 tem amount_cents=14958, card_last4='2938' e os três sinais."""
    run_seed(tmp_session)
    purchase = tmp_session.execute(
        select(Purchase).where(Purchase.case_id == "T-007")
    ).scalar_one()
    assert purchase.amount_cents == 14958
    assert purchase.card_last4 == "2938"
    # sinais ficam em features_json
    features = purchase.features_json
    signals_from_features = _signals_from_features(features)
    codes = [s["code"] for s in signals_from_features]
    assert codes == ["CARTAO_NAO_PRESENTE", "MADRUGADA", "PRIMEIRA_COMPRA_CARTAO"]


def test_seed_t003_and_t011_have_no_signals(tmp_session):
    from app.domain.signals.rules import compute_signals
    run_seed(tmp_session)
    for case_id in ("T-003", "T-011"):
        purchase = tmp_session.execute(
            select(Purchase).where(Purchase.case_id == case_id)
        ).scalar_one()
        signals = compute_signals(purchase.features_json)
        assert signals == [], f"{case_id} não deveria ter sinais"


def test_seed_purchases_status_aguardando(tmp_session):
    run_seed(tmp_session)
    for p in tmp_session.execute(select(Purchase)).scalars().all():
        assert p.status == "AGUARDANDO_ASSOCIADO"
        assert p.version == 1


def test_seed_confirmations_have_ttl(tmp_session):
    from datetime import UTC, datetime
    run_seed(tmp_session)
    now_naive = datetime.now(UTC).replace(tzinfo=None)
    for c in tmp_session.execute(select(Confirmation)).scalars().all():
        assert c.expires_at > now_naive


def test_purchases_json_no_forbidden_fields(tmp_path):
    """O purchases.json não tem feedback_label, customer_id nem 'CUST_SYN'."""
    fixtures_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "app", "fixtures", "purchases.json"
    )
    if not os.path.exists(fixtures_path):
        pytest.skip("purchases.json ainda não gerado")
    with open(fixtures_path) as f:
        content = f.read()
    assert "feedback_label" not in content
    assert "customer_id" not in content
    assert "CUST_SYN" not in content


def _signals_from_features(features: dict) -> list:
    """Extrai sinais computados das features para verificação."""
    from app.domain.signals.rules import compute_signals
    return [{"code": s.code, "label": s.label, "source": s.source}
            for s in compute_signals(features)]
