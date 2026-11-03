# Documentação: Prevenção Inteligente a Fraudes (Sicredi)

Documentação do projeto da Trilha 4 do **IBM AI Experiential Learning Lab 2026**, desenvolvido na optativa IBM do Inteli.

## Análise de dados e modelo

| # | Documento | Conteúdo |
|---|---|---|
| 01 | [Análise Exploratória](01_analise_exploratoria.md) | Linha de raciocínio, decisões e insights sobre os dados de transações |
| 02 | [Base Balanceada](02_base_balanceada.md) | Construção das bases de treino/teste e as 7 features criadas a partir dos insights |
| 03 | [Modelo](03_modelo.md) | Pipeline de pré-processamento, Random Forest, avaliação por PR-AUC e análise crítica dos resultados |

## Produto e implementação

- [Plano revisado: confirmação de compras pelo associado](plano_implementacao.md) — produto, fluxo, regras, contratos, requisitos e testes.
- [Direcional das entregas D01–D13](direcional_entregas.md) — estruturas, instruções, fontes, responsáveis e critérios de qualidade para as 13 entregas.
- [Versão em PDF do plano — v2 de 23/10/2026](plano_implementacao.pdf) — a ampliação de 27/10 está apenas no Markdown acima.

O sistema avalia a compra e decide o tratamento inicial; o associado autoriza, recusa ou informa dúvida, e o analista trata exceções. Ações financeiras são simuladas no MVP.

## Especificações técnicas

| Documento | Conteúdo |
|---|---|
| [Contrato da API JSON](specs/contrato_api.md) | Endpoints, estados, erros e exemplos de resposta |
| [Spec: teste de integração Orchestrate → watsonx.ai](specs/teste_integracao_orchestrate_wml.md) | Como provar que o Orchestrate consegue chamar o modelo no watsonx.ai |

## Planejamento

| Documento | Conteúdo |
|---|---|
| [Backlog](planejamento/backlog.md) | Cards C01–C32 com responsáveis, dependências e critérios de aceite |
| [Plano operacional](planejamento/plano_15_dias.md) | Sequência por etapas, divisão em quatro pessoas e critérios de passagem |
| [Artefatos e materiais de contexto](planejamento/artefatos_materiais_contexto.md) | Mapa das entregas identificadas nos materiais IBM |

## Arquitetura

- [Visão geral](arquitetura/visao-geral.md) — camadas, árvore do repositório e regras.
- Decisões de arquitetura (ADR):

| # | Decisão | Status |
|---|---|---|
| [0001](arquitetura/decisoes/0001-backend-fastapi.md) | Backend em Python + FastAPI | incorporada ao plano |
| [0002](arquitetura/decisoes/0002-banco-trocavel.md) | Banco trocável via SQLAlchemy; SQLite na demo | incorporada ao plano |
| [0003](arquitetura/decisoes/0003-codigo-em-ingles.md) | Código e rotas em inglês | incorporada ao plano |
| [0004](arquitetura/decisoes/0004-aviso-automatico-risco-medio.md) | Aviso automático no risco médio | **substituída** — política conservadora vigente |

## Dados

| Documento | Conteúdo |
|---|---|
| [Levantamento de dados](dados/levantamento-de-dados.md) | Cada dado ligado à necessidade de uma persona ou tela |
| [Modelo de dados](dados/modelo-de-dados.md) | Diagrama relacional, entidades, atributos e decisões em aberto |
| [Como os dados já foram usados](dados/como-os-dados-ja-foram-usados.md) | EDA, base balanceada, modelo RF e integração com o watsonx |
| [Linha do tempo do cartão](dados/linha-do-tempo.md) | Se o case permite montar a linha do tempo de um cartão |
| [Uso dos dados na aplicação](dados/uso-dos-dados-na-aplicacao.md) | Caminho do CSV do case até a tela |

## Design

Processo de Design Thinking em cinco etapas, dentro de [`design/`](design/):

| Pasta | Conteúdo |
|---|---|
| [`00-descoberta/`](design/00-descoberta/README.md) | Personas, mapas de empatia, cenário as-is, Hills e POV, anti-persona |
| [`01-wireframe/`](design/01-wireframe/README.md) | Três versões de wireframe (A, B, C) para app e console |
| [`02-mockup/`](design/02-mockup/README.md) | Três versões de mockup |
| [`03-prototipo/`](design/03-prototipo/README.md) | Fluxos de protótipo |
| [`04-alta-fidelidade/`](design/04-alta-fidelidade/README.md) | Telas de alta fidelidade |
| [`05-laboratorio-do-modelo/`](design/05-laboratorio-do-modelo/README.md) | Bancada, "e se" e explorador do modelo |
| [`glossario.md`](design/glossario.md) | Termos do projeto |
| [`agentes/arquitetura-de-agentes.md`](design/agentes/arquitetura-de-agentes.md) | Arquitetura de agentes |

## Entregas por pessoa

Cada pasta contém as entregas D01–D13 organizadas por responsável, com README de índice, registro de evidências/hipóteses e estado de cada documento.

| Pasta | Responsável | Entregas | Estado |
|---|---|---|---|
| [entregas/pessoa1/](entregas/pessoa1/README.md) | Pessoa 1 — Negócios, produto e narrativa | D01, D04, D05, D07, D08 | rascunho |
| [entregas/pessoa2/](entregas/pessoa2/README.md) | Pessoa 2 — Pesquisa e compreensão do usuário | D02, D03, D06 | rascunho — pesquisa não executada |
| [entregas/pessoa3/](entregas/pessoa3/README.md) | Pessoa 3 — Estrutura da solução e arquitetura | D09, D10 | rascunho |
| [entregas/pessoa4/](entregas/pessoa4/README.md) | Pessoa 4 — Protótipo, fluxo e validação | D11, D12, D13 | D12 revisado; D11 bloqueado; D13 protocolo pronto |

## Estrutura completa de `docs/`

```
docs/
├── 01_analise_exploratoria.md
├── 02_base_balanceada.md
├── 03_modelo.md
├── plano_implementacao.md
├── plano_implementacao.pdf
├── direcional_entregas.md
├── README.md                  ← este arquivo
│
├── arquitetura/               ← visão geral e decisões ADR
│   ├── visao-geral.md
│   └── decisoes/
│
├── assets/                    ← imagens dos documentos de dados/modelo
│
├── dados/                     ← modelo de dados, levantamento e uso na aplicação
│
├── design/                    ← Design Thinking: descoberta → alta fidelidade
│   ├── 00-descoberta/
│   ├── 01-wireframe/
│   ├── 02-mockup/
│   ├── 03-prototipo/
│   ├── 04-alta-fidelidade/
│   ├── 05-laboratorio-do-modelo/
│   ├── agentes/
│   ├── glossario.md
│   └── skills/
│
├── entregas/                  ← entregas D01–D13 por pessoa
│   ├── pessoa1/               ← D01, D04, D05, D07, D08
│   ├── pessoa2/               ← D02, D03, D06
│   ├── pessoa3/               ← D09, D10
│   └── pessoa4/               ← D11, D12, D13
│
├── planejamento/              ← backlog, plano operacional e mapa de artefatos
│
└── specs/                     ← contrato da API e spec de integração
```

> O CSV original (~290 MB) **não é versionado**. Para rodar os notebooks, coloque `case_transacoes_cartoes_sintetico_900k.csv` em `data/`. Para regerar as figuras: `python scripts/gerar_figuras_docs.py`.
