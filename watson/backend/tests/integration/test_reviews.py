"""Testes dos endpoints de revisão (§8 do contrato).

Cobre R05 (bruno 404 em review), criação nova, idempotência, GET /api/reviews analista.
"""
import uuid
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


def _login(client, persona_id):
    r = client.post("/api/session", json={"persona_id": persona_id})
    assert r.status_code == 200, r.text


# ---------------------------------------------------------------------------
# R05: bruno recebe 404 em review da compra da ana
# ---------------------------------------------------------------------------

def test_r05_bruno_404_on_review(client):
    """R05: bruno recebe 404 em POST /api/purchases/T-007/review."""
    _login(client, "bruno")
    r = client.post(
        "/api/purchases/T-007/review",
        json={"reason": "OUTRO"},
    )
    assert r.status_code == 404, r.text
    assert r.json()["error"]["code"] == "NOT_FOUND"


# ---------------------------------------------------------------------------
# Criação de revisão nova (201) e idempotência (200)
# ---------------------------------------------------------------------------

def test_create_review_returns_201(client):
    """POST /api/purchases/T-007/review cria revisão com 201."""
    _login(client, "ana")
    r = client.post(
        "/api/purchases/T-007/review",
        json={"reason": "NAO_RECONHECE_ESTABELECIMENTO", "details": "Não sei o nome."},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["simulation"] is True
    assert body["review_id"].startswith("REV-")
    assert body["protocol"].startswith("RZ-")
    assert body["case_id"] == "T-007"
    assert body["kind"] == "DUVIDA"
    assert body["created_by"] == "ASSOCIADO"
    # Revisão NÃO muda o status da compra
    assert body["case_status"] == "AGUARDANDO_ASSOCIADO"


def test_second_review_returns_200_existing(client):
    """Segunda revisão quando já há uma ABERTA retorna 200."""
    _login(client, "ana")
    r1 = client.post("/api/purchases/T-007/review", json={"reason": "OUTRO"})
    assert r1.status_code == 201
    protocol1 = r1.json()["protocol"]

    r2 = client.post("/api/purchases/T-007/review", json={"reason": "VALOR_DIFERENTE"})
    assert r2.status_code == 200, r2.text
    # Deve ser a mesma revisão
    assert r2.json()["protocol"] == protocol1


def test_review_invalid_reason_400(client):
    """reason inválido → 400 INVALID_REQUEST."""
    _login(client, "ana")
    r = client.post("/api/purchases/T-007/review", json={"reason": "INVALIDO"})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "INVALID_REQUEST"


def test_review_requires_session_401(client):
    r = client.post("/api/purchases/T-007/review", json={"reason": "OUTRO"})
    assert r.status_code == 401


def test_review_carla_403(client):
    """Analista chama rota de associado → 403."""
    _login(client, "carla")
    r = client.post("/api/purchases/T-007/review", json={"reason": "OUTRO"})
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# GET /api/reviews — analista
# ---------------------------------------------------------------------------

def test_analista_can_list_reviews(client):
    """Carla (analista) consegue listar revisões."""
    _login(client, "ana")
    client.post("/api/purchases/T-007/review", json={"reason": "OUTRO"})

    # Troca para analista
    client.delete("/api/session")
    _login(client, "carla")
    r = client.get("/api/reviews")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["simulation"] is True
    assert isinstance(body["reviews"], list)
    assert len(body["reviews"]) >= 1
    rev = body["reviews"][0]
    assert "review_id" in rev
    assert "analysis" in rev
    assert "score" in rev["analysis"]


def test_associado_403_on_get_reviews(client):
    """Associado não pode chamar GET /api/reviews → 403 FORBIDDEN_ROLE."""
    _login(client, "ana")
    r = client.get("/api/reviews")
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "FORBIDDEN_ROLE"


def test_get_reviews_unauthenticated_401(client):
    r = client.get("/api/reviews")
    assert r.status_code == 401


def test_reviews_list_includes_analysis(client):
    """GET /api/reviews traz analysis com score (pode ser null se modelo não disponível)."""
    # Cria revisão via DENY (abre PROTECAO)
    _login(client, "ana")
    client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "DENY", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    client.delete("/api/session")
    _login(client, "carla")
    r = client.get("/api/reviews")
    assert r.status_code == 200
    revs = r.json()["reviews"]
    assert len(revs) >= 1
    analysis = revs[0]["analysis"]
    # score pode ser None se modelo não disponível; nunca deve estar ausente
    assert "score" in analysis
    assert "score_source" in analysis
    assert "model_version" in analysis
