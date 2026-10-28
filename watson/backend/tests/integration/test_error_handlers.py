"""Testes dos handlers de erro globais (§2 do contrato)."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.errors import ApiError, add_error_handlers


@pytest.fixture()
def test_app():
    """App mínima com as rotas de teste e os handlers registrados."""
    app = FastAPI()
    add_error_handlers(app)

    @app.get("/api/boom")
    def boom():
        raise RuntimeError("segredo interno que não pode vazar")

    @app.get("/api/api-error")
    def api_error_route():
        raise ApiError(status_code=409, code="VERSION_MISMATCH", message="Versão desatualizada.")

    return app


def test_unknown_route_returns_404_envelope(test_app):
    resp = TestClient(test_app).get("/api/nao-existe")
    assert resp.status_code == 404
    body = resp.json()
    assert body["error"]["code"] == "NOT_FOUND"
    assert "error" in body
    assert "stack" not in str(body)


def test_unhandled_exception_returns_500_without_leak(test_app):
    resp = TestClient(test_app, raise_server_exceptions=False).get("/api/boom")
    assert resp.status_code == 500
    body = resp.json()
    assert body["error"]["code"] == "INTERNAL_ERROR"
    # Não pode vazar o texto da exceção
    assert "segredo" not in resp.text
    assert "stack" not in resp.text
    assert "traceback" not in resp.text.lower()


def test_api_error_is_returned_as_envelope(test_app):
    resp = TestClient(test_app).get("/api/api-error")
    assert resp.status_code == 409
    body = resp.json()
    assert body["error"]["code"] == "VERSION_MISMATCH"
    assert body["error"]["message"] == "Versão desatualizada."


def test_validation_error_returns_400_invalid_request():
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()
    add_error_handlers(app)

    class Body(BaseModel):
        value: int

    @app.post("/api/typed")
    def typed(body: Body):
        return body

    resp = TestClient(app).post("/api/typed", json={"value": "nao-e-int"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["error"]["code"] == "INVALID_REQUEST"
