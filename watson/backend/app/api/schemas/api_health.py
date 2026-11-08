"""Schema para o novo GET /api/health (§9 do contrato)."""
from __future__ import annotations

from pydantic import BaseModel


class ModelInfo(BaseModel):
    loaded: bool
    model_version: str | None = None
    score_source: str = "modelo_local"


class AgentInfo(BaseModel):
    configured: bool
    provider: str | None = None


class ApiHealthResponse(BaseModel):
    status: str  # "ok" | "degraded"
    contract_version: str = "v1"
    model: ModelInfo
    agent: AgentInfo
    policy_version: str
    simulation: bool = True
