"""Personas fictícias para a sessão de demonstração (§4 do contrato).

As três pessoas ficam aqui como fonte da verdade para o backend inteiro.
customer_id interno nunca aparece na API; só persona_id sai para o front.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PersonaRole = Literal["ASSOCIADO", "ANALISTA"]


@dataclass(frozen=True)
class Persona:
    persona_id: str
    display_name: str
    role: PersonaRole
    customer_id: str  # ID interno — nunca exposto na API


# Fonte da verdade das três pessoas fictícias (§4 e §11 do contrato)
PERSONAS: dict[str, Persona] = {
    "ana": Persona(
        persona_id="ana",
        display_name="Ana Souza (fictícia)",
        role="ASSOCIADO",
        customer_id="C-ANA",
    ),
    "bruno": Persona(
        persona_id="bruno",
        display_name="Bruno Lima (fictício)",
        role="ASSOCIADO",
        customer_id="C-BRUNO",
    ),
    "carla": Persona(
        persona_id="carla",
        display_name="Carla Reis, analista (fictícia)",
        role="ANALISTA",
        customer_id="C-CARLA",
    ),
}
