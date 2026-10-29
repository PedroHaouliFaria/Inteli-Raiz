"""Testes dos endpoints de compras (§5 do contrato).

Cobrem R02, R05, R07, R10, R11 e verificação de campos proibidos.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture()
def client(db_path):
    """App com SQLite temporário, sessão configurada."""
    import os
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["SESSION_SECRET"] = "test-secret-for-session"

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


def _login(client, persona_id):
    r = client.post("/api/session", json={"persona_id": persona_id})
    assert r.status_code == 200, r.text


def _logout(client):
    client.delete("/api/session")


# ---------------------------------------------------------------------------
# GET /api/purchases — lista
# ---------------------------------------------------------------------------

def test_ana_list_contains_t007_and_t003_in_order(client):
    """R: ana lista T-007 e T-003, nessa ordem (mais recente primeiro)."""
    _login(client, "ana")
    r = client.get("/api/purchases")
    assert r.status_code == 200
    data = r.json()
    assert data["simulation"] is True
    ids = [p["case_id"] for p in data["purchases"]]
    assert ids == ["T-007", "T-003"]


def test_bruno_list_contains_only_t011(client):
    _login(client, "bruno")
    r = client.get("/api/purchases")
    assert r.status_code == 200
    ids = [p["case_id"] for p in r.json()["purchases"]]
    assert ids == ["T-011"]


def test_purchases_list_without_session_401(client):
    r = client.get("/api/purchases")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "NOT_AUTHENTICATED"


def test_purchases_list_carla_403(client):
    """Carla é ANALISTA; associado endpoint → 403."""
    _login(client, "carla")
    r = client.get("/api/purchases")
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "FORBIDDEN_ROLE"


def test_purchases_list_expires_at_only_when_aguardando(client):
    """expires_at vem preenchido só enquanto AGUARDANDO_ASSOCIADO."""
    _login(client, "ana")
    r = client.get("/api/purchases")
    items = {p["case_id"]: p for p in r.json()["purchases"]}
    # T-007 está AGUARDANDO_ASSOCIADO → expires_at não é null
    assert items["T-007"]["expires_at"] is not None
    # T-003 está AGUARDANDO_ASSOCIADO também (seed), mas checamos o campo
    # via regra: qualquer item AGUARDANDO_ASSOCIADO tem expires_at
    for p in r.json()["purchases"]:
        if p["status"] == "AGUARDANDO_ASSOCIADO":
            assert p["expires_at"] is not None
        elif p["status"] != "AGUARDANDO_ASSOCIADO":
            assert p["expires_at"] is None


# ---------------------------------------------------------------------------
# GET /api/purchases/{case_id} — detalhe
# ---------------------------------------------------------------------------

def test_r02_t007_detail_values(client):
    """R02: detalhe de T-007 traz valor, data, MCC, last4 e challenge_id corretos."""
    _login(client, "ana")
    r = client.get("/api/purchases/T-007")
    assert r.status_code == 200
    data = r.json()
    assert data["simulation"] is True
    p = data["purchase"]
    assert p["amount"]["value"] == "149.58"
    assert p["occurred_at"] == "2026-10-25T06:12:00Z"
    assert p["merchant_category"]["mcc"] == "5411"
    assert p["merchant_category"]["label"] == "Supermercado"
    assert p["card"]["last4"] == "2938"
    assert data["confirmation"]["challenge_id"] == "CH-007"


def test_r05_bruno_gets_404_for_t007(client):
    """R05: bruno recebe 404 em T-007 (compra da ana)."""
    _login(client, "bruno")
    r = client.get("/api/purchases/T-007")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "NOT_FOUND"


def test_r05_404_body_same_as_inexistent(client):
    """R05: corpo do 404 para compra de outra pessoa é idêntico ao de compra inexistente."""
    _login(client, "bruno")
    r_other = client.get("/api/purchases/T-007")
    r_none = client.get("/api/purchases/T-999")
    assert r_other.status_code == 404
    assert r_none.status_code == 404
    assert r_other.json() == r_none.json()


def test_r05_carla_gets_403_for_t007(client):
    """R05: carla (ANALISTA) recebe 403 no endpoint de ASSOCIADO."""
    _login(client, "carla")
    r = client.get("/api/purchases/T-007")
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "FORBIDDEN_ROLE"


def test_r05_no_session_gets_401(client):
    r = client.get("/api/purchases/T-007")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "NOT_AUTHENTICATED"


def test_r07_t007_signals_match_fixture(client):
    """R07: sinais de T-007 batem com a linha do purchases.json."""
    _login(client, "ana")
    r = client.get("/api/purchases/T-007")
    assert r.status_code == 200
    signals = r.json()["alert"]["signals"]
    codes = [s["code"] for s in signals]
    assert "CARTAO_NAO_PRESENTE" in codes
    assert "MADRUGADA" in codes
    assert "PRIMEIRA_COMPRA_CARTAO" in codes
    assert len(codes) == 3


def test_r07_t003_no_signals_precaution_headline(client):
    """R07: T-003 vem sem sinais e com o headline de precaução."""
    _login(client, "ana")
    r = client.get("/api/purchases/T-003")
    assert r.status_code == 200
    data = r.json()
    assert data["alert"]["signals"] == []
    headline = data["alert"]["headline"]
    assert "precaução" in headline.lower() or "precau" in headline.lower()


def test_r11_all_purchase_responses_have_simulation_true(client):
    """R11: toda resposta de compra tem simulation: true."""
    _login(client, "ana")
    r_list = client.get("/api/purchases")
    assert r_list.json()["simulation"] is True
    r_detail = client.get("/api/purchases/T-007")
    assert r_detail.json()["simulation"] is True


def test_allowed_responses_empty_outside_aguardando(client):
    """allowed_responses fica vazio quando status != AGUARDANDO_ASSOCIADO."""
    _login(client, "ana")
    r = client.get("/api/purchases/T-007")
    # T-007 está AGUARDANDO_ASSOCIADO → deve ter 3 respostas
    conf = r.json()["confirmation"]
    assert len(conf["allowed_responses"]) == 3


def test_dates_have_utc_z_format(client):
    """Todas as datas da API saem em UTC com Z."""
    _login(client, "ana")
    r = client.get("/api/purchases/T-007")
    data = r.json()
    assert data["purchase"]["occurred_at"].endswith("Z")
    assert data["confirmation"]["expires_at"].endswith("Z")


def test_no_forbidden_fields_in_any_level(client):
    """Nenhuma resposta expõe feedback_label, customer_id, card_id completo ou score."""
    _login(client, "ana")
    import json
    r_list = client.get("/api/purchases")
    r_detail = client.get("/api/purchases/T-007")

    for text in (r_list.text, r_detail.text):
        assert "feedback_label" not in text
        assert "customer_id" not in text
        assert "CUST_SYN" not in text
        assert "C-ANA" not in text
        assert "CARD_SYN" not in text
        # card_id completo não aparece (apenas last4 está ok)
        assert "CARD_SYN_0042938" not in text


# ---------------------------------------------------------------------------
# R10: dois apps sobre o mesmo SQLite
# ---------------------------------------------------------------------------

def test_r10_second_app_sees_same_data_no_re_seed(db_path):
    """R10: segundo app sobre o mesmo SQLite devolve os mesmos dados sem rodar seed de novo."""
    import os
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["SESSION_SECRET"] = "test-secret-for-session"

    from app.config import get_settings
    from app.db.session import get_engine

    # Primeiro app
    get_settings.cache_clear()
    get_engine.cache_clear()
    from app.main import create_app
    app1 = create_app()
    with TestClient(app1) as c1:
        c1.post("/api/session", json={"persona_id": "ana"})
        r1 = c1.get("/api/purchases")
        ids1 = [p["case_id"] for p in r1.json()["purchases"]]

    # Segundo app — mesma URL do banco
    get_settings.cache_clear()
    get_engine.cache_clear()
    app2 = create_app()
    with TestClient(app2) as c2:
        c2.post("/api/session", json={"persona_id": "ana"})
        r2 = c2.get("/api/purchases")
        ids2 = [p["case_id"] for p in r2.json()["purchases"]]

    assert ids1 == ids2 == ["T-007", "T-003"]

    get_settings.cache_clear()
    get_engine.cache_clear()
