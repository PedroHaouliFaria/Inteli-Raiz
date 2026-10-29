"""Esquemas de resposta para os endpoints de sessão (§4 do contrato)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from app.api.schemas.common import SimulationTrue

PersonaRole = Literal["ASSOCIADO", "ANALISTA"]


class PersonaItem(BaseModel):
    model_config = {"extra": "forbid"}
    persona_id: str
    display_name: str
    role: PersonaRole


class PersonaListResponse(BaseModel):
    """GET /api/session/personas."""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "personas": [
                    {"persona_id": "ana", "display_name": "Ana Souza (fictícia)", "role": "ASSOCIADO"},
                    {"persona_id": "bruno", "display_name": "Bruno Lima (fictício)", "role": "ASSOCIADO"},
                    {"persona_id": "carla", "display_name": "Carla Reis, analista (fictícia)", "role": "ANALISTA"},
                ],
                "simulation": True,
            }
        },
    }

    personas: list[PersonaItem]
    simulation: SimulationTrue


class SessionResponse(BaseModel):
    """POST /api/session e GET /api/session."""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "persona_id": "ana",
                "display_name": "Ana Souza (fictícia)",
                "role": "ASSOCIADO",
                "simulation": True,
            }
        },
    }

    persona_id: str
    display_name: str
    role: PersonaRole
    simulation: SimulationTrue


class SessionLoginRequest(BaseModel):
    """Corpo do POST /api/session."""

    model_config = {"extra": "forbid"}

    persona_id: str
