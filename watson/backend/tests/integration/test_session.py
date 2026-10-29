"""Testes dos endpoints de sessão (§4 do contrato).

Cobrem: personas, POST/GET/DELETE /api/session, cookie HttpOnly + SameSite=lax,
persona inexistente, campo extra no corpo, sem cookie, cookie adulterado.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """App com SQLite temporário e SESSION_SECRET definido."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/test.db")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")

    # Reinicializa get_settings e get_engine para o SQLite do teste
    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


# ---------------------------------------------------------------------------
# GET /api/session/personas
# ---------------------------------------------------------------------------

def test_personas_lists_three(client):
    r = client.get("/api/session/personas")
    assert r.status_code == 200
    data = r.json()
    assert data["simulation"] is True
    ids = [p["persona_id"] for p in data["personas"]]
    assert ids == ["ana", "bruno", "carla"]


def test_personas_simulation_true(client):
    r = client.get("/api/session/personas")
    assert r.json()["simulation"] is True


# ---------------------------------------------------------------------------
# POST /api/session
# ---------------------------------------------------------------------------

def test_post_session_ana_returns_200_and_cookie(client):
    r = client.post("/api/session", json={"persona_id": "ana"})
    assert r.status_code == 200
    body = r.json()
    assert body["persona_id"] == "ana"
    assert body["role"] == "ASSOCIADO"
    assert body["simulation"] is True
    # Cookie deve estar presente
    cookie_header = r.headers.get("set-cookie", "")
    assert "raiz_session" in cookie_header


def test_post_session_cookie_httponly_samesite_lax(client):
    r = client.post("/api/session", json={"persona_id": "ana"})
    cookie_header = r.headers.get("set-cookie", "").lower()
    assert "httponly" in cookie_header
    assert "samesite=lax" in cookie_header


def test_post_session_unknown_persona_400(client):
    r = client.post("/api/session", json={"persona_id": "inexistente"})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "INVALID_REQUEST"


def test_post_session_extra_field_customer_id_400(client):
    """corpo com customer_id a mais deve ser rejeitado (§2: identidade nunca no corpo)."""
    r = client.post("/api/session", json={"persona_id": "ana", "customer_id": "C-ANA"})
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# GET /api/session
# ---------------------------------------------------------------------------

def test_get_session_without_cookie_401(client):
    r = client.get("/api/session")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "NOT_AUTHENTICATED"


def test_get_session_with_tampered_cookie_401(client):
    client.cookies.set("raiz_session", "INVALIDO.assinatura.errada")
    r = client.get("/api/session")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "NOT_AUTHENTICATED"


def test_get_session_after_login_200(client):
    client.post("/api/session", json={"persona_id": "ana"})
    r = client.get("/api/session")
    assert r.status_code == 200
    assert r.json()["persona_id"] == "ana"


# ---------------------------------------------------------------------------
# DELETE /api/session
# ---------------------------------------------------------------------------

def test_delete_session_returns_204(client):
    client.post("/api/session", json={"persona_id": "ana"})
    r = client.delete("/api/session")
    assert r.status_code == 204


def test_delete_session_then_get_401(client):
    client.post("/api/session", json={"persona_id": "ana"})
    client.delete("/api/session")
    r = client.get("/api/session")
    assert r.status_code == 401

# ---------------------------------------------------------------------------
# Cookie TimestampSigner expirado deve ser rejeitado; cookie fresco aceito
# ---------------------------------------------------------------------------

def _make_session_cookie(persona_id: str, secret: str, age_seconds: float) -> str:
    """Gera um cookie raiz_session no formato do SessionMiddleware (TimestampSigner).

    Patcha TimestampSigner.get_timestamp para fingir que o cookie foi assinado
    `age_seconds` atrás (sem depender de internals do itsdangerous).
    """
    import json
    import time
    from base64 import b64encode
    from unittest.mock import patch
    from itsdangerous import TimestampSigner

    signer = TimestampSigner(secret)
    payload = b64encode(json.dumps({"persona_id": persona_id}).encode()).decode()
    fake_ts = int(time.time() - age_seconds)
    with patch.object(signer, "get_timestamp", return_value=fake_ts):
        signed = signer.sign(payload)
    return signed.decode()


def test_get_session_with_expired_cookie_401(client):
    """Cookie raiz_session válido mas assinado há 9 h (> 8 h de max_age) → 401."""
    stale = _make_session_cookie("ana", "test-secret-for-session", age_seconds=9 * 3600)
    client.cookies.set("raiz_session", stale)
    r = client.get("/api/session")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "NOT_AUTHENTICATED"


def test_get_session_with_fresh_cookie_200(client):
    """Cookie raiz_session válido e recém-assinado (agora) → 200."""
    fresh = _make_session_cookie("ana", "test-secret-for-session", age_seconds=0)
    client.cookies.set("raiz_session", fresh)
    r = client.get("/api/session")
    assert r.status_code == 200
    assert r.json()["persona_id"] == "ana"
