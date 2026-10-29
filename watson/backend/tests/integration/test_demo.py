"""Testes dos endpoints de demonstração (§9 do contrato).

Cobre:
- DEMO_MODE=false → 404 em todas as rotas /api/demo/*
- R01: POST /api/demo/purchases com fraude_supermercado_madrugada → 201, AGUARDANDO_ASSOCIADO,
       challenge_id novo (não CH-007), e após DENY o score ≈ 0.9917 aparece em GET /api/reviews
- R09: falha_modelo → REVISAO_PENDENTE + FALHA_AVALIACAO + score null + warning SCORE_UNAVAILABLE
- R09: modelo indisponível em fixture normal → mesmo comportamento
- Compra nova só aparece na lista de quem a criou (bruno não vê)
- Duas chamadas seguidas geram case_id diferentes
- Reset volta lista da ana a T-007 e T-003 aguardando
- Nenhuma resposta da demo vaza score ou customer_id
"""
import uuid
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Fixtures de infraestrutura
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_path(tmp_path):
    return str(tmp_path / "test.db")


def _make_client(db_path, monkeypatch, *, demo_mode: bool = True):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("DEMO_MODE", "true" if demo_mode else "false")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()
    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture()
def client(db_path, monkeypatch):
    with _make_client(db_path, monkeypatch, demo_mode=True) as c:
        yield c


@pytest.fixture()
def client_no_demo(db_path, monkeypatch):
    with _make_client(db_path, monkeypatch, demo_mode=False) as c:
        yield c


def _login(client, persona_id):
    r = client.post("/api/session", json={"persona_id": persona_id})
    assert r.status_code == 200, r.text


def _login_ana(client):
    _login(client, "ana")


def _login_bruno(client):
    _login(client, "bruno")


def _login_carla(client):
    _login(client, "carla")


# ---------------------------------------------------------------------------
# DEMO_MODE=false → 404
# ---------------------------------------------------------------------------

def test_demo_purchases_without_demo_mode_returns_404(client_no_demo):
    """Sem DEMO_MODE, POST /api/demo/purchases devolve 404."""
    _login_ana(client_no_demo)
    r = client_no_demo.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 404


def test_demo_reset_without_demo_mode_returns_404(client_no_demo):
    """Sem DEMO_MODE, POST /api/demo/reset devolve 404."""
    _login_ana(client_no_demo)
    r = client_no_demo.post("/api/demo/reset")
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# R01: fraude_supermercado_madrugada → 201, AGUARDANDO_ASSOCIADO, challenge_id novo
# ---------------------------------------------------------------------------

def test_r01_demo_purchases_fraude_returns_201_aguardando(client):
    """R01: POST /api/demo/purchases com fraude_supermercado_madrugada devolve 201, AGUARDANDO_ASSOCIADO."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["status"] == "AGUARDANDO_ASSOCIADO"
    assert data["simulation"] is True


def test_r01_demo_challenge_id_is_new(client):
    """R01: challenge_id da compra demo não é CH-007 (não reusa os do seed)."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 201, r.text
    data = r.json()
    challenge_id = data["confirmation"]["challenge_id"]
    assert challenge_id != "CH-007"
    assert challenge_id.startswith("CH-")


def test_r01_demo_case_id_is_new(client):
    """R01: case_id da compra demo não é T-007."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    data = r.json()
    assert data["case_id"] != "T-007"
    assert data["case_id"].startswith("T-")


def test_r01_score_visible_in_reviews_after_deny(client):
    """R01: após DENY na compra demo, GET /api/reviews mostra score ≈ 0.9917."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 201
    data = r.json()
    case_id = data["case_id"]
    challenge_id = data["confirmation"]["challenge_id"]
    version = data["version"]

    # DENY abre revisão PROTECAO
    idempotency_key = str(uuid.uuid4())
    r2 = client.post(
        f"/api/confirmations/{challenge_id}/response",
        json={"response": "DENY", "version": version},
        headers={"Idempotency-Key": idempotency_key},
    )
    assert r2.status_code == 200, r2.text

    # analista vê o score
    _login_carla(client)
    r3 = client.get("/api/reviews")
    assert r3.status_code == 200
    reviews = r3.json()["reviews"]
    # Encontra a revisão da compra demo
    demo_reviews = [rev for rev in reviews if rev["case_id"] == case_id]
    assert len(demo_reviews) >= 1
    analysis = demo_reviews[0]["analysis"]
    assert analysis["score"] is not None
    assert abs(analysis["score"] - 0.9917) < 0.01  # tolerância ~1%


