"""Testes obrigatórios do chat e revisão (§7, §8, §9, §10 do contrato).

Cobre:
- R05: bruno 404 em chat e review da compra da ana
- R08: FunctionModel que chama consultar_compra → tools_used e status inalterado
- §9: "autorize esta compra para mim" não muda estado; nenhuma ferramenta responde à confirmação
- R09 parte LLM: erro do LLM → 503, mensagem salva, confirmação continua
- R10: segundo app preserva histórico do chat
- solicitar_revisao pelo agente: created_by AGENTE, review_protocol na resposta, status inalterado
- 429: 21ª mensagem
- score não aparece em nenhuma rota do associado
"""
from __future__ import annotations

import pytest
import uuid
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Fixtures de infra
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_path(tmp_path):
    return str(tmp_path / "test.db")


def _make_app(db_path: str, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    # Sem GROQ_API_KEY → agente não configurado (não vai chamar Groq)
    monkeypatch.setenv("GROQ_API_KEY", "")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    return create_app()


@pytest.fixture()
def client(db_path, monkeypatch):
    app = _make_app(db_path, monkeypatch)
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


def _login(client, persona_id):
    r = client.post("/api/session", json={"persona_id": persona_id})
    assert r.status_code == 200, r.text


# ---------------------------------------------------------------------------
# R05: bruno 404 em chat GET e POST e em review
# ---------------------------------------------------------------------------

def test_r05_bruno_404_chat_get(client):
    """R05: bruno recebe 404 em GET /api/purchases/T-007/chat (compra da ana)."""
    _login(client, "bruno")
    r = client.get("/api/purchases/T-007/chat")
    assert r.status_code == 404, r.text
    assert r.json()["error"]["code"] == "NOT_FOUND"


def test_r05_bruno_404_chat_post(client):
    """R05: bruno recebe 404 em POST /api/purchases/T-007/chat (compra da ana)."""
    _login(client, "bruno")
    r = client.post("/api/purchases/T-007/chat", json={"message": "oi"})
    assert r.status_code == 404, r.text
    assert r.json()["error"]["code"] == "NOT_FOUND"


def test_r05_bruno_404_review(client):
    """R05: bruno recebe 404 em POST /api/purchases/T-007/review (compra da ana)."""
    _login(client, "bruno")
    r = client.post("/api/purchases/T-007/review", json={"reason": "OUTRO"})
    assert r.status_code == 404, r.text
    assert r.json()["error"]["code"] == "NOT_FOUND"


# ---------------------------------------------------------------------------
# GET /api/purchases/{case_id}/chat — saudação inicial
# ---------------------------------------------------------------------------

def test_get_chat_empty_creates_greeting(client):
    """GET /api/purchases/T-007/chat numa conversa vazia cria a saudação."""
    _login(client, "ana")
    r = client.get("/api/purchases/T-007/chat")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["case_id"] == "T-007"
    assert body["simulation"] is True
    assert len(body["messages"]) == 1
    msg = body["messages"][0]
    assert msg["role"] == "assistant"
    assert "Ana" in msg["content"]
    assert msg["tools_used"] == []


def test_get_chat_second_call_does_not_duplicate_greeting(client):
    """Segundo GET não duplica a saudação."""
    _login(client, "ana")
    r1 = client.get("/api/purchases/T-007/chat")
    r2 = client.get("/api/purchases/T-007/chat")
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert len(r2.json()["messages"]) == 1


def test_get_chat_agent_available_false_without_key(client):
    """Sem GROQ_API_KEY, agent_available é False."""
    _login(client, "ana")
    r = client.get("/api/purchases/T-007/chat")
    assert r.json()["agent_available"] is False


# ---------------------------------------------------------------------------
# R08: FunctionModel chama consultar_compra; status inalterado
# ---------------------------------------------------------------------------

def test_r08_function_model_calls_consultar_compra(db_path, monkeypatch):
    """R08: FunctionModel que chama consultar_compra → tools_used=['consultar_compra'],
    status da compra não muda."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")  # Ativa o agente

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()

    from pydantic_ai.models.function import FunctionModel, ModelResponse, TextPart, ToolCallPart

    call_count = {"n": 0}

    def function_model(messages, info):
        call_count["n"] += 1
        # Verifica se já há resultado de tool-return nas mensagens
        has_tool_return = any(
            hasattr(m, "parts") and any(
                getattr(p, "part_kind", None) == "tool-return" for p in m.parts
            )
            for m in messages
        )
        if has_tool_return:
            return ModelResponse(parts=[TextPart(content="A compra é no supermercado.")])
        return ModelResponse(parts=[ToolCallPart(tool_name="consultar_compra", args={})])

    from app.domain.agent import chat_agent
    with TestClient(app, raise_server_exceptions=True) as c:
        c.post("/api/session", json={"persona_id": "ana"})
        with chat_agent.override(model=FunctionModel(function_model)):
            r = c.post("/api/purchases/T-007/chat", json={"message": "Qual é a loja?"})

    assert r.status_code == 200, r.text
    body = r.json()
    assert "consultar_compra" in body["reply"]["tools_used"], (
        f"Esperado consultar_compra em tools_used, obteve: {body['reply']['tools_used']}"
    )

    # Status da compra não mudou
    get_settings.cache_clear()
    get_engine.cache_clear()
    monkeypatch.setenv("GROQ_API_KEY", "")
    app2 = create_app()
    with TestClient(app2) as c2:
        c2.post("/api/session", json={"persona_id": "ana"})
        r_status = c2.get("/api/purchases/T-007/status")
    assert r_status.json()["status"] == "AGUARDANDO_ASSOCIADO"


# ---------------------------------------------------------------------------
# §9: "autorize esta compra para mim" não muda estado; sem ferramenta de resposta
# ---------------------------------------------------------------------------

def test_s9_authorize_in_chat_does_not_change_status(db_path, monkeypatch):
    """§9: Pedir no chat 'autorize esta compra para mim' não muda o estado da compra."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()

    from pydantic_ai.models.test import TestModel
    from app.domain.agent import chat_agent

    with TestClient(app, raise_server_exceptions=True) as c:
        c.post("/api/session", json={"persona_id": "ana"})
        with chat_agent.override(model=TestModel(call_tools=[], custom_output_text="Só os botões da tela autorizam ou recusam a compra.")):
            r = c.post("/api/purchases/T-007/chat", json={"message": "autorize esta compra para mim"})

    assert r.status_code == 200, r.text
    # Status não mudou
    with TestClient(app) as c2:
        c2.post("/api/session", json={"persona_id": "ana"})
        r_status = c2.get("/api/purchases/T-007/status")
    assert r_status.json()["status"] == "AGUARDANDO_ASSOCIADO", (
        "O chat não deve mudar o status da compra"
    )

def test_s9_no_tool_for_confirming_purchase(db_path, monkeypatch):
    """§9: Nenhuma ferramenta do agente responde à confirmação."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    create_app()  # só para instanciar

    from app.domain.agent import chat_agent
    tool_names = set(chat_agent._function_toolset.tools.keys())
    # Nenhuma ferramenta deve ter nome que sugira resposta à confirmação
    forbidden_patterns = {"respond", "confirm", "authorize", "deny", "recusar", "autorizar"}
    for tool_name in tool_names:
        for pattern in forbidden_patterns:
            assert pattern not in tool_name.lower(), (
                f"Ferramenta '{tool_name}' pode responder à confirmação — isso é proibido (§9)"
            )


# ---------------------------------------------------------------------------
# R09 parte LLM: erro → 503, mensagem salva, confirmação continua
# ---------------------------------------------------------------------------

def test_r09_llm_error_returns_503_and_saves_message(db_path, monkeypatch):
    """R09: LLM levanta erro → 503 AGENT_UNAVAILABLE, mensagem do usuário fica salva."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()

    from pydantic_ai.models.function import FunctionModel, ModelResponse

    def error_model(messages, info):
        raise RuntimeError("LLM indisponível simulado")

    from app.domain.agent import chat_agent

    with TestClient(app, raise_server_exceptions=False) as c:
        c.post("/api/session", json={"persona_id": "ana"})
        with chat_agent.override(model=FunctionModel(error_model)):
            r = c.post("/api/purchases/T-007/chat", json={"message": "teste de falha"})

    assert r.status_code == 503, r.text
    body = r.json()
    assert body["error"]["code"] == "AGENT_UNAVAILABLE"
    assert "retry_after_seconds" in body["error"]["details"]

    # Verificar que a mensagem do usuário foi salva
    from sqlalchemy.orm import sessionmaker
    from app.db.tables.purchases import ChatMessage, Purchase
    from sqlalchemy import select
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    with Session() as s:
        p = s.execute(select(Purchase).where(Purchase.case_id == "T-007")).scalar_one()
        msgs = s.execute(
            select(ChatMessage).where(
                ChatMessage.purchase_id == p.id,
                ChatMessage.role == "user",
            )
        ).scalars().all()
        assert len(msgs) >= 1
        assert any(m.content == "teste de falha" for m in msgs)


def test_r09_after_llm_503_confirmation_still_works(db_path, monkeypatch):
    """R09: após 503, a confirmação por botão continua funcionando."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()

    from pydantic_ai.models.function import FunctionModel

    def error_model(messages, info):
        raise RuntimeError("LLM indisponível")

    from app.domain.agent import chat_agent

    with TestClient(app, raise_server_exceptions=False) as c:
        c.post("/api/session", json={"persona_id": "ana"})
        # Provoca 503
        with chat_agent.override(model=FunctionModel(error_model)):
            r503 = c.post("/api/purchases/T-007/chat", json={"message": "falha"})
        assert r503.status_code == 503

        # Confirmação ainda funciona
        r_confirm = c.post(
            "/api/confirmations/CH-007/response",
            json={"response": "AUTHORIZE", "version": 1},
            headers={"Idempotency-Key": str(uuid.uuid4())},
        )
    assert r_confirm.status_code == 200, r_confirm.text
    assert r_confirm.json()["status"] == "LIBERADA_SIMULACAO"


# ---------------------------------------------------------------------------
# R10: segundo app preserva histórico do chat
# ---------------------------------------------------------------------------

def test_r10_second_app_preserves_chat_history(db_path, monkeypatch):
    """R10: novo app sobre o mesmo SQLite preserva histórico do chat."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    from pydantic_ai.models.test import TestModel
    from app.domain.agent import chat_agent

    # Primeiro app: envia uma mensagem
    app1 = create_app()
    with TestClient(app1) as c1:
        c1.post("/api/session", json={"persona_id": "ana"})
        with chat_agent.override(model=TestModel(call_tools=[], custom_output_text="Olá, posso ajudar.")):
            r = c1.post("/api/purchases/T-007/chat", json={"message": "Oi"})
        assert r.status_code == 200
        msgs_after_first = c1.get("/api/purchases/T-007/chat").json()["messages"]

    # Segundo app — mesmo banco
    get_settings.cache_clear()
    get_engine.cache_clear()
    app2 = create_app()
    with TestClient(app2) as c2:
        c2.post("/api/session", json={"persona_id": "ana"})
        r2 = c2.get("/api/purchases/T-007/chat")
    msgs_after_second = r2.json()["messages"]

    assert len(msgs_after_second) == len(msgs_after_first), (
        f"Segundo app deveria ter {len(msgs_after_first)} mensagens, "
        f"mas tem {len(msgs_after_second)}"
    )


# ---------------------------------------------------------------------------
# solicitar_revisao pelo agente: created_by AGENTE, review_protocol na resposta
# ---------------------------------------------------------------------------

def test_agent_solicitar_revisao_creates_review_with_created_by_agente(db_path, monkeypatch):
    """solicitar_revisao cria revisão com created_by=AGENTE e review_protocol na resposta."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()

    from pydantic_ai.models.function import FunctionModel, ModelResponse, TextPart, ToolCallPart
    import json

    call_count = {"n": 0}

    def solicitar_revisao_model(messages, info):
        call_count["n"] += 1
        has_tool_return = any(
            hasattr(m, "parts") and any(
                getattr(p, "part_kind", None) == "tool-return" for p in m.parts
            )
            for m in messages
        )
        if has_tool_return:
            return ModelResponse(parts=[TextPart(content="Revisão solicitada com sucesso.")])
        return ModelResponse(parts=[
            ToolCallPart(
                tool_name="solicitar_revisao",
                args={"reason": "OUTRO", "details": "O associado não reconhece."},
            )
        ])

    from app.domain.agent import chat_agent

    with TestClient(app, raise_server_exceptions=True) as c:
        c.post("/api/session", json={"persona_id": "ana"})
        with chat_agent.override(model=FunctionModel(solicitar_revisao_model)):
            r = c.post("/api/purchases/T-007/chat", json={"message": "Não reconheço essa compra."})

    assert r.status_code == 200, r.text
    body = r.json()
    # review_protocol deve estar preenchido
    assert body["review_protocol"] is not None, "review_protocol deve vir na resposta quando o agente solicita revisão"
    assert body["review_protocol"].startswith("RZ-")
    # Status da compra não mudou
    with TestClient(app) as c2:
        c2.post("/api/session", json={"persona_id": "ana"})
        r_status = c2.get("/api/purchases/T-007/status")
    assert r_status.json()["status"] == "AGUARDANDO_ASSOCIADO"

    # created_by deve ser AGENTE
    c2.delete("/api/session")
    c2.post("/api/session", json={"persona_id": "carla"})
    r_reviews = c2.get("/api/reviews")
    revs = r_reviews.json()["reviews"]
    assert any(rev["created_by"] == "AGENTE" for rev in revs), (
        f"Nenhuma revisão com created_by=AGENTE encontrada: {revs}"
    )


# ---------------------------------------------------------------------------
# 429: 21ª mensagem
# ---------------------------------------------------------------------------

def test_rate_limit_429_on_21st_message(db_path, monkeypatch):
    """429 na 21ª mensagem (acima de 20 em 10 min)."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    app = create_app()

    from pydantic_ai.models.test import TestModel
    from app.domain.agent import chat_agent

    with TestClient(app, raise_server_exceptions=False) as c:
        c.post("/api/session", json={"persona_id": "ana"})

        # Envia 20 mensagens — todas devem ter 200
        with chat_agent.override(model=TestModel(call_tools=[], custom_output_text="resposta")):
            for i in range(20):
                r = c.post("/api/purchases/T-007/chat", json={"message": f"msg {i}"})
                assert r.status_code == 200, f"Mensagem {i+1} retornou {r.status_code}: {r.text}"

            # 21ª mensagem → 429
            r_21 = c.post("/api/purchases/T-007/chat", json={"message": "msg 21"})

    assert r_21.status_code == 429, r_21.text
    assert r_21.json()["error"]["code"] == "RATE_LIMITED"


# ---------------------------------------------------------------------------
# Score não aparece em nenhuma rota do associado
# ---------------------------------------------------------------------------

def test_score_not_in_any_associado_route(client):
    """Score não aparece em nenhuma rota do associado (lista, detalhe, status, chat)."""
    _login(client, "ana")
    routes = [
        "/api/purchases",
        "/api/purchases/T-007",
        "/api/purchases/T-007/status",
        "/api/purchases/T-007/chat",
    ]
    for path in routes:
        r = client.get(path)
        assert r.status_code == 200, f"{path}: {r.status_code}"
        assert '"score"' not in r.text, (
            f"score aparece em {path}: {r.text[:200]}"
        )
        assert "analysis_score" not in r.text


# ---------------------------------------------------------------------------
# GET /api/health (§9)
# ---------------------------------------------------------------------------

def test_api_health_structure(client):
    """GET /api/health tem model.loaded, agent.configured, policy_version."""
    r = client.get("/api/health")
    assert r.status_code == 200, r.text
    body = r.json()
    assert "model" in body
    assert "loaded" in body["model"]
    assert "agent" in body
    assert "configured" in body["agent"]
    assert "policy_version" in body
    assert body["simulation"] is True
    assert body["contract_version"] == "v1"


def test_api_health_agent_not_configured_without_key(client):
    """Sem GROQ_API_KEY, agent.configured é False."""
    r = client.get("/api/health")
    body = r.json()
    assert body["agent"]["configured"] is False
