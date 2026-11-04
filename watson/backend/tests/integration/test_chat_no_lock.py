"""Teste de regressão: o chat não pode travar o banco enquanto o LLM responde.

Usa um SQLite em arquivo (tmp_path) — o único ambiente onde o locking se manifesta.
O FunctionModel simula o LLM: na primeira chamada emite uma tool-call, e a função
da ferramenta tenta abrir uma segunda sessão no mesmo banco e gravar um evento.

Antes da correção isso falha com "database is locked" porque a transação BEGIN
IMMEDIATE da sessão principal ainda está aberta durante a execução da ferramenta.
Após a correção, cada ferramenta encerra sua própria transação antes de retornar
ao LLM, e o post_chat não mantém nenhuma transação aberta enquanto o LLM pensa.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def _setup(tmp_path, monkeypatch):
    db_file = str(tmp_path / "lock_test.db")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "fake-key-for-test")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    return create_app(), db_file


def test_no_db_lock_during_tool_call(tmp_path, monkeypatch):
    """A ferramenta do agente NÃO deve travar o banco com BEGIN IMMEDIATE aberto.

    A função do modelo FunctionModel, ao processar o tool-return, tenta gravar
    diretamente no banco via uma segunda conexão — como faria um request concorrente
    de polling de status ou de outro associado. Se a transação da sessão principal
    estiver aberta, esta gravação falha com OperationalError: database is locked.
    """
    app, db_file = _setup(tmp_path, monkeypatch)

    from pydantic_ai.models.function import FunctionModel, ModelResponse, TextPart, ToolCallPart
    from app.domain.agent import chat_agent

    concurrent_write_errors: list[Exception] = []

    def model_with_concurrent_write(messages, info):
        """Simula o LLM: primeiro chama consultar_compra; depois, ao receber o
        tool-return, tenta gravar no banco por uma segunda conexão independente
        (simulando um request paralelo de outro associado ou de polling de status)
        antes de finalizar.
        """
        has_tool_return = any(
            hasattr(m, "parts") and any(
                getattr(p, "part_kind", None) == "tool-return" for p in m.parts
            )
            for m in messages
        )

        if has_tool_return:
            # Tenta gravar com uma segunda sessão — DEVE funcionar se não há lock
            try:
                from sqlalchemy import create_engine, text
                from sqlalchemy.orm import sessionmaker
                engine2 = create_engine(f"sqlite:///{db_file}", pool_pre_ping=True)

                # Aplica as mesmas configurações SQLite (WAL + BEGIN IMMEDIATE)
                from sqlalchemy import event as sa_event

                @sa_event.listens_for(engine2, "connect")
                def _set_wal(conn, _rec):
                    conn.execute("PRAGMA journal_mode=WAL")

                @sa_event.listens_for(engine2, "begin")
                def _do_begin_imm(conn):
                    conn.exec_driver_sql("BEGIN IMMEDIATE")

                Session2 = sessionmaker(bind=engine2)
                with Session2() as s2:
                    # Gravação simples — simula outro request escrevendo no banco
                    s2.execute(text(
                        "INSERT INTO chat_messages (message_id, purchase_id, role, content, created_at) "
                        "VALUES ('M-concurrent-test', 1, 'user', 'concurrent write test', datetime('now'))"
                    ))
                    s2.commit()
                engine2.dispose()
            except Exception as exc:
                concurrent_write_errors.append(exc)

            return ModelResponse(parts=[TextPart(content="Compra verificada.")])

        return ModelResponse(parts=[ToolCallPart(tool_name="consultar_compra", args={})])

    with TestClient(app, raise_server_exceptions=True) as c:
        c.post("/api/session", json={"persona_id": "ana"})
        with chat_agent.override(model=FunctionModel(model_with_concurrent_write)):
            r = c.post("/api/purchases/T-007/chat", json={"message": "Qual é a loja?"})

    assert r.status_code == 200, r.text

    # A gravação concorrente NÃO deve ter travado
    assert concurrent_write_errors == [], (
        "Banco travado durante execução da ferramenta do agente — "
        f"erros encontrados: {concurrent_write_errors}"
    )
