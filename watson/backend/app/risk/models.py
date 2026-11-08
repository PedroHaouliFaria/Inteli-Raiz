"""Onde o modelo de risco roda. O resto do código só conhece a interface RiskModel.

- local: carrega outputs/modelo_rf.joblib (o mesmo arquivo publicado no watsonx.ai). Precisa do extra `risk`.
- watsonx: chama o deployment online no watsonx.ai Runtime, como agente/tools/pontuar_transacao.py.
"""

import time
from pathlib import Path
from typing import Protocol

import httpx

from app.risk.features import FEATURE_NAMES, FEATURES, FeatureKind

# Numéricos e binários vão como float, para None virar NaN e o imputador do pipeline preencher.
_NUMBER_COLUMNS = [f.name for f in FEATURES if f.kind is not FeatureKind.CATEGORICAL]

IAM_URL = "https://iam.cloud.ibm.com/identity/token"


class RiskModel(Protocol):
    name: str
    provider: str

    def predict(self, rows: list[dict]) -> list[float]:
        """Probabilidade de fraude de cada transação, de 0 a 1, na mesma ordem."""
        ...


class LocalRiskModel:
    provider = "local"

    def __init__(self, path: Path) -> None:
        import joblib

        # Arquivo gerado pelo notebook 03 do próprio time, versionado no repositório.
        self._pipeline = joblib.load(path)
        self.name = path.stem

    def predict(self, rows: list[dict]) -> list[float]:
        import pandas as pd

        frame = pd.DataFrame(rows, columns=list(FEATURE_NAMES))
        frame[_NUMBER_COLUMNS] = frame[_NUMBER_COLUMNS].astype(float)
        return [float(p) for p in self._pipeline.predict_proba(frame)[:, 1]]


class WatsonxRiskModel:
    provider = "watsonx"

    def __init__(self, url: str, api_key: str, deployment_id: str, name: str = "rf_fraude_sicredi") -> None:
        if not api_key or not deployment_id:
            raise ValueError("defina WATSONX_API_KEY e RISK_WATSONX_DEPLOYMENT_ID para usar o modelo no watsonx.ai")
        self._url = url.rstrip("/")
        self._api_key = api_key
        self._deployment_id = deployment_id
        self._token: str | None = None
        self._token_expires_at = 0.0
        self.name = name

    def _bearer(self) -> str:
        if self._token is None or time.time() > self._token_expires_at - 60:
            resp = httpx.post(
                IAM_URL,
                data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": self._api_key},
                timeout=20,
            )
            resp.raise_for_status()
            body = resp.json()
            self._token = body["access_token"]
            self._token_expires_at = float(body.get("expiration", time.time() + 3000))
        return self._token

    def predict(self, rows: list[dict]) -> list[float]:
        payload = {
            "input_data": [
                {"fields": list(FEATURE_NAMES), "values": [[row[name] for name in FEATURE_NAMES] for row in rows]}
            ]
        }
        resp = httpx.post(
            f"{self._url}/ml/v4/deployments/{self._deployment_id}/predictions?version=2021-05-01",
            json=payload,
            headers={"Authorization": f"Bearer {self._bearer()}"},
            timeout=30,
        )
        resp.raise_for_status()
        output = resp.json()["predictions"][0]
        prob_idx = output["fields"].index("probability")
        return [float(values[prob_idx][1]) for values in output["values"]]
