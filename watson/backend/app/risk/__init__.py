"""Score de risco em tempo de execução: carrega o modelo treinado, calcula sinais e fatores explicáveis."""

from functools import lru_cache
from pathlib import Path

from app.config import get_settings
from app.risk.dataset import ReferenceData, load_reference_data
from app.risk.models import RiskModel


@lru_cache
def get_risk_model() -> RiskModel:
    settings = get_settings()
    if settings.risk_model_provider == "watsonx":
        from app.risk.models import WatsonxRiskModel

        return WatsonxRiskModel(settings.watsonx_url, settings.watsonx_api_key, settings.risk_watsonx_deployment_id)
    from app.risk.models import LocalRiskModel

    return LocalRiskModel(Path(settings.risk_model_path))


@lru_cache
def get_reference_data() -> ReferenceData:
    return load_reference_data(Path(get_settings().risk_data_dir))
