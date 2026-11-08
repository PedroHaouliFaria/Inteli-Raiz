from datetime import datetime, timedelta
from decimal import Decimal

from app.simulation.burst import AttemptStatus, BurstSimulationConfig, RealPurchase, simulate_burst

PURCHASE = RealPurchase(
    id=9121,
    card_id=4821,
    occurred_at=datetime(2025, 9, 26, 3, 14),
    amount=Decimal("2349.90"),
    channel="card_not_present",
    region="São Paulo, SP",
    velocity_1h=47,
)


def test_below_threshold_generates_nothing():
    low = RealPurchase(**{**PURCHASE.__dict__, "velocity_1h": 9})
    assert simulate_burst(low) == []
    missing = RealPurchase(**{**PURCHASE.__dict__, "velocity_1h": None})
    assert simulate_burst(missing) == []


def test_generates_at_most_max_attempts_and_never_more_than_the_counter():
    assert len(simulate_burst(PURCHASE)) == 5
    small = RealPurchase(**{**PURCHASE.__dict__, "velocity_1h": 3})
    assert len(simulate_burst(small, BurstSimulationConfig(velocity_threshold=3))) == 2


def test_attempts_follow_the_rule():
    attempts = simulate_burst(PURCHASE)
    window_start = PURCHASE.occurred_at - timedelta(minutes=15)
    times = [a.occurred_at for a in attempts]
    assert times == sorted(times)
    for a in attempts:
        assert a.is_simulated
        assert a.simulated_from_id == PURCHASE.id
        assert a.card_id == PURCHASE.card_id
        assert (a.channel, a.region) == (PURCHASE.channel, PURCHASE.region)
        assert window_start <= a.occurred_at < PURCHASE.occurred_at
        assert PURCHASE.amount * Decimal("0.3") <= a.amount <= PURCHASE.amount * Decimal("1.5")
        assert a.status in (AttemptStatus.HELD, AttemptStatus.DECLINED)


def test_same_seed_same_attempts():
    assert simulate_burst(PURCHASE) == simulate_burst(PURCHASE)
    assert simulate_burst(PURCHASE) != simulate_burst(PURCHASE, BurstSimulationConfig(seed=7))


def test_config_is_read_from_settings(monkeypatch):
    from app import config

    monkeypatch.setenv("BURST_MAX_ATTEMPTS", "2")
    config.get_settings.cache_clear()
    try:
        assert len(simulate_burst(PURCHASE, config.get_burst_simulation_config())) == 2
    finally:
        config.get_settings.cache_clear()
