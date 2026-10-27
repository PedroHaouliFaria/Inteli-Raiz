"""As 28 entradas do modelo de risco, na ordem do pipeline (notebooks/03_modelo, seção 4 da spec)."""

from dataclasses import dataclass
from enum import StrEnum


class FeatureKind(StrEnum):
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    BINARY = "binary"


@dataclass(frozen=True)
class Feature:
    name: str
    label: str
    group: str
    kind: FeatureKind


_N, _C, _B = FeatureKind.NUMERIC, FeatureKind.CATEGORICAL, FeatureKind.BINARY

FEATURES: tuple[Feature, ...] = (
    Feature("amount", "Valor da compra (R$)", "Contexto da compra", _N),
    Feature("amount_fees", "Tarifa (R$)", "Contexto da compra", _N),
    Feature("acceptor_risk", "Risco do estabelecimento", "Estabelecimento", _N),
    Feature("customer_presumed_income", "Renda presumida (R$)", "Associado e conta", _N),
    Feature("customer_reported_income", "Renda declarada (R$)", "Associado e conta", _N),
    Feature("account_available_credit", "Crédito disponível (R$)", "Associado e conta", _N),
    Feature("account_balance", "Saldo da conta (R$)", "Associado e conta", _N),
    Feature("card_credit_limit", "Limite do cartão (R$)", "Associado e conta", _N),
    Feature("cardid_count_1m", "Contagem do cartão (1m)", "Velocidade e distância", _N),
    Feature("cp_card_term_vel_1h", "Uso cartão × terminal (1h)", "Velocidade e distância", _N),
    Feature("cp_card_prev_term_dist_1h", "Distância do terminal anterior (1h)", "Velocidade e distância", _N),
    Feature("digitalwallettoken_count_3m", "Tokens de carteira digital (3m)", "Velocidade e distância", _N),
    Feature("hora", "Hora", "Contexto da compra", _N),
    Feature("dia_semana", "Dia da semana (0 = segunda)", "Contexto da compra", _N),
    Feature("valor_vs_media_cartao", "Valor ÷ média do cartão", "Sinais criados pela equipe", _N),
    Feature("valor_vs_limite", "Valor ÷ limite", "Sinais criados pela equipe", _N),
    Feature("tipo_transacao", "Tipo", "Contexto da compra", _C),
    Feature("modalidade_transacao", "Modalidade", "Contexto da compra", _C),
    Feature("card_presence_flag", "Cartão presente", "Contexto da compra", _C),
    Feature("card_type", "Tipo do cartão", "Contexto da compra", _C),
    Feature("card_brand", "Bandeira", "Contexto da compra", _C),
    Feature("mcc", "MCC (ramo do estabelecimento)", "Estabelecimento", _C),
    Feature("acceptor_region", "UF do estabelecimento", "Estabelecimento", _C),
    Feature("customer_risk_rating", "Classificação de risco do associado", "Associado e conta", _C),
    Feature("customer_region", "UF do associado", "Associado e conta", _C),
    Feature("madrugada", "Madrugada", "Sinais criados pela equipe", _B),
    Feature("cnp_credito", "Crédito sem cartão presente", "Sinais criados pela equipe", _B),
    Feature("primeira_compra_cartao", "Primeira compra do cartão", "Sinais criados pela equipe", _B),
)

FEATURE_NAMES: tuple[str, ...] = tuple(f.name for f in FEATURES)
BY_NAME: dict[str, Feature] = {f.name: f for f in FEATURES}

# Como o notebook 03 e a ferramenta do agente mandam um categórico vazio.
MISSING_CATEGORY = "nan"


def normalize(row: dict) -> dict:
    """Deixa uma transação no formato que o pipeline espera: numérico vazio = None, categórico vazio = "nan"."""
    missing = [name for name in FEATURE_NAMES if name not in row]
    if missing:
        raise ValueError(f"faltam campos: {', '.join(missing)}")
    out: dict = {}
    for f in FEATURES:
        value = row[f.name]
        if f.kind is FeatureKind.CATEGORICAL:
            out[f.name] = MISSING_CATEGORY if value is None or value == "" else str(value)
        elif f.kind is FeatureKind.BINARY:
            out[f.name] = None if value is None else int(bool(value))
        else:
            out[f.name] = None if value is None or value == "" else float(value)
    return out
