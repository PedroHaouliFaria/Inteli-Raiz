from fastapi import APIRouter, HTTPException, Query

from app.api.schemas.model_lab import (
    FactorOut,
    FeatureInfo,
    ModelInfo,
    SampleDetail,
    SampleSummary,
    ScoreRequest,
    ScoreResponse,
)
from app.config import get_notice_policy, get_settings
from app.domain.model_lab import evaluate
from app.risk import get_reference_data, get_risk_model
from app.risk.dataset import Sample
from app.risk.features import FEATURES

router = APIRouter(prefix="/model-lab", tags=["model-lab"])


def _summary(sample: Sample) -> SampleSummary:
    f = sample.features
    return SampleSummary(id=sample.id, is_fraud=sample.is_fraud, amount=f["amount"], mcc=f["mcc"], hour=f["hora"])


def _detail(sample: Sample) -> SampleDetail:
    return SampleDetail(**_summary(sample).model_dump(), features=sample.features)


def _label(label: str | None) -> bool | None:
    return None if label is None else label == "fraud"


@router.get("/info", response_model=ModelInfo)
def info() -> ModelInfo:
    model, reference, policy = get_risk_model(), get_reference_data(), get_notice_policy()
    return ModelInfo(
        name=model.name,
        provider=model.provider,
        medium_threshold=policy.medium_threshold,
        high_threshold=policy.high_threshold,
        decision_threshold=get_settings().risk_decision_threshold,
        test_set_size=len(reference.samples),
        test_set_frauds=sum(s.is_fraud for s in reference.samples.values()),
        features=[
            FeatureInfo(
                name=f.name,
                label=f.label,
                group=f.group,
                kind=f.kind.value,
                typical_value=reference.baseline[f.name],
                options=reference.options.get(f.name, []),
            )
            for f in FEATURES
        ],
    )


@router.get("/samples", response_model=list[SampleSummary])
def search_samples(
    q: str = "",
    label: str | None = Query(None, pattern="^(fraud|legit)$"),
    limit: int = Query(20, ge=1, le=100),
) -> list[SampleSummary]:
    return [_summary(s) for s in get_reference_data().search(q, _label(label), limit)]


@router.get("/samples/random", response_model=SampleDetail)
def random_sample(label: str | None = Query(None, pattern="^(fraud|legit)$")) -> SampleDetail:
    return _detail(get_reference_data().pick_random(_label(label)))


@router.get("/samples/{sample_id}", response_model=SampleDetail)
def get_sample(sample_id: str) -> SampleDetail:
    sample = get_reference_data().find(sample_id)
    if sample is None:
        raise HTTPException(404, "Transação não encontrada no conjunto de teste")
    return _detail(sample)


@router.post("/score", response_model=ScoreResponse)
def score(request: ScoreRequest) -> ScoreResponse:
    model = get_risk_model()
    try:
        result = evaluate(
            request.features,
            model=model,
            reference=get_reference_data(),
            policy=get_notice_policy(),
            decision_threshold=get_settings().risk_decision_threshold,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return ScoreResponse(
        score=result.score,
        band=result.band.value,
        above_decision_threshold=result.above_decision_threshold,
        factors=[FactorOut(**vars(f)) for f in result.factors],
        model_name=model.name,
        provider=model.provider,
        latency_ms=result.latency_ms,
    )
