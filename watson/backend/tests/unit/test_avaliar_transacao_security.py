"""Testes de segurança da ferramenta avaliar_transacao (§10 do contrato).

Fix 1:
- Ferramenta não devolve score, score_source nem model_version ao LLM.
- Resposta final do agente não contém o valor numérico do score.
"""
from __future__ import annotations

import asyncio
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_purchase(score: float = 0.9917):
    """Cria um objeto Purchase falso com o score gravado."""
    p = MagicMock()
    p.case_id = "T-007"
    p.customer_id = "cust-ana"
    p.analysis_score = score
    p.analysis_score_source = "modelo_local"
    p.analysis_model_version = "rf-2026-10-27"
    p.analysis_decision = "SOLICITAR_CONFIRMACAO"
    p.analysis_policy_version = "confirmacao-v2"
    p.analysis_gaps_json = ["Nome do estabelecimento não disponível."]
    p.analysis_evaluated_at = datetime(2026, 10, 25, 6, 12, 0)
    p.features_json = {}
    return p


def _make_ctx(purchase):
    """Cria um RunContext falso com deps adequados."""
    ctx = MagicMock()
    ctx.deps.case_id = "T-007"
    ctx.deps.customer_id = "cust-ana"

    session = MagicMock()
    session.execute.return_value.scalar_one_or_none.return_value = purchase
    ctx.deps.db = session
    return ctx


# ---------------------------------------------------------------------------
# Teste 1: ferramenta não devolve score, score_source nem model_version
# ---------------------------------------------------------------------------

def test_avaliar_transacao_does_not_return_score_fields():
    """avaliar_transacao não deve devolver score, score_source nem model_version (§10)."""
    from app.domain.agent import _make_agent

    agent = _make_agent()
    # Extrai a função da ferramenta registrada
    tool_fn = agent._function_toolset.tools["avaliar_transacao"].function

    purchase = _make_purchase(score=0.9917)
    ctx = _make_ctx(purchase)

    result = asyncio.get_event_loop().run_until_complete(tool_fn(ctx))

    # Campos proibidos
    assert "score" not in result, f"'score' não deve estar no retorno: {result}"
    assert "score_source" not in result, f"'score_source' não deve estar no retorno: {result}"
    assert "model_version" not in result, f"'model_version' não deve estar no retorno: {result}"

    # Campos obrigatórios pelo §10
    assert "analysis_id" in result
    assert "score_available" in result
    assert isinstance(result["score_available"], bool)
    assert "decision" in result
    assert "policy_version" in result


def test_avaliar_transacao_does_not_leak_score_value_in_text():
    """O valor numérico do score (ex.: '0.9917') não deve aparecer como string no retorno."""
    from app.domain.agent import _make_agent

    agent = _make_agent()
    tool_fn = agent._function_toolset.tools["avaliar_transacao"].function

    score = 0.9917
    purchase = _make_purchase(score=score)
    ctx = _make_ctx(purchase)

    result = asyncio.get_event_loop().run_until_complete(tool_fn(ctx))

    result_str = str(result)
    assert str(score) not in result_str, (
        f"Valor do score {score} não deve aparecer no retorno da ferramenta: {result_str}"
    )
    assert "0.99" not in result_str, (
        f"Valor do score (0.99...) não deve aparecer no retorno: {result_str}"
    )


# ---------------------------------------------------------------------------
# Teste 2: segunda camada — resposta do agente com score é substituída
# ---------------------------------------------------------------------------

def test_agent_response_with_score_value_is_scrubbed(tmp_path, monkeypatch):
    """Se o LLM escrever o valor do score na resposta, ela deve ser substituída por msg segura."""
    import os
    db_path = str(tmp_path / "test.db")
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
    from fastapi.testclient import TestClient

    # FunctionModel que devolve diretamente o valor do score (0.9917) na resposta
    # sem chamar nenhuma tool — simula vazamento por injeção de prompt
    def leaking_model(messages, info):
        return ModelResponse(parts=[
            TextPart(content="O score desta compra é 0.9917, que corresponde a 99% de fraude.")
        ])

    from app.domain.agent import chat_agent

    with TestClient(app, raise_server_exceptions=True) as c:
        c.post("/api/session", json={"persona_id": "ana"})
        with chat_agent.override(model=FunctionModel(leaking_model)):
            r = c.post("/api/purchases/T-007/chat", json={"message": "qual é o score?"})

    assert r.status_code == 200, r.text
    body = r.json()
    reply_content = body["reply"]["content"]

    # A resposta não deve conter o valor do score
    assert "0.9917" not in reply_content, (
        f"Score '0.9917' não deve aparecer na resposta final: {reply_content}"
    )
    assert "99%" not in reply_content, (
        f"'99%' não deve aparecer na resposta final: {reply_content}"
    )
