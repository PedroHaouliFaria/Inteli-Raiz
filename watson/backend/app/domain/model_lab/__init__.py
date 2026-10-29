"""Laboratório do modelo: ambiente experimental para ver o que o modelo de risco infere de uma transação.

Nada aqui cria alerta, caso ou aviso; só pontua e explica.
"""

import time
from dataclasses import dataclass

from app.domain.notices.policy import NoticePolicy, RiskBand, risk_band
from app.risk.explain import Factor, explain
from app.risk.features import normalize
from app.risk.dataset import ReferenceData
from app.risk.models import RiskModel


@dataclass(frozen=True)
class Evaluation:
    score: float
    band: RiskBand
    above_decision_threshold: bool
    factors: list[Factor]
    latency_ms: int


def evaluate(
    features: dict,
    *,
    model: RiskModel,
    reference: ReferenceData,
    policy: NoticePolicy,
    decision_threshold: float,
) -> Evaluation:
    started = time.monotonic()
    explanation = explain(model, normalize(features), reference.baseline)
    return Evaluation(
        score=explanation.score,
        band=risk_band(explanation.score, policy),
        above_decision_threshold=explanation.score >= decision_threshold,
        factors=explanation.factors,
        latency_ms=int((time.monotonic() - started) * 1000),
    )
