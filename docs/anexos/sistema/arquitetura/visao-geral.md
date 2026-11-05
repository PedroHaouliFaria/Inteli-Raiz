# Arquitetura do Watson

Aprovada pelo Leo em 27/10/2026. O código fica em `watson/`, a documentação principal em `docs/documentacao-do-projeto.md` e seus detalhes em `docs/anexos/`. O backend usa Python + FastAPI e SQLAlchemy; SQLite é o padrão local e PostgreSQL é usado pelo Compose. Db2 permanece como possibilidade histórica, sem execução comprovada nesta revisão.

> **Revisão de estrutura em 04/11/2026:** a documentação está organizada por área em [docs/](../../../README.md). O inventário atual de componentes, política e contratos está em [D09](../requisitos-da-solucao.md) e [D10](../arquitetura-do-sistema.md). Esta visão preserva decisões originais; o desenvolvimento local usa SQLite por padrão, o Compose configura PostgreSQL e o chat usa Pydantic AI/Groq, sem presumir serviços externos executados.

## Camadas

1. **Frontend** (`watson/frontend`): React + Carbon. Só conversa com a API, por HTTP + JSON, seguindo o contrato OpenAPI que o backend gera.
2. **API** (`watson/backend/app/api`): recebe, valida e responde.
3. **Domínio** (`watson/backend/app/domain`): as regras do negócio, sem FastAPI nem SQL.
4. **Agentes, risco e dados** (`app/agents`, `app/risk`, `app/db`): o domínio usa cada um por uma interface.
5. **Serviços de fora**: Groq no chat atual, com modelo de risco local. O deploy watsonx.ai e as opções de Db2 ficam identificados como históricos; não são dependências presumidas do fluxo integrado.

## Árvore

```
(raiz do repositório)
├── docs/
│   ├── documentacao-do-projeto.md   ← leitura principal: historia, decisoes e resultados
│   └── anexos/                    ← detalhes tecnicos e fontes
│       ├── produto/
│       ├── experiencia-do-usuario/
│       ├── sistema/
│       ├── dados-e-modelo/
│       ├── gestao/
│       ├── evidencias/
│       └── historico/
│
└── watson/                        ← todo o código da aplicação, em inglês
    ├── README.md
    ├── frontend/
    │   └── src/
    │       ├── app/               ← App.jsx, rotas, estilos globais
    │       ├── features/          ← session, associate e analyst; console antigo em queue, board, case e member-app
    │       ├── components/        ← compartilhados: WatsonRail, Term, Glossary
    │       ├── api/               ← cliente HTTP do backend
    │       ├── state/             ← estado do console legado; fluxo atual usa o cliente HTTP
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
