"""
Ferramenta ADK: pontuar_transacao
Pontua uma transação no deployment WML e retorna probabilidade de fraude.
"""

import time
import requests

# ---------------------------------------------------------------------------
# Casos de teste extraídos de data/processed/teste_proporcao_real.csv.
# Ordem das 28 features conforme seção 4 da spec:
#   16 numéricas  → float | None (null JSON quando faltante)
#    9 categóricas → str   | "nan" (string quando faltante)
#    3 binárias    → 0 | 1
# card_presence_flag está no grupo categórico → "Y" / "N".
# mcc vai como string mesmo sendo dígitos.
# ---------------------------------------------------------------------------
CASOS = {
    "legitima": {
        # EVT_SYN_000043320  |  feedback_label = 0
        # --- 16 numéricas ---
        "amount":                      15.68,
        "amount_fees":                 0.46,
        "acceptor_risk":               24.0,
        "customer_presumed_income":    1200.0,
        "customer_reported_income":    1677.35,
        "account_available_credit":    4075.23,
        "account_balance":             6409.86,
        "card_credit_limit":           4874.97,
        "cardid_count_1m":             1.0,
        "cp_card_term_vel_1h":         4.0,
        "cp_card_prev_term_dist_1h":   12.92,
        "digitalwallettoken_count_3m": 10.0,
        "hora":                        18,
        "dia_semana":                  0,
        "valor_vs_media_cartao":       0.06785675646435141,
        "valor_vs_limite":             0.0032164300498259473,
        # --- 9 categóricas ---
        "tipo_transacao":              "credito",
        "modalidade_transacao":        "cartao_presente",
        "card_presence_flag":          "Y",
        "card_type":                   "credito",
        "card_brand":                  "BANDEIRA_A",
        "mcc":                         "5912",
        "acceptor_region":             "GO",
        "customer_risk_rating":        "baixo",
        "customer_region":             "SP",
        # --- 3 binárias ---
        "madrugada":                   0,
        "cnp_credito":                 0,
        "primeira_compra_cartao":      0,
    },
    "fraude": {
        # EVT_SYN_000094500  |  feedback_label = 1
        # --- 16 numéricas ---
        "amount":                      149.58,
        "amount_fees":                 2.09,
        "acceptor_risk":               70.0,
        "customer_presumed_income":    1964.73,
        "customer_reported_income":    3476.74,
        "account_available_credit":    664.75,
        "account_balance":             1295.91,
        "card_credit_limit":           14553.86,
        "cardid_count_1m":             30.0,
        "cp_card_term_vel_1h":         70.0,
        "cp_card_prev_term_dist_1h":   102.13,
        "digitalwallettoken_count_3m": 80.0,
        "hora":                        3,
        "dia_semana":                  6,
        "valor_vs_media_cartao":       None,    # vazio no CSV → numérica faltante
        "valor_vs_limite":             0.010277685782328537,
        # --- 9 categóricas ---
        "tipo_transacao":              "credito",
        "modalidade_transacao":        "cartao_nao_presente",
        "card_presence_flag":          "N",
        "card_type":                   "credito",
        "card_brand":                  "BANDEIRA_A",
        "mcc":                         "5411",
        "acceptor_region":             "nan",   # vazio no CSV → categórica faltante
        "customer_risk_rating":        "baixo",
        "customer_region":             "SP",
        # --- 3 binárias ---
        "madrugada":                   1,
        "cnp_credito":                 1,
        "primeira_compra_cartao":      1,
    },
}

_FEATURE_ORDER = list(CASOS["legitima"].keys())  # 28 colunas na ordem da spec


