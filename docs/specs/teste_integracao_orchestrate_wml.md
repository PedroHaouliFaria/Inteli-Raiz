# Spec: teste de integração Orchestrate → watsonx.ai

> **Encerrada em 27/10/2026.** O orientador revogou a obrigatoriedade do IBM Cloud porque o Orchestrate não está funcionando para muitos grupos. O agente e o modelo passam para o nosso backend (ver §4 do [`plano_implementacao.md`](../plano_implementacao.md)). Esta spec fica como evidência: o teste 7.1 contra o watsonx.ai passou, e os passos do Orchestrate não rodaram. O `agente/agents/agente_teste.yaml` é histórico.

> **Prazo:** 24/10/2026. **Responsável:** Lucas (ferramenta e agente), Pedro R. (modelo implantado).
> **Pergunta que o teste responde:** uma ferramenta Python rodando no watsonx Orchestrate (Tóquio) consegue pegar um token IAM e receber um score do modelo implantado no watsonx.ai Runtime (Dallas)?
> Se sim, seguimos com o modelo no watsonx.ai. Se não, ativamos o plano B (score por regras dentro da ferramenta).

## 1. Critério de aprovação

O teste passa quando **todos** os itens abaixo forem verdadeiros:

1. `orchestrate tools import` aceita o `requirements.txt` (a allowlist do tenant libera `requests`).
2. No preview do agente, o pedido "pontue a transação de teste" devolve `ok: true` e `score` ≥ 0,80 para o caso de fraude `EVT_SYN_000094500`.
3. O caso legítimo `EVT_SYN_000043320` devolve `score` < 0,30.
4. A resposta chega em menos de 10 s. A primeira chamada do dia pode demorar mais, porque o deploy fica ocioso após 1 dia; vale a segunda.

Se o item 1 ou 2 falhar e não houver correção até 24/10, ativar o plano B.

## 2. Pré-requisitos

**Do Pedro R. (modelo):** feito no PR #6, já na `develop`.

- [x] Ler os CSVs com as 9 categóricas como texto: `pd.read_csv(..., dtype={c: str for c in FEATURES_CAT})`. Hoje o `mcc` tem 1 vazio no treino, o pandas lê a coluna como `float` e o encoder aprende `"5411.0"`. A ferramenta manda `"5411"`, que cairia como categoria desconhecida (`-1`) sem nenhum erro.
- [x] Retreinar o pipeline do `notebooks/03_modelo.ipynb` com `scikit-learn==1.6.*` em Python 3.12.
- [x] **Remover o `FunctionTransformer(lambda X: X.astype(str))`** do `pipe_cat`. Lambda não é serializável, e o `store_model` vai falhar. Em vez disso, converter as categóricas para `str` no pandas **antes** do `fit`:
  `X_treino[FEATURES_CAT] = X_treino[FEATURES_CAT].astype(str)`. O resultado é idêntico ao atual: o `astype(str)` já transformava `NaN` em `"nan"`.
- [x] Implantar no deployment space com model type `scikit-learn_1.6` e software spec `runtime-25.1-py3.12`, como deploy **online**. Feito com `scripts/deploy_watsonx.py`.
- [x] Passar ao Lucas: `deployment_id` e a ordem exata das colunas (`TODAS_FEATURES`, seção 4). `deployment_id` = `01a17dba-b0c2-7778-b2ca-fa8e3ad07593`; a ordem bate com a seção 4.

**Do Lucas:**

- [x] Uma **API key da IBM Cloud** (IBM Cloud → Manage → Access (IAM) → API keys) de um usuário que seja membro do deployment space. Essa chave **não é** a do Orchestrate.
- [ ] A **service instance URL** e a **API key do Orchestrate**: na instância do Orchestrate, ícone do usuário → Settings → aba **API details** → Generate API key. Bloqueado: o trial expirou em 27/10.
- [x] Python 3.12 em um venv com:
  ```bash
  pip install ibm-watsonx-orchestrate==2.19.0 requests==2.32.4
  ```

Nenhuma chave entra no repositório nem no código. Elas ficam só na connection do Orchestrate e em variáveis de ambiente locais.

## 3. Arquivos

```
agente/
  tools/
    pontuar_transacao.py     # ferramenta do teste
    requirements.txt         # requests==2.32.4
  agents/
    agente_teste.yaml        # agente mínimo só para chamar a ferramenta
```

## 4. Contrato com o watsonx.ai

**Token IAM**

```
POST https://iam.cloud.ibm.com/identity/token
Content-Type: application/x-www-form-urlencoded
grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=<IBM Cloud API key>
→ {"access_token": "...", "expires_in": 3600, ...}
```

**Predição**

```
POST {wml_url}/ml/v4/deployments/{deployment_id}/predictions?version=2021-05-01
Authorization: Bearer <access_token>
Content-Type: application/json
```

