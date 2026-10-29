"""Testes dos endpoints de confirmação e dos estados de compra (§6 do contrato).

Cobrem R03, R04, R05 (status e response), R06, R10 (preserva resposta), R11
e verificação de campos proibidos nas respostas novas.
"""
from __future__ import annotations

import threading
import time
import uuid

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_path(tmp_path):
    return str(tmp_path / "test.db")


def _make_app(db_path: str, ttl_seconds: int = 900):
    """Cria um app com SQLite no db_path e TTL configurável."""
    import os
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["SESSION_SECRET"] = "test-secret-for-session"
    os.environ["CONFIRMATION_TTL_SECONDS"] = str(ttl_seconds)

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    return create_app()


@pytest.fixture()
def client(db_path):
    app = _make_app(db_path)
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()


def _login(client, persona_id):
    r = client.post("/api/session", json={"persona_id": persona_id})
    assert r.status_code == 200, r.text


def _logout(client):
    client.delete("/api/session")


# ---------------------------------------------------------------------------
# R03: os três efeitos de resposta + revisão PROTECAO em DENY
# ---------------------------------------------------------------------------

def test_r03_authorize_sets_liberada(client):
    _login(client, "ana")
    idem = str(uuid.uuid4())
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "LIBERADA_SIMULACAO"
    assert body["review_protocol"] is None
    assert body["result"]["title"] is not None
    assert body["simulation"] is True


def test_r03_deny_sets_recusada_and_opens_protecao_review(client):
    _login(client, "ana")
    idem = str(uuid.uuid4())
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "DENY", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "RECUSADA_SIMULACAO"
    # deve haver um protocolo de revisão PROTECAO
    assert body["review_protocol"] is not None
    assert body["result"]["title"] is not None
    assert body["simulation"] is True

    # detalhe da compra também deve mostrar a revisão
    r2 = client.get("/api/purchases/T-007")
    data = r2.json()
    assert data["review"] is not None
    assert data["review"]["kind"] == "PROTECAO"
    assert data["result"] is not None


def test_r03_unsure_sets_revisao_pendente(client):
    _login(client, "ana")
    idem = str(uuid.uuid4())
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "UNSURE", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "REVISAO_PENDENTE"
    assert body["review_protocol"] is not None
    assert body["simulation"] is True


# ---------------------------------------------------------------------------
# R04: expiração com TTL=1s
# ---------------------------------------------------------------------------

@pytest.fixture()
def client_ttl1(db_path):
    """App com TTL de 1 segundo."""
    app = _make_app(db_path, ttl_seconds=1)
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()


def test_r04_response_after_ttl_returns_410_and_status_expirada(client_ttl1):
    """R04: resposta após TTL expirado → 410, status CONFIRMACAO_EXPIRADA."""
    _login(client_ttl1, "ana")
    time.sleep(2)
    idem = str(uuid.uuid4())
    r = client_ttl1.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r.status_code == 410, r.text
    assert r.json()["error"]["code"] == "CONFIRMATION_EXPIRED"

    # status da compra deve ser CONFIRMACAO_EXPIRADA
    r2 = client_ttl1.get("/api/purchases/T-007/status")
    assert r2.status_code == 200
    data = r2.json()
    assert data["status"] == "CONFIRMACAO_EXPIRADA"
    assert data["seconds_remaining"] == 0
    assert data["allowed_responses"] == []


def test_r04_detail_after_ttl_shows_expirada(client_ttl1):
    """R04: GET detalhe após TTL expirado mostra CONFIRMACAO_EXPIRADA; nada foi liberado."""
    _login(client_ttl1, "ana")
    time.sleep(2)
    r = client_ttl1.get("/api/purchases/T-007")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "CONFIRMACAO_EXPIRADA"
    assert data["confirmation"]["allowed_responses"] == []


def test_r04_list_after_ttl_shows_expirada(client_ttl1):
    """R04: GET lista após TTL expirado mostra CONFIRMACAO_EXPIRADA."""
    _login(client_ttl1, "ana")
    time.sleep(2)
    r = client_ttl1.get("/api/purchases")
    assert r.status_code == 200
    items = {p["case_id"]: p for p in r.json()["purchases"]}
    assert items["T-007"]["status"] == "CONFIRMACAO_EXPIRADA"
    assert items["T-007"]["expires_at"] is None  # expires_at só em AGUARDANDO