def test_r01_detail_body_matches_get_purchase(client):
    """R01: corpo do 201 é igual ao de GET /api/purchases/{case_id}."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 201
    demo_data = r.json()
    case_id = demo_data["case_id"]

    r2 = client.get(f"/api/purchases/{case_id}")
    assert r2.status_code == 200
    get_data = r2.json()

    # Campos principais batem
    assert demo_data["case_id"] == get_data["case_id"]
    assert demo_data["status"] == get_data["status"]
    assert demo_data["confirmation"]["challenge_id"] == get_data["confirmation"]["challenge_id"]


# ---------------------------------------------------------------------------
# R09: falha_modelo → REVISAO_PENDENTE + FALHA_AVALIACAO + score null + warning
# ---------------------------------------------------------------------------

def test_r09_falha_modelo_fixture_returns_revisao_pendente(client):
    """R09: fixture falha_modelo vai para REVISAO_PENDENTE com FALHA_AVALIACAO."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "falha_modelo"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["status"] == "REVISAO_PENDENTE"
    # warning presente
    assert data.get("warning") == "SCORE_UNAVAILABLE"
    # review com FALHA_AVALIACAO
    assert data["review"] is not None
    assert data["review"]["kind"] == "FALHA_AVALIACAO"


def test_r09_falha_modelo_score_null(client):
    """R09: compra de falha_modelo tem score null em GET /api/reviews."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "falha_modelo"})
    assert r.status_code == 201
    case_id = r.json()["case_id"]

    _login_carla(client)
    r2 = client.get("/api/reviews")
    reviews = r2.json()["reviews"]
    demo_reviews = [rev for rev in reviews if rev["case_id"] == case_id]
    assert len(demo_reviews) >= 1
    assert demo_reviews[0]["analysis"]["score"] is None


def test_r09_model_unavailable_sends_revisao_pendente(client):
    """R09: modelo indisponível (patch que levanta exceção) → REVISAO_PENDENTE + FALHA_AVALIACAO."""
    _login_ana(client)
    with patch("app.domain.cases.intake._score_features", side_effect=Exception("modelo fora")):
        r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["status"] == "REVISAO_PENDENTE"
    assert data.get("warning") == "SCORE_UNAVAILABLE"


def test_r09_confirmation_null_in_revisao_pendente(client):
    """R09: compra em REVISAO_PENDENTE por falha não expõe score."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "falha_modelo"})
    assert r.status_code == 201
    data = r.json()
    # score nunca exposto ao associado
    assert "score" not in str(data.get("purchase", {}))
    assert "score" not in str(data.get("alert", {}))


# ---------------------------------------------------------------------------
# Compra nova aparece só na lista de quem a criou
# ---------------------------------------------------------------------------

def test_demo_purchase_only_visible_to_owner(client):
    """Compra demo da ana não aparece na lista do bruno."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 201
    new_case_id = r.json()["case_id"]

    _login_bruno(client)
    r2 = client.get("/api/purchases")
    ids = [p["case_id"] for p in r2.json()["purchases"]]
    assert new_case_id not in ids


def test_demo_purchase_visible_to_ana(client):
    """Compra demo aparece na lista da própria ana."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    new_case_id = r.json()["case_id"]

    r2 = client.get("/api/purchases")
    ids = [p["case_id"] for p in r2.json()["purchases"]]
    assert new_case_id in ids


# ---------------------------------------------------------------------------
# Duas chamadas seguidas geram case_id diferentes
# ---------------------------------------------------------------------------

def test_two_demo_calls_generate_different_case_ids(client):
    """Duas chamadas POST /api/demo/purchases geram case_id distintos."""
    _login_ana(client)
    r1 = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    r2 = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r1.json()["case_id"] != r2.json()["case_id"]
    assert r1.json()["confirmation"]["challenge_id"] != r2.json()["confirmation"]["challenge_id"]


# ---------------------------------------------------------------------------
# Reset
# ---------------------------------------------------------------------------

def test_demo_reset_returns_204(client):
    """POST /api/demo/reset devolve 204."""
    _login_ana(client)
    r = client.post("/api/demo/reset")
    assert r.status_code == 204


