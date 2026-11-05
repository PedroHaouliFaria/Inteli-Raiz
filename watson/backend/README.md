# backend

API do Watson em Python + FastAPI: confirmação de compras, revisão humana, agente de chat Pydantic AI/Groq e persistência via SQLAlchemy.

```bash
cd watson/backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,risk]"          # adicione postgres ao extra se configurar PostgreSQL
cp .env.example .env                  # troque SESSION_SECRET; sem DATABASE_URL, usa SQLite
uvicorn app.main:app --reload         # http://localhost:8000/docs
pytest
```

O chat integrado usa `GROQ_API_KEY`. Sem a chave, as compras e confirmações continuam funcionando, mas o chat responde `503 AGENT_UNAVAILABLE`. `WATSONX_API_KEY` é usada apenas pelo provider Watsonx e pelo deployment opcional do modelo de risco.

## Fluxo integrado

O associado entra por e-mail/senha fictícios, abre uma compra e responde AUTHORIZE, DENY ou UNSURE pelos controles da interface. Pedir atendimento é separado da resposta. A analista lista revisões e registra AUTHORIZE ou DENY em `POST /api/reviews/{review_id}/decision`; a compra e o histórico são atualizados na simulação. O agente consulta contexto e solicita revisão, sem responder à confirmação pelo associado.

Para usar a aplicação completa, consulte o [guia de demonstração](../../docs/anexos/sistema/como-usar-a-demonstracao.md). O [contrato da API](../../docs/anexos/sistema/specs/contrato-da-api.md) detalha identidade, estados, erros e respostas.

## Login da demonstração

| Usuário | Perfil | E-mail | Senha |
|---|---|---|---|
| Ana Souza | Associado | `ana@raiz.demo` | `Ana@123` |
| Bruno Lima | Associado | `bruno@raiz.demo` | `Bruno@123` |
| Carla Reis | Analista | `carla@raiz.demo` | `Carla@123` |

Os valores ficam em `.env` pelas variáveis `MOCK_<PESSOA>_EMAIL` e `MOCK_<PESSOA>_PASSWORD`; o `.env.example` contém os mesmos valores para facilitar a configuração. São credenciais fictícias e não devem ser usadas em produção.

## Pastas

| Pasta | Papel |
|---|---|
| `app/api/routes/` | Camada HTTP: uma rota por recurso. Só recebe, valida e responde |
| `app/api/schemas/` | Modelos Pydantic, o contrato com o frontend (OpenAPI em `/docs`) |
| `app/domain/` | Regras do negócio (`cases`, `decisions`, `notices`, `audit`). Sem FastAPI e sem SQL |
| `app/domain/agent/` | Chat integrado Pydantic AI/Groq, contexto autorizado e ferramenta de revisão |
| `app/agents/` | Providers, prompts e ferramentas do console legado; não representam o chat integrado atual |
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
