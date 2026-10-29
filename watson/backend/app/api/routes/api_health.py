"""GET /api/health — novo endpoint do contrato (§9).

Diferente do antigo /health (mantido para compatibilidade), este:
- Fica sob o prefixo /api
- Inclui model.loaded, agent.configured, policy_version
- Não expõe dado de pessoa
"""
from __future__ import annotations

from fastapi import APIRouter

from app.api.schemas.api_health import AgentInfo, ApiHealthResponse, ModelInfo

router = APIRouter(tags=["api-health"])


@router.get("/api/health", response_model=ApiHealthResponse)
def api_health() -> ApiHealthResponse:
    """Saúde do serviço (§9 do contrato). Público, sem dado de pessoa."""
    from app.config import get_settings
    settings = get_settings()

    # Verifica se o modelo local está disponível
    model_loaded = False
    model_version: str | None = None
    try:
        import pathlib
        from app.risk.models import LocalRiskModel
        model_path = pathlib.Path(settings.risk_model_path)
        if model_path.exists():
            m = LocalRiskModel(model_path)
            model_loaded = True
            model_version = m.name
    except Exception:
        model_loaded = False

    # Verifica se o agente está configurado
    agent_configured = bool(settings.groq_api_key)
    provider: str | None = None
    if agent_configured:
        model_name = settings.llm_model
        provider = model_name.split(":")[0] if ":" in model_name else model_name

    return ApiHealthResponse(
        status="ok" if model_loaded else "degraded",
        contract_version="v1",
        model=ModelInfo(
            loaded=model_loaded,
            model_version=model_version,
            score_source="modelo_local",
        ),
        agent=AgentInfo(
            configured=agent_configured,
            provider=provider,
        ),
        policy_version="confirmacao-v2",
        simulation=True,
    )
