# backend

API do Watson em Python + FastAPI: regras de negócio, agentes (watsonx.ai) e acesso ao banco.

```bash
cd watson/backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,postgres,risk]" # use ".[dev,db2]" para Db2, ".[watsonx]" para o agente real; "risk" roda o modelo de risco local
cp .env.example .env                  # sem .env, usa SQLite local e o agente simulado
uvicorn app.main:app --reload         # http://localhost:8000/docs
pytest
```

## Pastas

| Pasta | Papel |
|---|---|
| `app/api/routes/` | Camada HTTP: uma rota por recurso. Só recebe, valida e responde |
| `app/api/schemas/` | Modelos Pydantic, o contrato com o frontend (OpenAPI em `/docs`) |
| `app/domain/` | Regras do negócio (`cases`, `decisions`, `notices`, `audit`). Sem FastAPI e sem SQL |
| `app/agents/` | Agentes do produto, com `providers/` (watsonx ou simulado), `prompts/` versionados e `tools/` só de leitura |
| `app/risk/` | Score em tempo de execução: carrega o modelo, calcula sinais e fatores |
| `app/db/` | Camada trocável: `tables/`, `repositories/`, `session.py`, `types.py` e `migrations/` (Alembic) |
| `app/simulation/` | Carga do case, chegada simulada de transações e aparelhos do app |
| `tests/unit/`, `tests/integration/` | Testes do domínio e da API com banco |

## Regras

- Dependência numa direção só: `api` chama `domain`, que usa `db`, `agents` e `risk`.
- Código, rotas, tabelas e colunas em inglês; textos para o usuário em português.
- O banco muda só pela `DATABASE_URL`. Use tipos portáveis: enums como texto e JSON pelo `PortableJSON`.
- Migrações: `alembic revision --autogenerate -m "..."` e `alembic upgrade head`.

## Modelo de risco e Laboratório do modelo

- `RISK_MODEL_PROVIDER=local` (padrão) lê `outputs/modelo_rf.joblib` na raiz do repositório, o mesmo arquivo publicado no watsonx.ai. Precisa do extra `risk` (scikit-learn 1.6.1, a versão do treino).
- `RISK_MODEL_PROVIDER=watsonx` chama o deployment online: defina `WATSONX_API_KEY` e `RISK_WATSONX_DEPLOYMENT_ID` (saída de `scripts/deploy_watsonx.py`).
- As rotas `/model-lab/*` alimentam a aba Laboratório do modelo: `info` (campos, faixas, limiares), `samples` (busca e sorteio no conjunto de teste de `data/processed/`) e `score` (score, faixa e fatores).
- Fatores: quanto o score cai se só aquele campo volta ao valor típico das compras legítimas do treino (mediana ou moda). É uma conta nossa, não do Random Forest.
