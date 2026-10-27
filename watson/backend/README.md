# backend

API do Watson em Python + FastAPI: regras de negócio, agentes (watsonx.ai) e acesso ao banco.

```bash
cd watson/backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,postgres]"     # use ".[dev,db2]" para Db2 e ".[watsonx]" para o agente real
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
