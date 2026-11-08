"""Testes unitários para app/risk/features.normalize (Item 0)."""
import pytest

from app.risk.features import normalize


def _full_row(**overrides) -> dict:
    """Linha mínima com todos os 28 campos."""
    base = {
        "amount": "149.58",
        "amount_fees": "2.09",
        "acceptor_risk": "70.0",
        "customer_presumed_income": "1964.73",
        "customer_reported_income": "3476.74",
        "account_available_credit": "664.75",
        "account_balance": "1295.91",
        "card_credit_limit": "14553.86",
        "cardid_count_1m": "30.0",
        "cp_card_term_vel_1h": "70.0",
        "cp_card_prev_term_dist_1h": "102.13",
        "digitalwallettoken_count_3m": "80.0",
        "hora": "3",
        "dia_semana": "6",
        "valor_vs_media_cartao": "",
        "valor_vs_limite": "0.01",
        "tipo_transacao": "credito",
        "modalidade_transacao": "cartao_nao_presente",
        "card_presence_flag": "N",
        "card_type": "credito",
        "card_brand": "BANDEIRA_A",
        "mcc": "5411",
        "acceptor_region": "",
        "customer_risk_rating": "baixo",
        "customer_region": "SP",
        "madrugada": "1",
        "cnp_credito": "1",
        "primeira_compra_cartao": "1",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Bug: int(bool("0")) == 1  — deve ser 0
# ---------------------------------------------------------------------------

def test_binary_string_zero_yields_int_zero():
    """Bug item 0: normalize("0") para binário deve retornar 0, não 1."""
    row = _full_row(madrugada="0", cnp_credito="0", primeira_compra_cartao="0")
    out = normalize(row)
    assert out["madrugada"] == 0, f"esperado 0, obteve {out['madrugada']}"
    assert out["cnp_credito"] == 0
    assert out["primeira_compra_cartao"] == 0


def test_binary_string_one_yields_int_one():
    row = _full_row(madrugada="1", cnp_credito="1", primeira_compra_cartao="1")
    out = normalize(row)
    assert out["madrugada"] == 1
    assert out["cnp_credito"] == 1
    assert out["primeira_compra_cartao"] == 1


def test_binary_int_zero_yields_int_zero():
    row = _full_row(madrugada=0, cnp_credito=0, primeira_compra_cartao=0)
    out = normalize(row)
    assert out["madrugada"] == 0


def test_binary_int_one_yields_int_one():
    row = _full_row(madrugada=1, cnp_credito=1, primeira_compra_cartao=1)
    out = normalize(row)
    assert out["madrugada"] == 1


def test_binary_none_yields_none():
    row = _full_row(madrugada=None)
    out = normalize(row)
    assert out["madrugada"] is None


def test_binary_empty_string_yields_none():
    row = _full_row(madrugada="")
    out = normalize(row)
    assert out["madrugada"] is None


def test_binary_invalid_string_raises_value_error():
    row = _full_row(madrugada="true")
    with pytest.raises(ValueError):
        normalize(row)


def test_binary_invalid_int_raises_value_error():
    row = _full_row(madrugada=2)
    with pytest.raises(ValueError):
        normalize(row)


def test_binary_invalid_float_raises_value_error():
    row = _full_row(madrugada=0.5)
    with pytest.raises(ValueError):
        normalize(row)
