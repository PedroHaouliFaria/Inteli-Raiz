"""Estado do modelo de risco compartilhado entre o lifespan, o seed/demo e o health.

O modelo é carregado uma única vez no lifespan (app.main) e gravado aqui.
O GET /api/health lê deste módulo, sem instanciar nada.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.risk.models import LocalRiskModel

# Preenchido pelo lifespan; None quando o modelo não está disponível.
loaded_model: "LocalRiskModel | None" = None
model_loaded: bool = False
model_version: str | None = None
