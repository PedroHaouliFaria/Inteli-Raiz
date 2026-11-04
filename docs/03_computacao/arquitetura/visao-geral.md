# Arquitetura do Watson

Aprovada pelo Leo em 27/10/2026. O código fica em `watson/`, a documentação em `docs/`, e o backend é Python + FastAPI com o banco trocável entre PostgreSQL e Db2.

> **Revisão de estrutura em 04/11/2026:** a documentação está organizada por área em [docs/](../../README.md). O inventário atual de componentes, política e contratos está em [D09](../D09_estrutura_solucao.md) e [D10](../D10_arquitetura.md). Esta visão preserva decisões originais; o runtime atual de demo usa SQLite e chat Pydantic AI/Groq, sem presumir serviços externos executados.

## Camadas

1. **Frontend** (`watson/frontend`): React + Carbon. Só conversa com a API, por HTTP + JSON, seguindo o contrato OpenAPI que o backend gera.
2. **API** (`watson/backend/app/api`): recebe, valida e responde.
3. **Domínio** (`watson/backend/app/domain`): as regras do negócio, sem FastAPI nem SQL.
4. **Agentes, risco e dados** (`app/agents`, `app/risk`, `app/db`): o domínio usa cada um por uma interface.
5. **Serviços de fora**: watsonx.ai (modelos Granite e o modelo de risco implantado), o banco (PostgreSQL ou Db2) e o dataset do case.

## Árvore

```
(raiz do repositório)
├── docs/                          ← toda a documentação, em português, por área
│   ├── 01_negocios/               ← D01, D04, D05, D07, D08 e canvas de proposta de valor
│   ├── 02_ux_design/              ← D02, D03, D06, D12, D13, pesquisa e processo_design/
│   ├── 03_computacao/             ← D09–D11, arquitetura/ (esta visão e decisoes/) e specs/
│   ├── 04_dados_e_modelo/         ← análise, base, modelo e dados/
│   ├── 05_gestao/                 ← plano, direcional, pendências, evidências/hipóteses e planejamento
│   └── 06_evidencias/             ← logs e ambiente das execuções
│
└── watson/                        ← todo o código da aplicação, em inglês
    ├── README.md
    ├── frontend/
    │   └── src/
    │       ├── app/               ← App.jsx, rotas, estilos globais
    │       ├── features/          ← uma pasta por tela: queue, board, case, member-app
    │       ├── components/        ← compartilhados: WatsonRail, Term, Glossary
    │       ├── api/               ← cliente HTTP do backend
    │       ├── state/             ← store do fluxo ponta a ponta
    │       └── mocks/             ← dados fictícios até cada tela ler da API
    ├── backend/
    │   ├── app/
    │   │   ├── main.py, config.py
    │   │   ├── api/routes/, api/schemas/
    │   │   ├── domain/            ← cases, decisions, notices, audit
    │   │   ├── agents/            ← providers (watsonx, simulated), prompts, tools
    │   │   ├── risk/
    │   │   ├── db/                ← tables, repositories, session, types, migrations (Alembic)
    │   │   └── simulation/
    │   └── tests/                 ← unit, integration
    └── infra/                     ← docker-compose, docker/, ibm-cloud/, ci/
```

As pastas `data/`, `notebooks/`, `scripts/` e `outputs/` do time de dados (branch `develop`) continuam na raiz, sem mudança.

## Regras

- Dependência numa direção só: `api` → `domain` → (`db`, `agents`, `risk`).
- Uma tela, uma pasta em `features/`; um componente só sobe para `components/` quando a segunda tela precisa dele.
- Rotas, pastas, arquivos, tabelas e colunas em inglês. Textos de tela e documentação em português.
- O banco muda só pela `DATABASE_URL`. Ver [decisão 0002](decisoes/0002-banco-trocavel.md).

## Decisões

| # | Decisão | Status |
|---|---|---|
| [0001](decisoes/0001-backend-fastapi.md) | Backend em Python + FastAPI | incorporada ao plano (28/10) |
| [0002](decisoes/0002-banco-trocavel.md) | Camada de dados trocável (SQLAlchemy); demonstração em SQLite | incorporada ao plano (28/10) |
| [0003](decisoes/0003-codigo-em-ingles.md) | Código e rotas em inglês | incorporada ao plano (28/10) |
| [0004](decisoes/0004-aviso-automatico-risco-medio.md) | Agente envia o aviso sozinho no risco médio; analista só nas exceções | substituída pela política conservadora do plano (28/10) |

Documento original da proposta: https://claude.ai/artifact/QBiEv2MbGhirTkKeDU8Wow