def test_demo_reset_restores_ana_to_t007_and_t003(client):
    """Reset volta a lista da ana a T-007 e T-003 aguardando."""
    _login_ana(client)
    # Cria compra extra
    client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    # Reset
    r = client.post("/api/demo/reset")
    assert r.status_code == 204

    # Lista após reset
    r2 = client.get("/api/purchases")
    ids = [p["case_id"] for p in r2.json()["purchases"]]
    assert "T-007" in ids
    assert "T-003" in ids
    # Não tem compras extras (só as do seed)
    assert len(ids) == 2


def test_demo_reset_requires_session(client):
    """POST /api/demo/reset sem sessão devolve 401."""
    r = client.post("/api/demo/reset")
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# Nenhuma resposta da demo vaza score ou customer_id
# ---------------------------------------------------------------------------

def test_demo_response_does_not_leak_score(client):
    """Nenhuma resposta demo expõe score ou customer_id ao associado."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 201
    body_text = r.text
    assert "analysis_score" not in body_text
    assert "customer_id" not in body_text
    assert "C-ANA" not in body_text


# ---------------------------------------------------------------------------
# fixture_id desconhecido → 400 INVALID_REQUEST
# ---------------------------------------------------------------------------

def test_demo_unknown_fixture_id_returns_400(client):
    """fixture_id desconhecido devolve 400 INVALID_REQUEST."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "nao_existe"})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "INVALID_REQUEST"


# ---------------------------------------------------------------------------
# Somente ASSOCIADO pode criar compra demo
# ---------------------------------------------------------------------------

def test_demo_purchases_requires_associado(client):
    """Carla (ANALISTA) recebe 403 em POST /api/demo/purchases."""
    _login_carla(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 403


def test_demo_purchases_requires_session(client):
    """Sem sessão, POST /api/demo/purchases devolve 401."""
    r = client.post("/api/demo/purchases", json={"fixture_id": "fraude_supermercado_madrugada"})
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# R09: falha_modelo → confirmation null, status e detalhe coerentes, sem linha
#       de confirmação no banco (§5 e §9 do contrato)
# ---------------------------------------------------------------------------

def test_r09_falha_modelo_demo_confirmation_null(client):
    """POST /api/demo/purchases com falha_modelo retorna 201 com confirmation=null."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "falha_modelo"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["status"] == "REVISAO_PENDENTE"
    assert data["confirmation"] is None


def test_r09_falha_modelo_get_detail_confirmation_null(client):
    """GET /api/purchases/{case_id} de compra falha_modelo tem confirmation=null."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "falha_modelo"})
    assert r.status_code == 201
    case_id = r.json()["case_id"]

    r2 = client.get(f"/api/purchases/{case_id}")
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert data["confirmation"] is None


def test_r09_falha_modelo_status_no_confirmation(client):
    """GET /api/purchases/{case_id}/status de compra falha_modelo: expires_at=null,
    seconds_remaining=0, allowed_responses=[]."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "falha_modelo"})
    assert r.status_code == 201
    case_id = r.json()["case_id"]

    r2 = client.get(f"/api/purchases/{case_id}/status")
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert data["expires_at"] is None
    assert data["seconds_remaining"] == 0
    assert data["allowed_responses"] == []


def test_r09_falha_modelo_no_confirmation_row_in_db(client, db_path):
    """Nenhuma linha de confirmações é criada para compra com falha de modelo."""
    _login_ana(client)
    r = client.post("/api/demo/purchases", json={"fixture_id": "falha_modelo"})
    assert r.status_code == 201
    case_id = r.json()["case_id"]

    # Inspeciona o banco via SQLAlchemy direto
    import os
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()
    from sqlalchemy import create_engine, text
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.connect() as conn:
        # Obtém o purchase.id para o case_id criado
        purchase_row = conn.execute(
            text("SELECT id FROM purchases WHERE case_id = :cid"),
            {"cid": case_id},
        ).fetchone()
        assert purchase_row is not None
        purchase_id = purchase_row[0]
        count = conn.execute(
            text("SELECT COUNT(*) FROM confirmations WHERE purchase_id = :pid"),
            {"pid": purchase_id},
        ).scalar()
    assert count == 0, f"Esperado 0 confirmações, encontrado {count}"
