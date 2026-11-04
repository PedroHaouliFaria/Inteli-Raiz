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
- [Direcional das entregas D01–D13](../artefatos/documentacao/direcional_entregas.md) — estruturas, instruções, fontes, responsáveis e critérios de qualidade para as 13 entregas.
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
| [Artefatos e materiais de contexto](../artefatos/documentacao/fontes_e_exigencias_ibm.md) | Mapa das entregas identificadas nos materiais IBM |

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

Processo de Design Thinking em cinco etapas, dentro de [`design/`](design):

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

## Artefatos do projeto

As entregas ficam em [artefatos/](../artefatos/README.md), por ID D01–D13, com documentação e evidências comuns. Não há pastas de entregas por pessoa. O [direcional](../artefatos/documentacao/direcional_entregas.md) define o conteúdo; a [matriz de aceite](../artefatos/documentacao/criterios_e_pendencias.md) registra o que falta.

## Estrutura de apoio técnico

```text
docs/
├── README.md
├── 01_analise_exploratoria.md
├── 02_base_balanceada.md
├── 03_modelo.md
├── plano_implementacao.md
├── plano_implementacao.pdf       # fotografia antiga, conforme aviso acima
├── arquitetura/                 # visão geral e ADRs
├── assets/                      # figuras de dados/modelo
├── dados/                       # levantamento e uso dos dados
├── design/                      # materiais visuais de apoio
├── planejamento/                # backlog e plano operacional histórico
└── specs/                       # contrato JSON e teste histórico watsonx.ai
```

> O CSV original (~290 MB) não é versionado. Para os notebooks, coloque `case_transacoes_cartoes_sintetico_900k.csv` em `data/`. Para gerar figuras: `python scripts/gerar_figuras_docs.py`.
