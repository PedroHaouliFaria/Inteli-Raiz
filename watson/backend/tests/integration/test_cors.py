"""Testes de integração para o comportamento do CORS com credenciais.

Verifica que a origem do front recebe allow-credentials=true e que origens
estranhas não recebem allow-origin.
"""
import os

import pytest
from fastapi.testclient import TestClient

FRONTEND_ORIGIN = "http://localhost:5173"
OTHER_ORIGIN = "http://evil.example.com"


@pytest.fixture()
def client():
    """TestClient com a app real; lru_cache já foi limpo pelo autouse fixture."""
    os.environ.setdefault("SESSION_SECRET", "test-secret-for-cors")
    from app.main import create_app

    return TestClient(create_app(), raise_server_exceptions=True)


def test_cors_credentials_allowed_for_frontend_origin(client):
    """A origem do front recebe allow-credentials: true e allow-origin exato."""
    response = client.get(
        "/health",
        headers={"Origin": FRONTEND_ORIGIN},
    )
    assert response.headers.get("access-control-allow-credentials") == "true"
    assert response.headers.get("access-control-allow-origin") == FRONTEND_ORIGIN


def test_cors_wildcard_not_sent_for_frontend_origin(client):
    """allow-origin nunca é '*' quando credentials está habilitado."""
    response = client.get(
        "/health",
        headers={"Origin": FRONTEND_ORIGIN},
    )
    assert response.headers.get("access-control-allow-origin") != "*"


def test_cors_allow_origin_absent_for_unknown_origin(client):
    """Uma origem desconhecida não recebe o cabeçalho access-control-allow-origin."""
    response = client.get(
        "/health",
        headers={"Origin": OTHER_ORIGIN},
    )
    assert "access-control-allow-origin" not in response.headers
