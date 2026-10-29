"""GET /api/health — novo endpoint do contrato (§9).

Diferente do antigo /health (mantido para compatibilidade), este:
- Fica sob o prefixo /api
- Inclui model.loaded, agent.configured, policy_version
- Não expõe dado de pessoa
- Não carrega o modelo do disco: lê o estado gravado no lifespan (app.risk.state).
"""
from __future__ import annotations

from fastapi import APIRouter

from app.api.schemas.api_health import AgentInfo, ApiHealthResponse, ModelInfo

router = APIRouter(tags=["api-health"])


@router.get("/api/health", response_model=ApiHealthResponse)
def api_health() -> ApiHealthResponse:
    """Saúde do serviço (§9 do contrato). Público, sem dado de pessoa."""
    from app.config import get_settings
    import app.risk.state as risk_state

    settings = get_settings()

    # Lê o estado do modelo gravado uma única vez no lifespan — sem instanciar o modelo
    model_loaded = risk_state.model_loaded
    model_version = risk_state.model_version

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
