"""Tentativas simuladas de rajada (docs/dados/modelo-de-dados.md, seção "Rajada: indicador e tentativas simuladas").

No case, a rajada só existe como contador (`cp_card_term_vel_1h` → `velocity_1h`), não como linhas.
Para a demo mostrar a rajada na linha do tempo, geramos tentativas anteriores no mesmo cartão,
coerentes com o contador e sempre marcadas como simuladas. Elas nunca recebem risk_assessment,
nunca viram alerta e ficam fora das métricas.
"""

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


class AttemptStatus(str, Enum):
    HELD = "held"
    DECLINED = "declined"


@dataclass(frozen=True)
class BurstSimulationConfig:
    velocity_threshold: int = 10
    max_attempts: int = 5
    window_minutes: int = 15
    min_amount_factor: float = 0.3
    max_amount_factor: float = 1.5
    seed: int = 42


@dataclass(frozen=True)
class RealPurchase:
    """A compra real do case que serve de base para a simulação."""

    id: int
    card_id: int
    occurred_at: datetime
    amount: Decimal
    channel: str
    region: str
    velocity_1h: int | None


@dataclass(frozen=True)
class SimulatedAttempt:
    card_id: int
    occurred_at: datetime
    amount: Decimal
    channel: str
    region: str
    status: AttemptStatus
    simulated_from_id: int
    is_simulated: bool = True


def simulate_burst(purchase: RealPurchase, config: BurstSimulationConfig | None = None) -> list[SimulatedAttempt]:
    """Gera até `max_attempts` tentativas nos `window_minutes` antes da compra real, em ordem de horário.

    Só simula quando `velocity_1h` alcança o limite. O sorteio usa a semente fixa e o id da compra,
    então a mesma compra gera sempre as mesmas tentativas.
    """
    config = config or BurstSimulationConfig()
    velocity = purchase.velocity_1h or 0
    if velocity < config.velocity_threshold:
        return []

    # O contador conta a compra real também; nunca simulamos mais tentativas do que ele indica.
    count = min(config.max_attempts, velocity - 1)
    rng = random.Random(f"{config.seed}:{purchase.id}")
    window_seconds = config.window_minutes * 60
    offsets = sorted(rng.sample(range(1, window_seconds), count), reverse=True)

    attempts = []
    for offset in offsets:
        factor = Decimal(str(rng.uniform(config.min_amount_factor, config.max_amount_factor)))
        attempts.append(
            SimulatedAttempt(
                card_id=purchase.card_id,
                occurred_at=purchase.occurred_at - timedelta(seconds=offset),
                amount=(purchase.amount * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                channel=purchase.channel,
                region=purchase.region,
                status=rng.choice(list(AttemptStatus)),
                simulated_from_id=purchase.id,
            )
        )
    return attempts
