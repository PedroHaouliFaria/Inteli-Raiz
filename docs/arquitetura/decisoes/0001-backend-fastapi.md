# 0001 · Backend em Python + FastAPI

**Status:** proposta pelo Leo em 27/10/2026 e incorporada ao plano no [alinhamento de 28/10](../../plano_implementacao.md#alinhamento-com-o-watson-2810).

## Contexto
O backend serve a API do console e do app do associado, roda os agentes (watsonx.ai) e usa o modelo de risco, e precisa funcionar com PostgreSQL e com Db2.

## Opções
| | Python + FastAPI | TypeScript + NestJS | Java + Spring Boot |
|---|---|---|---|
| watsonx | SDK oficial `ibm-watsonx-ai` | SDK Node, menos exemplos | REST |
| PostgreSQL ↔ Db2 | SQLAlchemy + `ibm_db_sa` | Prisma/Drizzle não falam Db2 | JPA cobre os dois |
| Modelo de risco | mesmo ecossistema dos notebooks | precisaria de um serviço em Python | precisaria de um serviço em Python |

## Decisão
Python + FastAPI: API, agentes e modelo na mesma linguagem, OpenAPI gerado dos esquemas Pydantic e pouco código de estrutura para 5 pessoas.

## Consequências
O projeto tem duas linguagens (JavaScript no frontend, Python no resto). O frontend consome o contrato OpenAPI em `/docs`.
