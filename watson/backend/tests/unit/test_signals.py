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
    "modalidade_transacao": "cartao_nao_presente",
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
    "modalidade_transacao": "cartao_presente",
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
    "modalidade_transacao": "cartao_presente",
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


# ---------------------------------------------------------------------------
# Fix B: MADRUGADA usa só a coluna madrugada=="1"
# ---------------------------------------------------------------------------

def test_madrugada_hora5_flag0_nao_dispara():
    """hora=5 e madrugada=0: NÃO deve disparar MADRUGADA (bug da implementação antiga)."""
    feats = {
        "card_presence_flag": "Y",
        "hora": "5",
        "madrugada": "0",
        "primeira_compra_cartao": "0",
    }
    codes = [s.code for s in compute_signals(feats)]
    assert "MADRUGADA" not in codes


def test_madrugada_hora_vazia_flag1_dispara():
    """hora="" e madrugada="1": deve disparar MADRUGADA sem quebrar."""
    feats = {
        "card_presence_flag": "Y",
        "hora": "",
        "madrugada": "1",
        "primeira_compra_cartao": "0",
    }
    signals = compute_signals(feats)
    codes = [s.code for s in signals]
    assert "MADRUGADA" in codes
    madrugada_signal = next(s for s in signals if s.code == "MADRUGADA")
    assert madrugada_signal.label == "Feita de madrugada."


def test_madrugada_hora_vazia_flag0_nao_dispara():
    """hora="" e madrugada="0": NÃO deve disparar MADRUGADA."""
    feats = {
        "card_presence_flag": "Y",
        "hora": "",
        "madrugada": "0",
        "primeira_compra_cartao": "0",
    }
    codes = [s.code for s in compute_signals(feats)]
    assert "MADRUGADA" not in codes


# ---------------------------------------------------------------------------
# Fix C: CARTAO_NAO_PRESENTE usa modalidade_transacao, não card_presence_flag
# ---------------------------------------------------------------------------

def test_cartao_nao_presente_modalidade_online_dispara():
    """modalidade_transacao='cartao_nao_presente' deve disparar CARTAO_NAO_PRESENTE."""
    feats = {
        "modalidade_transacao": "cartao_nao_presente",
        "card_presence_flag": "N",  # consistente
        "hora": "10",
        "madrugada": "0",
        "primeira_compra_cartao": "0",
    }
    codes = [s.code for s in compute_signals(feats)]
    assert "CARTAO_NAO_PRESENTE" in codes


def test_cartao_presente_card_flag_n_nao_dispara():
    """modalidade_transacao='cartao_presente' com card_presence_flag='N' (dados inconsistentes):
    NÃO deve disparar (1697 linhas afetadas pelo bug)."""
    feats = {
        "modalidade_transacao": "cartao_presente",
        "card_presence_flag": "N",  # inconsistente — deve ser ignorado
        "hora": "10",
        "madrugada": "0",
        "primeira_compra_cartao": "0",
    }
    codes = [s.code for s in compute_signals(feats)]
    assert "CARTAO_NAO_PRESENTE" not in codes


def test_cartao_presente_nao_dispara():
    """modalidade_transacao='cartao_presente' NÃO deve disparar CARTAO_NAO_PRESENTE."""
    feats = {
        "modalidade_transacao": "cartao_presente",
        "card_presence_flag": "Y",
        "hora": "10",
        "madrugada": "0",
        "primeira_compra_cartao": "0",
    }
    codes = [s.code for s in compute_signals(feats)]
    assert "CARTAO_NAO_PRESENTE" not in codes

