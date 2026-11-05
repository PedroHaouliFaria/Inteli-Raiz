from __future__ import annotations

from pydantic import BaseModel, Field

from app.api.schemas.common import SimulationTrue


class CopilotStatusResponse(BaseModel):
    model_config = {"extra": "forbid"}

    greeting: str
    capabilities: list[str]
    agent_available: bool
    simulation: SimulationTrue


class CopilotRequest(BaseModel):
    model_config = {"extra": "forbid"}

    message: str = Field(..., min_length=1, max_length=1000)


class CopilotReplyResponse(BaseModel):
    model_config = {"extra": "forbid"}

    content: str
    tools_used: list[str]
    action_taken: bool
    simulation: SimulationTrue
