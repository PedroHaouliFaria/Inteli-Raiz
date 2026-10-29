import os
import pytest

# Testes rodam num SQLite em memória e com o agente simulado, sem depender de .env.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["AGENT_PROVIDER"] = "simulated"
os.environ["SESSION_SECRET"] = "test-secret-for-session"


@pytest.fixture(autouse=True)
def _clear_caches():
    """Limpa os caches de get_settings e get_engine antes e depois de cada teste.

    Impede que um teste que grave DATABASE_URL ou CONFIRMATION_TTL_SECONDS
    contamine o teste seguinte via cache de lru_cache.
    """
    from app.config import get_settings
    from app.db.session import get_engine

    get_settings.cache_clear()
    get_engine.cache_clear()
    yield
    get_settings.cache_clear()
    get_engine.cache_clear()
