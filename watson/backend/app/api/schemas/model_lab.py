from typing import Literal

from pydantic import BaseModel

FeatureValue = float | int | str | None


class FeatureInfo(BaseModel):
    name: str
    label: str
    group: str
    kind: Literal["numeric", "categorical", "binary"]
    typical_value: FeatureValue
    options: list[str] = []


class ModelInfo(BaseModel):
    name: str
    provider: str
    medium_threshold: float
    high_threshold: float
    decision_threshold: float
    test_set_size: int
    test_set_frauds: int
    features: list[FeatureInfo]


class SampleSummary(BaseModel):
    id: str
    is_fraud: bool
    amount: float | None
    mcc: str
    hour: float | None


class SampleDetail(SampleSummary):
    features: dict[str, FeatureValue]


class ScoreRequest(BaseModel):
    features: dict[str, FeatureValue]


class FactorOut(BaseModel):
    feature: str
    value: FeatureValue
    typical_value: FeatureValue
    contribution: float


class ScoreResponse(BaseModel):
    score: float
    band: Literal["low", "medium", "high"]
    above_decision_threshold: bool
    factors: list[FactorOut]
    model_name: str
    provider: str
    latency_ms: int