def pontuar(api_key: str, wml_url: str, deployment_id: str, linha: dict) -> dict:
    """
    Função pura (sem ADK). Obtém token IAM, chama /predictions e devolve
    {"ok": True, "score": float, "predicao": int, "latencia_ms": int}
    ou {"ok": False, "etapa": str, "status_http": int|None, "erro": str}.
    Nunca lança exceção.
    """
    t0 = time.monotonic()

    # 1. Token IAM
    try:
        token_resp = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": api_key,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=20,
        )
        token_resp.raise_for_status()
        token = token_resp.json()["access_token"]
    except requests.HTTPError as exc:
        return {"ok": False, "etapa": "iam", "status_http": exc.response.status_code,
                "erro": str(exc.response.status_code)}
    except Exception as exc:
        return {"ok": False, "etapa": "iam", "status_http": None, "erro": type(exc).__name__}

    # 2. Payload na ordem exata de _FEATURE_ORDER
    values = [linha[col] for col in _FEATURE_ORDER]
    payload = {"input_data": [{"fields": _FEATURE_ORDER, "values": [values]}]}

    url = f"{wml_url}/ml/v4/deployments/{deployment_id}/predictions?version=2021-05-01"

    # 3. Chamada ao deployment
    try:
        pred_resp = requests.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=20,
        )
        pred_resp.raise_for_status()
        body = pred_resp.json()
    except requests.HTTPError as exc:
        return {"ok": False, "etapa": "predictions", "status_http": exc.response.status_code,
                "erro": str(exc.response.status_code)}
    except Exception as exc:
        return {"ok": False, "etapa": "predictions", "status_http": None, "erro": type(exc).__name__}

    # 4. Localiza "probability" e "prediction" pelo índice em fields
    try:
        output = body["predictions"][0]
        fields = output["fields"]
        values_out = output["values"][0]
        prob_idx = fields.index("probability")
        pred_idx = fields.index("prediction")
        score = float(values_out[prob_idx][1])
        predicao = int(values_out[pred_idx])
    except Exception as exc:
        return {"ok": False, "etapa": "resposta", "status_http": None, "erro": type(exc).__name__}

    latencia_ms = int((time.monotonic() - t0) * 1000)
    return {"ok": True, "score": score, "predicao": predicao, "latencia_ms": latencia_ms}


# ---------------------------------------------------------------------------
# Bloco ADK — carregado só quando o ambiente Orchestrate estiver presente.
# Sem o ADK, `from pontuar_transacao import pontuar, CASOS` funciona normal.
# ---------------------------------------------------------------------------
try:
    from ibm_watsonx_orchestrate.agent_builder.tools import tool
    from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
    from ibm_watsonx_orchestrate.run import connections

    APP_ID = "wml_fraude"

    @tool(expected_credentials=[{"app_id": APP_ID, "type": ConnectionType.KEY_VALUE}])
    def pontuar_transacao(caso: str) -> dict:
        """
        Pontua uma transação de teste no modelo de detecção de fraudes no watsonx.ai.

        Passe caso="fraude" para pontuar EVT_SYN_000094500 (esperado: score ≥ 0,80)
        ou caso="legitima" para pontuar EVT_SYN_000043320 (esperado: score < 0,30).

        Retorna um dict com ok, score, predicao e latencia_ms em caso de sucesso,
        ou ok=False com etapa e erro em caso de falha.
        """
        if caso not in CASOS:
            return {
                "ok": False,
                "etapa": "entrada",
                "status_http": None,
                "erro": f"caso '{caso}' inválido; use 'fraude' ou 'legitima'",
            }

        try:
            creds = connections.key_value(APP_ID)  # dict: api_key, wml_url, deployment_id
            api_key = creds["api_key"]
            wml_url = creds["wml_url"]
            deployment_id = creds["deployment_id"]
        except Exception as exc:
            return {"ok": False, "caso": caso, "etapa": "credenciais",
                    "status_http": None, "erro": type(exc).__name__}

        resultado = pontuar(api_key, wml_url, deployment_id, CASOS[caso])
        resultado["caso"] = caso
        return resultado

except ImportError:
    pass  # ADK não instalado — pontuar() e CASOS continuam importáveis
