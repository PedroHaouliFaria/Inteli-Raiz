"""Tipos comuns compartilhados entre os esquemas de resposta."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import BaseModel, PlainSerializer, field_validator


_MONEY_RE = re.compile(r"^\d+\.\d{2}$")


def _serialize_utc(v: datetime) -> str:
    """Serializa datetime para ISO 8601 UTC com Z. Naive é tratado como UTC."""
    if v.tzinfo is None:
        v = v.replace(tzinfo=timezone.utc)
    return v.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# Tipo anotado: aceita datetime (naive=UTC) e serializa como "YYYY-MM-DDTHH:MM:SSZ"
UtcDatetime = Annotated[datetime, PlainSerializer(_serialize_utc, return_type=str)]


class Money(BaseModel):
    """Valor monetário como string decimal com exatamente 2 casas (§2 do contrato)."""

    model_config = {"extra": "forbid"}

    value: str
    currency: Literal["BRL"] = "BRL"

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
