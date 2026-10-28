"""Testes dos sinais de risco por regra (§5 e §6 do contrato)."""
import pytest

from app.domain.signals.rules import compute_signals, Signal


# ---------------------------------------------------------------------------
# T-007: fraude_supermercado_madrugada
# card_presence_flag=N → CARTAO_NAO_PRESENTE
# hora=3 → MADRUGADA
# primeira_compra_cartao=1 → PRIMEIRA_COMPRA_CARTAO
# ---------------------------------------------------------------------------

T007_FEATURES = {
    "card_presence_flag": "N",
    "hora": 3,
    "madrugada": 1,
    "primeira_compra_cartao": 1,
    "mcc": "5411",
    "card_type": "credito",
    "card_brand": "BANDEIRA_A",
    "amount": 149.58,
    "card_id": "CARD_SYN_0042938",
}


def test_t007_has_three_signals_in_order():
    signals = compute_signals(T007_FEATURES)
    codes = [s.code for s in signals]
    assert codes == ["CARTAO_NAO_PRESENTE", "MADRUGADA", "PRIMEIRA_COMPRA_CARTAO"]


def test_t007_madrugada_label_includes_hour():
    signals = compute_signals(T007_FEATURES)
    madrugada = next(s for s in signals if s.code == "MADRUGADA")
    assert "3h" in madrugada.label


def test_t007_amount_cents_and_card_last4():
    """Verifica derivação de amount_cents e card_last4 a partir dos dados brutos."""
    from app.domain.signals.rules import amount_to_cents, card_last4
    assert amount_to_cents(149.58) == 14958
    assert card_last4("CARD_SYN_0042938") == "2938"


# ---------------------------------------------------------------------------
# T-003: legitima_farmacia — sem sinais
# ---------------------------------------------------------------------------

T003_FEATURES = {
    "card_presence_flag": "Y",
    "hora": 18,
    "madrugada": 0,
    "primeira_compra_cartao": 0,
    "mcc": "5912",
    "card_type": "credito",
    "card_brand": "BANDEIRA_A",
    "amount": 15.68,
    "card_id": "CARD_SYN_0016717",
}


def test_t003_has_no_signals():
    signals = compute_signals(T003_FEATURES)
    assert signals == []


# ---------------------------------------------------------------------------
# T-011: compra_do_bruno — sem sinais
# ---------------------------------------------------------------------------

T011_FEATURES = {
    "card_presence_flag": "Y",
    "hora": 8,
    "madrugada": 0,
    "primeira_compra_cartao": 0,
    "mcc": "5812",
    "card_type": "debito",
    "card_brand": "BANDEIRA_B",
    "amount": 131.44,
    "card_id": "CARD_SYN_0028931",
}


def test_t011_has_no_signals():
    signals = compute_signals(T011_FEATURES)
    assert signals == []


# ---------------------------------------------------------------------------
# Rótulos de MCC
# ---------------------------------------------------------------------------

def test_mcc_labels():
    from app.domain.signals.rules import mcc_label
    assert mcc_label("5411") == "Supermercado"
    assert mcc_label("5912") == "Farmácia"
    assert mcc_label("5812") == "Restaurante"
    assert mcc_label("9999") == "Categoria 9999"


# ---------------------------------------------------------------------------
# source = "regra" em todos os sinais
# ---------------------------------------------------------------------------

def test_all_signals_have_source_regra():
    signals = compute_signals(T007_FEATURES)
    for s in signals:
        assert s.source == "regra"
