"""Testes de análise gravada (Item 1): score do modelo local no seed."""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture()
def client(db_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


def _db_session(db_path: str):
    # DATABASE_URL já foi setado pelo monkeypatch do teste que chama esta função
    from app.config import get_settings
    from app.db.session import get_engine
    from sqlalchemy.orm import sessionmaker
    get_settings.cache_clear()
    get_engine.cache_clear()
    engine = get_engine()
    return sessionmaker(bind=engine)()


# ---------------------------------------------------------------------------
# Testes de análise (Item 1)
# ---------------------------------------------------------------------------

def test_t007_score_approximately_0_9917(db_path, client):
    """T-007: score ≈ 0.9917 (tolerância 0.001)."""
    from sqlalchemy import select
    from app.db.tables.purchases import Purchase

    session = _db_session(db_path)
    try:
        p = session.execute(select(Purchase).where(Purchase.case_id == "T-007")).scalar_one()
        if p.analysis_score is None:
            pytest.skip("modelo local não disponível no ambiente de CI")
        assert abs(p.analysis_score - 0.9917) < 0.001, (
            f"score de T-007 esperado ≈ 0.9917, obtido {p.analysis_score}"
        )
        assert p.analysis_score_source == "modelo_local"
        assert p.analysis_model_version is not None
        assert p.analysis_decision == "SOLICITAR_CONFIRMACAO"
        assert p.analysis_policy_version == "confirmacao-v2"
    finally:
        session.close()


def test_t003_score_approximately_0_0089(db_path, client):
    """T-003: score ≈ 0.0089 (tolerância 0.001)."""
    from sqlalchemy import select
    from app.db.tables.purchases import Purchase

    session = _db_session(db_path)
    try:
        p = session.execute(select(Purchase).where(Purchase.case_id == "T-003")).scalar_one()
        if p.analysis_score is None:
            pytest.skip("modelo local não disponível no ambiente de CI")
        assert abs(p.analysis_score - 0.0089) < 0.001, (
            f"score de T-003 esperado ≈ 0.0089, obtido {p.analysis_score}"
        )
    finally:
        session.close()


def test_analysis_score_not_in_associado_routes(client):
    """Score não aparece em nenhuma rota do associado."""
    client.post("/api/session", json={"persona_id": "ana"})
    r_list = client.get("/api/purchases")
    r_detail = client.get("/api/purchases/T-007")
    r_status = client.get("/api/purchases/T-007/status")
    for resp in (r_list, r_detail, r_status):
        assert '"score"' not in resp.text, (
            f"score não deve aparecer em rota do associado: {resp.url}"
        )
        assert "analysis_score" not in resp.text


def test_analysis_null_when_model_fails(db_path, monkeypatch):
    """Se o modelo não carregar, score fica null — nunca inventa."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    # Usa caminho inválido para forçar falha do modelo
    from app.db.tables import Base
    from sqlalchemy.orm import sessionmaker
    engine = get_engine()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        from app.db.seed import run_seed
        run_seed(session, ttl_seconds=900, model_path="/nao/existe/modelo.joblib")

    from sqlalchemy import select
    from app.db.tables.purchases import Purchase
    with Session() as session:
        p = session.execute(select(Purchase).where(Purchase.case_id == "T-007")).scalar_one()
        assert p.analysis_score is None
        assert p.analysis_score_source is None