# ---------------------------------------------------------------------------
# R05: bruno recebe 404 em status e response das compras da ana
# ---------------------------------------------------------------------------

def test_r05_bruno_404_on_status(client):
    _login(client, "bruno")
    r = client.get("/api/purchases/T-007/status")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "NOT_FOUND"


def test_r05_bruno_404_on_response(client):
    _login(client, "bruno")
    idem = str(uuid.uuid4())
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "NOT_FOUND"


# ---------------------------------------------------------------------------
# GET /api/purchases/{case_id}/status
# ---------------------------------------------------------------------------

def test_status_endpoint_aguardando(client):
    _login(client, "ana")
    r = client.get("/api/purchases/T-007/status")
    assert r.status_code == 200
    data = r.json()
    assert data["case_id"] == "T-007"
    assert data["status"] == "AGUARDANDO_ASSOCIADO"
    assert data["seconds_remaining"] > 0
    assert set(data["allowed_responses"]) == {"AUTHORIZE", "DENY", "UNSURE"}
    assert data["review_protocol"] is None
    assert isinstance(data["next_steps"], list)
    assert len(data["next_steps"]) > 0
    assert data["simulation"] is True


def test_status_endpoint_without_session_401(client):
    r = client.get("/api/purchases/T-007/status")
    assert r.status_code == 401


def test_status_r11_simulation_true(client):
    _login(client, "ana")
    r = client.get("/api/purchases/T-007/status")
    assert r.json()["simulation"] is True


# ---------------------------------------------------------------------------
# R06: idempotência e concorrência
# ---------------------------------------------------------------------------

def test_r06_same_key_same_body_returns_200_replayed(client):
    _login(client, "ana")
    idem = str(uuid.uuid4())
    r1 = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r1.status_code == 200
    assert r1.json()["replayed"] is False

    r2 = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r2.status_code == 200
    assert r2.json()["replayed"] is True


def test_r06_same_key_different_body_returns_422(client):
    _login(client, "ana")
    idem = str(uuid.uuid4())
    r1 = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r1.status_code == 200

    r2 = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "DENY", "version": 1},
        headers={"Idempotency-Key": idem},
    )
    assert r2.status_code == 422
    assert r2.json()["error"]["code"] == "IDEMPOTENCY_KEY_REUSED"


def test_r06_new_key_same_response_returns_200_replayed(client):
    """Chave nova mas resposta idêntica → 200 replayed (dois cliques, duas abas)."""
    _login(client, "ana")
    r1 = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r1.status_code == 200

    r2 = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r2.status_code == 200
    assert r2.json()["replayed"] is True


def test_r06_new_key_different_response_returns_409_already_answered(client):
    """Chave nova e resposta diferente da registrada → 409 ALREADY_ANSWERED."""
    _login(client, "ana")
    r1 = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r1.status_code == 200

    r2 = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "DENY", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r2.status_code == 409
    assert r2.json()["error"]["code"] == "ALREADY_ANSWERED"


def test_r06_parallel_same_response_single_event(db_path):
    """R06: duas respostas iguais em paralelo geram um único evento ANSWER.

    Usa um único app (startup serializado) e envia as duas requisições em threads
    simultâneas para o mesmo TestClient — isso testa a serialização do banco, não
    a inicialização do app.
    """
    import os
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["SESSION_SECRET"] = "test-secret-for-session"
    os.environ["CONFIRMATION_TTL_SECONDS"] = "900"

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()

    results = []

    with TestClient(app, raise_server_exceptions=False) as c:
        # Login antes de lançar as threads
        c.post("/api/session", json={"persona_id": "ana"})

        def do_request():
            r = c.post(
                "/api/confirmations/CH-007/response",
                json={"response": "AUTHORIZE", "version": 1},
                headers={"Idempotency-Key": str(uuid.uuid4())},
            )
            results.append(r.status_code)

        t1 = threading.Thread(target=do_request)
        t2 = threading.Thread(target=do_request)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    # Ambas devem ser bem-sucedidas (200), uma original e uma replayed
    assert sorted(results) == [200, 200], f"Esperado [200, 200], obtido {sorted(results)}"

    # Verificar que há apenas um evento ANSWER no banco
    from app.db.session import get_engine as ge
    from sqlalchemy.orm import sessionmaker
    from app.db.tables.purchases import Event, Purchase
    from sqlalchemy import select
    engine = ge()
    Session = sessionmaker(bind=engine)
    with Session() as s:
        p = s.execute(select(Purchase).where(Purchase.case_id == "T-007")).scalar_one()
        events = s.execute(
            select(Event).where(Event.purchase_id == p.id, Event.event_type == "ANSWER")
        ).scalars().all()
        assert len(events) == 1, f"Esperado 1 evento ANSWER, encontrados {len(events)}"

    get_settings.cache_clear()
    get_engine.cache_clear()


