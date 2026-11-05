"""Testes dos endpoints de revisão (§8 do contrato).

Cobre R05 (bruno 404 em review), criação nova, idempotência, GET /api/reviews analista.
"""
import uuid
import pytest
from fastapi.testclient import TestClient


JUSTIFICATION = "Dados conferidos no detalhe e decisão registrada pela analista."


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
    assert body["case_status"] == "BLOQUEADA_PREVENTIVAMENTE"


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
    assert body["page"] == 1
    assert body["page_size"] == 20
    assert body["total"] >= 1
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


# ---------------------------------------------------------------------------
# Decisão da analista — fecha revisão e muda o estado da compra
# ---------------------------------------------------------------------------

def _create_t007_review(client):
    _login(client, "ana")
    response = client.post("/api/purchases/T-007/review", json={"reason": "OUTRO"})
    assert response.status_code == 201
    review_id = response.json()["review_id"]
    client.delete("/api/session")
    _login(client, "carla")
    return review_id


def test_analyst_can_get_sanitized_review_detail(client):
    review_id = _create_t007_review(client)

    response = client.get(f"/api/reviews/{review_id}")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["review_id"] == review_id
    assert body["purchase"]["case_id"] == "T-007"
    assert len(body["purchase"]["card_last4"]) == 4
    assert "analysis" in body
    assert "timeline" in body
    serialized = response.text
    assert "features_json" not in serialized
    assert "customer_id" not in serialized
    assert "chat" not in serialized.lower()


def test_review_detail_access_and_not_found(client):
    review_id = _create_t007_review(client)
    client.delete("/api/session")
    _login(client, "ana")
    assert client.get(f"/api/reviews/{review_id}").status_code == 403

    client.delete("/api/session")
    _login(client, "carla")
    missing = client.get("/api/reviews/REV-INEXISTENTE")
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.parametrize(
    ("decision", "expected_status"),
    [
        ("AUTHORIZE", "LIBERADA_SIMULACAO"),
        ("DENY", "RECUSADA_SIMULACAO"),
    ],
)
def test_analyst_decision_closes_review_and_updates_purchase(client, decision, expected_status):
    review_id = _create_t007_review(client)

    response = client.post(
        f"/api/reviews/{review_id}/decision",
        json={"decision": decision, "justification": JUSTIFICATION},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["review_status"] == "FECHADA"
    assert body["case_status"] == expected_status
    assert body["justification"] == JUSTIFICATION
    assert body["decided_by"] == "Carla Reis, analista (fictícia)"
    assert body["decided_at"].endswith("Z")
    assert body["simulation"] is True

    # A revisão fechada sai da fila aberta.
    open_ids = {item["review_id"] for item in client.get("/api/reviews").json()["reviews"]}
    assert review_id not in open_ids

    # O associado vê o novo estado da compra.
    client.delete("/api/session")
    _login(client, "ana")
    detail = client.get("/api/purchases/T-007").json()
    assert detail["status"] == expected_status
    assert detail["confirmation"]["allowed_responses"] == []


def test_analyst_decision_records_audit_event(client):
    review_id = _create_t007_review(client)
    response = client.post(
        f"/api/reviews/{review_id}/decision",
        json={"decision": "AUTHORIZE", "justification": JUSTIFICATION},
    )
    assert response.status_code == 200

    from sqlalchemy import select
    from sqlalchemy.orm import Session
    from app.db.session import get_engine
    from app.db.tables.purchases import Event, Purchase, Review

    with Session(get_engine()) as session:
        purchase = session.execute(select(Purchase).where(Purchase.case_id == "T-007")).scalar_one()
        event = session.execute(
            select(Event).where(
                Event.purchase_id == purchase.id,
                Event.event_type == "ANALYST_DECISION",
            )
        ).scalar_one()
        assert event.to_status == "LIBERADA_SIMULACAO"
        assert event.payload["review_id"] == review_id
        assert event.payload["analyst_id"] == "carla"
        assert event.payload["justification"] == JUSTIFICATION
        review = session.execute(select(Review).where(Review.review_id == review_id)).scalar_one()
        assert review.decision == "AUTHORIZE"
        assert review.decision_reason == JUSTIFICATION
        assert review.decided_by == "carla"
        assert review.decided_at is not None


@pytest.mark.parametrize(
    "payload",
    [
        {"decision": "AUTHORIZE"},
        {"decision": "AUTHORIZE", "justification": "curta"},
        {"decision": "DENY", "justification": " " * 20},
        {"decision": "DENY", "justification": "x" * 501},
    ],
)
def test_analyst_decision_requires_valid_justification(client, payload):
    review_id = _create_t007_review(client)
    response = client.post(f"/api/reviews/{review_id}/decision", json=payload)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_REQUEST"


def test_closed_review_cannot_be_decided_twice(client):
    review_id = _create_t007_review(client)
    first = client.post(
        f"/api/reviews/{review_id}/decision",
        json={"decision": "DENY", "justification": JUSTIFICATION},
    )
    assert first.status_code == 200

    second = client.post(
        f"/api/reviews/{review_id}/decision",
        json={"decision": "AUTHORIZE", "justification": JUSTIFICATION},
    )
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "REVIEW_ALREADY_CLOSED"


def test_closed_review_appears_in_filtered_paginated_history(client):
    review_id = _create_t007_review(client)
    decided = client.post(
        f"/api/reviews/{review_id}/decision",
        json={"decision": "DENY", "justification": JUSTIFICATION},
    )
    assert decided.status_code == 200

    history = client.get("/api/reviews?status=FECHADA&decision=DENY&page=1&page_size=1")
    assert history.status_code == 200, history.text
    body = history.json()
    assert body["total"] == 1
    assert body["total_pages"] == 1
    item = body["reviews"][0]
    assert item["review_id"] == review_id
    assert item["decision"] == "DENY"
    assert item["decision_reason"] == JUSTIFICATION
    assert item["decided_by"] == "Carla Reis, analista (fictícia)"
    assert item["decided_at"].endswith("Z")

    no_matches = client.get("/api/reviews?status=FECHADA&decision=AUTHORIZE")
    assert no_matches.status_code == 200
    assert no_matches.json()["total"] == 0
    assert no_matches.json()["reviews"] == []


def test_review_list_rejects_invalid_pagination(client):
    _login(client, "carla")
    response = client.get("/api/reviews?page_size=101")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_REQUEST"


def test_associate_cannot_decide_review(client):
    review_id = _create_t007_review(client)
    client.delete("/api/session")
    _login(client, "ana")

    response = client.post(
        f"/api/reviews/{review_id}/decision",
        json={"decision": "AUTHORIZE", "justification": JUSTIFICATION},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN_ROLE"
