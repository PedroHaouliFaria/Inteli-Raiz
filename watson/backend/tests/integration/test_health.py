from fastapi.testclient import TestClient

from app.main import app


def test_health_reports_database_and_agent_provider():
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "sqlite", "agent_provider": "simulated"}
