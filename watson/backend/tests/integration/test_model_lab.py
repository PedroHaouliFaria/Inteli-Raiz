"""Rodam com o modelo real (outputs/modelo_rf.joblib); pulados se o extra `risk` não estiver instalado."""

import pytest
from fastapi.testclient import TestClient

pytest.importorskip("sklearn")

from app.main import app  # noqa: E402

client = TestClient(app)
KNOWN_FRAUD = "EVT_SYN_000094500"


def test_info_lists_the_28_features_and_the_bands():
    body = client.get("/model-lab/info").json()

    assert len(body["features"]) == 28
    assert body["test_set_frauds"] == 29
    assert (body["medium_threshold"], body["high_threshold"]) == (0.6, 0.8)


def test_known_fraud_scores_high_and_velocity_is_the_top_factor():
    sample = client.get(f"/model-lab/samples/{KNOWN_FRAUD}").json()
    body = client.post("/model-lab/score", json={"features": sample["features"]}).json()

    assert sample["is_fraud"] is True
    assert body["band"] == "high" and body["above_decision_threshold"] is True
    assert body["factors"][0]["feature"] == "cp_card_term_vel_1h"


def test_editing_a_field_changes_the_score():
    features = client.get(f"/model-lab/samples/{KNOWN_FRAUD}").json()["features"]
    edited = client.post("/model-lab/score", json={"features": {**features, "cp_card_term_vel_1h": 2}}).json()

    assert edited["band"] == "medium"


def test_missing_fields_are_rejected():
    response = client.post("/model-lab/score", json={"features": {"amount": 10}})

    assert response.status_code == 422


def test_unknown_sample_is_404():
    assert client.get("/model-lab/samples/EVT_NAO_EXISTE").status_code == 404
