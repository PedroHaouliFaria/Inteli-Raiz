"""Fatores explicáveis do score.

O Random Forest não diz por que deu um score a uma transação específica. Medimos assim:
para cada campo, trocamos só ele pelo valor típico de uma compra legítima e vemos quanto o score muda.
Positivo = o campo empurrou o score para cima. Uma chamada ao modelo com 1 + 28 linhas.
"""

from dataclasses import dataclass

from app.risk.features import FEATURES
from app.risk.models import RiskModel


@dataclass(frozen=True)
class Factor:
    feature: str
    value: object
    typical_value: object
    contribution: float


@dataclass(frozen=True)
class Explanation:
    score: float
    factors: list[Factor]


def explain(model: RiskModel, row: dict, baseline: dict) -> Explanation:
    changed = [f for f in FEATURES if row[f.name] != baseline[f.name]]
    variants = [{**row, f.name: baseline[f.name]} for f in changed]
    score, *others = model.predict([row, *variants])
    factors = [
        Factor(f.name, row[f.name], baseline[f.name], round(score - other, 4))
        for f, other in zip(changed, others)
    ]
    factors.sort(key=lambda factor: abs(factor.contribution), reverse=True)
    return Explanation(score=score, factors=factors)
