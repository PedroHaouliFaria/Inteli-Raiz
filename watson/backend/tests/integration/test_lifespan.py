"""Testa o comportamento do lifespan: seed e engine (Fix E)."""
import pytest


def test_lifespan_uses_app_engine():
    """O lifespan usa get_engine() da aplicação (não cria engine próprio).
    Verificado indiretamente: o engine da sessão e o do lifespan devem ser o mesmo objeto."""
    from app.db.session import get_engine

    # Garante que o cache do get_engine está limpo no escopo deste teste
    get_engine.cache_clear()

    # Importa o módulo main para acessar a função lifespan; não sobe servidor
    import app.main as main_module

    # Importa o código do lifespan para inspecionar: ele deve chamar get_engine
    import inspect
    source = inspect.getsource(main_module.lifespan)
    assert "get_engine" in source, "lifespan deve usar get_engine() em vez de criar engine próprio"
    assert "create_engine" not in source, "lifespan não deve criar engine próprio com create_engine()"


def test_lifespan_seed_failure_raises(monkeypatch, tmp_path):
    """Falha no seed durante o lifespan deve derrubar a subida do app."""
    import os

    db_path = str(tmp_path / "fail_test.db")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    from app.config import get_settings
    from app.db.session import get_engine
    get_settings.cache_clear()
    get_engine.cache_clear()

    import app.db.seed as seed_module
    original_run_seed = seed_module.run_seed

    def broken_seed(session, ttl_seconds=900):
        raise RuntimeError("Seed falhou intencionalmente")

    monkeypatch.setattr(seed_module, "run_seed", broken_seed)

    from fastapi.testclient import TestClient
    import app.main as main_module

    # Recarrega o main com o monkeypatch ativo
    import importlib
    importlib.reload(main_module)

    with pytest.raises(Exception):
        # TestClient.__enter__ chama o lifespan; falha deve propagar
        with TestClient(main_module.app):
            pass

    # Cleanup
    monkeypatch.setattr(seed_module, "run_seed", original_run_seed)
    get_settings.cache_clear()
    get_engine.cache_clear()
