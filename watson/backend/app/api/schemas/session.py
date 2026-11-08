"""Esquemas de resposta para os endpoints de sessão (§4 do contrato)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

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
                "demo_mode": False,
            }
        },
    }

    persona_id: str
    display_name: str
    role: PersonaRole
    simulation: SimulationTrue
    demo_mode: bool


class SessionLoginRequest(BaseModel):
    """Corpo do POST /api/session."""

    model_config = {"extra": "forbid"}

    email: str | None = Field(default=None, min_length=3, max_length=254)
    password: str | None = Field(default=None, min_length=1, max_length=128)
    # Temporário: permite que a suíte legada migre sem alterar os contratos
    # dos demais domínios. A rota só aceita isto com flag explícita de teste.
    persona_id: str | None = None

    @model_validator(mode="after")
    def validate_login_shape(self):
        if self.email is not None and self.password is not None and self.persona_id is None:
            return self
        if self.persona_id is not None and self.email is None and self.password is None:
            return self
        raise ValueError("Informe e-mail e senha.")
