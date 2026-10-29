from app.risk.explain import explain
from app.risk.features import FEATURE_NAMES


class LinearModel:
    """Modelo de mentira: o score sobe 0,1 por unidade de velocidade."""

    name, provider = "fake", "test"

    def predict(self, rows):
        return [min(1.0, 0.1 * row["cp_card_term_vel_1h"]) for row in rows]


def _row(**changes):
    return {**{name: 0 for name in FEATURE_NAMES}, **changes}


def test_factor_is_the_score_drop_when_the_field_goes_back_to_typical():
    result = explain(LinearModel(), _row(cp_card_term_vel_1h=7), baseline=_row(cp_card_term_vel_1h=2))

    assert round(result.score, 4) == 0.7
    assert [(f.feature, f.contribution) for f in result.factors] == [("cp_card_term_vel_1h", 0.5)]


def test_fields_already_at_the_typical_value_are_not_factors():
    result = explain(LinearModel(), _row(cp_card_term_vel_1h=2, hora=3), baseline=_row(cp_card_term_vel_1h=2))

    assert [f.feature for f in result.factors] == ["hora"]
    assert result.factors[0].contribution == 0