`wml_url` = `https://us-south.ml.cloud.ibm.com`.

Corpo: `fields` na ordem exata abaixo, uma linha em `values`.

```json
{"input_data": [{"fields": ["amount", "amount_fees", "acceptor_risk", "customer_presumed_income", "customer_reported_income", "account_available_credit", "account_balance", "card_credit_limit", "cardid_count_1m", "cp_card_term_vel_1h", "cp_card_prev_term_dist_1h", "digitalwallettoken_count_3m", "hora", "dia_semana", "valor_vs_media_cartao", "valor_vs_limite", "tipo_transacao", "modalidade_transacao", "card_presence_flag", "card_type", "card_brand", "mcc", "acceptor_region", "customer_risk_rating", "customer_region", "madrugada", "cnp_credito", "primeira_compra_cartao"], "values": [[...]]}]}
```

Regras de tipo:

- **16 numéricas** (as primeiras): `float`, ou `null` quando faltar (o imputer usa a mediana).
- **9 categóricas**: `string`, e o valor faltante vai como `"nan"`, não `null`, para bater com o treino. `mcc` também vai como string (`"5411"`).
- **3 binárias** (as últimas): `0` ou `1`.

**Resposta esperada:**

```json
{"predictions": [{"fields": ["prediction", "probability"], "values": [[1, [0.03, 0.97]]]}]}
```

`score` = `probability[1]`. Localizar `"probability"` pelo índice em `fields`, não por posição fixa. Formato confirmado numa chamada real em 27/10: `{"predictions": [{"fields": ["prediction", "probability"], "values": [[1, [0.0083, 0.9917]]]}]}`.

## 5. Os dois casos fixos

Vêm de `data/processed/teste_proporcao_real.csv`. Ficam embutidos na ferramenta como dicts, já com os tipos da seção 4.

| Caso | `event_external_id` | Rótulo | Por que |
|---|---|---|---|
| `fraude` | `EVT_SYN_000094500` | fraude | crédito sem cartão presente, 3h, primeira compra do cartão, `acceptor_region` e `valor_vs_media_cartao` vazios (testa os nulos) |
| `legitima` | `EVT_SYN_000043320` | legítima | crédito presencial, 18h, sem nenhum campo vazio |

Os valores de cada coluna estão nas linhas desses IDs no CSV.

## 6. A ferramenta `pontuar_transacao`

**Separar a lógica em duas partes**, para testar o watsonx.ai localmente antes de envolver o Orchestrate:

1. `pontuar(api_key, wml_url, deployment_id, linha) -> dict`: função pura que pega o token, monta o payload e chama `/predictions`. Não depende do ADK.
2. `pontuar_transacao(caso: str) -> dict`: a ferramenta decorada, que lê a connection e chama `pontuar`.

**Entrada da ferramenta:** `caso` ∈ {`"fraude"`, `"legitima"`}. Docstring em português explicando isso, porque o agente usa a docstring para decidir a chamada.

**Saída** (sempre um `dict`, nunca uma exceção para o agente):

```python
# sucesso
{"ok": True, "caso": "fraude", "score": 0.97, "predicao": 1, "latencia_ms": 812}
# falha
{"ok": False, "caso": "fraude", "etapa": "iam" | "predictions" | "resposta", "status_http": 401, "erro": "<mensagem curta>"}
```

O campo `erro` **nunca** traz a API key, o token ou cabeçalhos.

**Partes fixas do ADK** (confirmadas na doc e no código do ADK 2.19):

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections

APP_ID = "wml_fraude"

@tool(expected_credentials=[{"app_id": APP_ID, "type": ConnectionType.KEY_VALUE}])
def pontuar_transacao(caso: str) -> dict:
    creds = connections.key_value(APP_ID)  # dict: api_key, wml_url, deployment_id
    ...
```

**Outros requisitos:**

- `requests` com `timeout=20` em cada chamada. O limite da ferramenta no Orchestrate é 2 min.
- Sem cache de token. Cada chamada pede um token novo: é mais simples e o volume do teste é mínimo.
- O `requirements.txt` só tem `requests==2.32.4`, com versão exata.

## 7. Passo a passo

**7.1 Teste local da função `pontuar`** (prova IAM + watsonx.ai sem o Orchestrate):

```bash
export WML_API_KEY=... WML_URL=https://us-south.ml.cloud.ibm.com WML_DEPLOYMENT_ID=...
cd agente/tools
python -c "from pontuar_transacao import pontuar, CASOS; import os; print(pontuar(os.environ['WML_API_KEY'], os.environ['WML_URL'], os.environ['WML_DEPLOYMENT_ID'], CASOS['fraude']))"
```

Se falhar aqui, o problema está no token ou no deploy, não no Orchestrate. Nesse caso, falar com o Pedro R. antes de seguir.

**7.2 Apontar o CLI para a instância SaaS:**

```bash
orchestrate env add -n sicredi -u <service-instance-url> --type ibm_iam --activate
orchestrate env activate sicredi --api-key <API key do Orchestrate>
```

A sessão expira a cada 2 h. Quando expirar, repetir o `activate`.

**7.3 Criar a connection key_value:**

```bash
orchestrate connections add -a wml_fraude
orchestrate connections configure -a wml_fraude --env draft -t team -k key_value
orchestrate connections set-credentials -a wml_fraude --env draft \
  -e "api_key=<IBM Cloud API key>" \
  -e "wml_url=https://us-south.ml.cloud.ibm.com" \
  -e "deployment_id=<deployment_id>"
