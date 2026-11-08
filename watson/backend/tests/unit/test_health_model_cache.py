"""Teste de segurança do GET /api/health — modelo carregado uma única vez.

Fix 2: O LocalRiskModel não deve ser instanciado a cada chamada ao health.
O modelo deve ser carregado uma vez (no lifespan ou num cache) e o health
apenas reporta esse estado.
"""
from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock


def test_api_health_does_not_reload_model_on_each_call(tmp_path, monkeypatch):
    """Múltiplas chamadas ao /api/health não instanciam o modelo de novo.

    Conta invocações do construtor LocalRiskModel.__init__ via patch:
    - Após o lifespan subir (seed + carga inicial), o contador é gravado.
    - Três chamadas ao health não devem adicionar nenhuma nova instância.
    """
    db_path = str(tmp_path / "test.db")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-for-session")
    monkeypatch.setenv("GROQ_API_KEY", "")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    from app.main import create_app
    from fastapi.testclient import TestClient

    constructor_calls = {"n": 0}

    def counting_init(self, path):
        constructor_calls["n"] += 1
        # Modelo não existe no ambiente de teste — apenas contamos
        raise FileNotFoundError("modelo não disponível no teste")

    with patch("app.risk.models.LocalRiskModel.__init__", counting_init):
        app = create_app()
        with TestClient(app, raise_server_exceptions=True) as c:
            # Após o lifespan iniciar, grava quantas instâncias foram feitas (seed)
            calls_after_startup = constructor_calls["n"]

            # Chama o health 3 vezes
            r1 = c.get("/api/health")
            r2 = c.get("/api/health")
            r3 = c.get("/api/health")

    assert r1.status_code == 200, r1.text
    assert r2.status_code == 200, r2.text
    assert r3.status_code == 200, r3.text

    calls_after_health = constructor_calls["n"]
    extra = calls_after_health - calls_after_startup
    assert extra == 0, (
        f"LocalRiskModel foi instanciado {extra} vezes extra durante as chamadas ao health "
        f"(total={calls_after_health}, após startup={calls_after_startup}). "
        "O health deve apenas ler o estado do lifespan, sem instanciar o modelo."
    )