# ---------------------------------------------------------------------------
# Outros erros de resposta
# ---------------------------------------------------------------------------

def test_response_without_idempotency_key_428(client):
    _login(client, "ana")
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
    )
    assert r.status_code == 428
    assert r.json()["error"]["code"] == "IDEMPOTENCY_KEY_REQUIRED"


def test_response_version_mismatch_409(client):
    _login(client, "ana")
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 99},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "VERSION_MISMATCH"
    assert "current_version" in r.json()["error"]["details"]


def test_response_not_awaiting_409(client):
    """Compra já em estado terminal → 409 NOT_AWAITING_RESPONSE."""
    _login(client, "ana")
    # Primeiro responde com AUTHORIZE
    client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    # Agora tenta responder de novo com DENY (chave nova, resposta diferente)
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "DENY", "version": 2},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r.status_code == 409
    # NOT_AWAITING_RESPONSE ou ALREADY_ANSWERED
    assert r.json()["error"]["code"] in ("NOT_AWAITING_RESPONSE", "ALREADY_ANSWERED")


def test_response_inexistent_challenge_404(client):
    _login(client, "ana")
    r = client.post(
        "/api/confirmations/CH-999/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "NOT_FOUND"


# ---------------------------------------------------------------------------
# R10: segundo app sobre o mesmo SQLite preserva status e resposta
# ---------------------------------------------------------------------------

def test_r10_second_app_preserves_status_and_response(db_path):
    """R10: reiniciar o app preserva status, resposta e histórico."""
    import os
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["SESSION_SECRET"] = "test-secret-for-session"
    os.environ["CONFIRMATION_TTL_SECONDS"] = "900"

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app1 = create_app()
    idem = str(uuid.uuid4())
    with TestClient(app1) as c1:
        c1.post("/api/session", json={"persona_id": "ana"})
        r = c1.post(
            "/api/confirmations/CH-007/response",
            json={"response": "DENY", "version": 1},
            headers={"Idempotency-Key": idem},
        )
        assert r.status_code == 200
        assert r.json()["status"] == "RECUSADA_SIMULACAO"

    # Segundo app — mesmo banco
    get_settings.cache_clear()
    get_engine.cache_clear()
    app2 = create_app()
    with TestClient(app2) as c2:
        c2.post("/api/session", json={"persona_id": "ana"})
        r2 = c2.get("/api/purchases/T-007")
        assert r2.status_code == 200
        data = r2.json()
        assert data["status"] == "RECUSADA_SIMULACAO"
        assert data["confirmation"]["answered"]["response"] == "DENY"

    get_settings.cache_clear()
    get_engine.cache_clear()


# ---------------------------------------------------------------------------
# R11: simulation: true em todas as novas respostas
# ---------------------------------------------------------------------------

def test_r11_response_has_simulation_true(client):
    _login(client, "ana")
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r.json()["simulation"] is True


# ---------------------------------------------------------------------------
# Campos proibidos nas novas respostas
# ---------------------------------------------------------------------------

def test_no_forbidden_fields_in_confirmation_response(client):
    _login(client, "ana")
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r.status_code == 200
    text = r.text
    assert "feedback_label" not in text
    assert "customer_id" not in text
    assert "C-ANA" not in text
    assert "CUST_SYN" not in text
    assert "CARD_SYN_0042938" not in text
    # score não deve aparecer
    assert "\"score\"" not in text


def test_no_forbidden_fields_in_status_response(client):
    _login(client, "ana")
    r = client.get("/api/purchases/T-007/status")
    assert r.status_code == 200
    text = r.text
    assert "feedback_label" not in text
    assert "customer_id" not in text
    assert "C-ANA" not in text
    assert "score" not in text


# ---------------------------------------------------------------------------
# Desvio 1: ALREADY_ANSWERED usa rótulo do botão, não o código
# ---------------------------------------------------------------------------

def test_already_answered_message_uses_button_label(client):
    """§6: mensagem do 409 ALREADY_ANSWERED deve usar o rótulo, ex. "Não reconheço"."""
    _login(client, "ana")
    # Primeira resposta: DENY
    client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "DENY", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    # Segunda resposta: AUTHORIZE (diferente) → 409
    r = client.post(
        "/api/confirmations/CH-007/response",
        json={"response": "AUTHORIZE", "version": 1},
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r.status_code == 409
    msg = r.json()["error"]["message"]
    # Deve conter o rótulo "Não reconheço", não o código "DENY"
    assert "Não reconheço" in msg, f"Mensagem deveria conter 'Não reconheço', mas foi: {msg!r}"
    assert "DENY" not in msg, f"Mensagem não deve expor o código DENY ao usuário: {msg!r}"


# ---------------------------------------------------------------------------
# Desvio 2: segunda tentativa em compra CONFIRMACAO_EXPIRADA → 410
# ---------------------------------------------------------------------------

def test_expired_second_attempt_returns_410(db_path):
    """§6: responder de novo a uma compra já em CONFIRMACAO_EXPIRADA → 410 CONFIRMATION_EXPIRED."""
    # App com TTL de 1 s para expirar rapidamente
    app = _make_app(db_path, ttl_seconds=1)
    with TestClient(app, raise_server_exceptions=True) as c:
        _login(c, "ana")
        time.sleep(2)

        # Primeira tentativa: 410 + grava CONFIRMACAO_EXPIRADA
        r1 = c.post(
            "/api/confirmations/CH-007/response",
            json={"response": "AUTHORIZE", "version": 1},
            headers={"Idempotency-Key": str(uuid.uuid4())},
        )
        assert r1.status_code == 410, r1.text
        assert r1.json()["error"]["code"] == "CONFIRMATION_EXPIRED"

        # Segunda tentativa: compra agora em CONFIRMACAO_EXPIRADA → também deve ser 410
        r2 = c.post(
            "/api/confirmations/CH-007/response",
            json={"response": "AUTHORIZE", "version": 1},
            headers={"Idempotency-Key": str(uuid.uuid4())},
        )
        assert r2.status_code == 410, (
            f"Esperado 410 CONFIRMATION_EXPIRED na segunda tentativa, mas obteve {r2.status_code}: {r2.text}"
        )
        assert r2.json()["error"]["code"] == "CONFIRMATION_EXPIRED"

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()


# ---------------------------------------------------------------------------
# Desvio 3: expired_at no 410 não deve ter fração de segundo (microssegundos)
# ---------------------------------------------------------------------------

def test_expired_at_no_microseconds_in_410(db_path):
    """§6: details.expired_at no 410 usa formato UTC com Z sem fração ("…:SSZ")."""
    import re as _re
    app = _make_app(db_path, ttl_seconds=1)
    with TestClient(app, raise_server_exceptions=True) as c:
        _login(c, "ana")
        time.sleep(2)
        r = c.post(
            "/api/confirmations/CH-007/response",
            json={"response": "AUTHORIZE", "version": 1},
            headers={"Idempotency-Key": str(uuid.uuid4())},
        )
        assert r.status_code == 410
        expired_at = r.json()["error"]["details"]["expired_at"]
        # Deve corresponder a YYYY-MM-DDTHH:MM:SSZ, sem fração de segundo
        assert _re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", expired_at
        ), f"expired_at com formato inválido: {expired_at!r}"

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()