```

**7.4 Importar a ferramenta:**

```bash
orchestrate tools import -k python -f agente/tools/pontuar_transacao.py -r agente/tools/requirements.txt -a wml_fraude
```

Se der erro de allowlist, é **resultado do teste**: anotar a mensagem e avisar o grupo.

**7.5 Agente mínimo** (`agente/agents/agente_teste.yaml`):

```yaml
spec_version: v1
kind: native
name: agente_teste_integracao
description: Agente descartável para testar a chamada ao modelo de fraude no watsonx.ai.
instructions: |
  Quando o usuário pedir para pontuar a transação de teste, chame pontuar_transacao
  com caso "fraude" ou "legitima" e mostre o JSON retornado, sem interpretar.
tools:
  - pontuar_transacao
```

```bash
orchestrate agents import -f agente/agents/agente_teste.yaml
```

Sem `llm`, o agente usa o modelo padrão da instância.

**7.6 Testar no preview** da UI (Manage Agents → `agente_teste_integracao`), que usa as credenciais `draft`:

- "pontue a transação de teste de fraude" → espera `score` ≥ 0,80
- "pontue a transação de teste legítima" → espera `score` < 0,30
- repetir as duas e anotar a `latencia_ms`

## 8. O que registrar

Anotar no fim deste arquivo:

- o resultado de cada critério da seção 1;
- as latências;
- erros encontrados e as correções feitas;
- a decisão final: watsonx.ai ou plano B.

Exportar a sessão do Bob em `bob_sessions/lucas/`, com a captura do resumo de consumo.

## 9. Fora do teste

Os casos de demo (10 a 15), as faixas de decisão, os sinais explicativos, o workflow do analista e o agente final. A `pontuar_transacao` vira a base da `avaliar_transacao` depois que o teste passar.

## Resultado

### 27/10: watsonx.ai validado; Orchestrate bloqueado

**Modelo implantado** (PR #6, branch `modelo/sklearn-1.6`):

- Retreinado em Python 3.12.8, scikit-learn 1.6.1 e pandas 2.2.3, com as categóricas lidas como texto e sem a `lambda`.
- Publicado com `scripts/deploy_watsonx.py` no space "Inteli Raiz Space" (Dallas), como deploy online.
- `deployment_id` = `01a17dba-b0c2-7778-b2ca-fa8e3ad07593`.

**Teste 7.1** (`pontuar` local → IAM → `/predictions`), duas rodadas seguidas:

| Caso | Score | Predição | Latência 1ª | Latência 2ª | Critério |
|---|---|---|---|---|---|
| `fraude` | 0,9917 | 1 | 2.920 ms | 1.266 ms | ≥ 0,80 ✓ |
| `legitima` | 0,0089 | 0 | 1.129 ms | 1.162 ms | < 0,30 ✓ |

Os scores são idênticos aos do modelo local. As latências medidas vão do computador do Lucas até Dallas, não do Orchestrate.

**Critérios da seção 1:**

1. Allowlist do `requests` no `tools import`: **não testado.** O trial do watsonx Orchestrate expirou e o "Extend Trial" deu erro. O caso foi levado ao orientador.
2. e 3. Scores dos dois casos: **passam** na chamada direta ao watsonx.ai. Ainda falta passar pelo preview do agente.
4. Latência abaixo de 10 s: **passa** na chamada direta.

**Erros encontrados e correções:**

- O `store_model` do `ibm-watsonx-ai` 1.8.1 sobe o conteúdo com `httpx.put` sem timeout, e o padrão de 5 s do httpx estoura. O script aumenta esse timeout para 300 s.
- O deploy exigiu uma task credential (`missing_user_task_credential`). O script cria uma com a API key atual quando não existe nenhuma.

**Decisão (27/10, depois da mensagem do orientador):** o Orchestrate sai do escopo e o modelo passa a rodar no backend a partir do `joblib`. O deploy no watsonx.ai fica como evidência e como `score_source=watsonx` opcional.
