"""Testes dos endpoints de sessão (§4 do contrato).

Cobrem: personas, POST/GET/DELETE /api/session, cookie HttpOnly + SameSite=lax,
persona inexistente, campo extra no corpo, sem cookie, cookie adulterado.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path):
    """App com SQLite temporário e SESSION_SECRET definido."""
    import os
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp_path}/test.db"
    os.environ["SESSION_SECRET"] = "test-secret-for-session"

    # Reinicializa get_settings e get_engine para o SQLite do teste
    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c

    get_settings.cache_clear()
    get_engine.cache_clear()


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
# Cookie sem timestamp (formato antigo) deve ser rejeitado com 401
# ---------------------------------------------------------------------------

def test_get_session_with_expired_cookie_401(client):
    """Demonstra a vulnerabilidade: um cookie no formato HMAC-sem-timestamp
    gerado pelo middleware antigo é aceito para sempre pelo servidor.

    Com o CookieSessionMiddleware atual → resposta 200 (FALHA esperada).
    Com o SessionMiddleware do starlette → resposta 401 (formato inválido).

    O teste usa _encode_session do middleware antigo para criar o cookie
    diretamente, sem passar pelo login.
    """
    import json
    import hmac as _hmac
    import hashlib
    import base64

    SECRET = "test-secret-for-session"

    def _b64url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

    def _encode_old_session(secret: str, data: dict) -> str:
        """Replica o formato do CookieSessionMiddleware: base64url(json).base64url(hmac)."""
        payload = _b64url_encode(json.dumps(data, separators=(",", ":")).encode())
        sig = _hmac.new(secret.encode(), payload.encode(), hashlib.sha256).digest()
        return f"{payload}.{_b64url_encode(sig)}"

    # Cookie HMAC sem timestamp – válido para sempre no middleware antigo
    stale_cookie = _encode_old_session(SECRET, {"persona_id": "ana"})

    client.cookies.set("raiz_session", stale_cookie)
    r = client.get("/api/session")
    # Deve rejeitar: sem timestamp não há como garantir que a sessão não é antiga.
    assert r.status_code == 401, (
        "VULNERABILIDADE: cookie sem timestamp aceito como sessão válida"
    )
    assert r.json()["error"]["code"] == "NOT_AUTHENTICATED"
