"""Tipos comuns compartilhados entre os esquemas de resposta."""
from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, field_validator


_MONEY_RE = re.compile(r"^\d+\.\d{2}$")


class Money(BaseModel):
    """Valor monetário como string decimal com exatamente 2 casas (§2 do contrato)."""

    model_config = {"extra": "forbid"}

    value: str
    currency: str = "BRL"

    @field_validator("value")
    @classmethod
    def must_be_decimal_string_with_two_places(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("value deve ser string")
        if not _MONEY_RE.match(v):
            raise ValueError(
                "value deve ser string decimal com exatamente dois dígitos de centavos, ex: '149.58'"
            )
        return v


# Tipo que garante simulation: true em toda resposta de compra (R11)
SimulationTrue = Literal[True]
