# Inteli-Raiz

**Raiz: confirmação assistida de compras para associados do Sicredi.** Projeto da optativa IBM do Inteli (IBM AI Experiential Learning Lab 2026, desafio Sicredi de prevenção a fraudes), com dados sintéticos e ações financeiras simuladas.

## Acesso rápido

| O que | Onde |
|---|---|
| Aplicação publicada | <https://raiz-jq28.onrender.com> (no primeiro acesso, o servidor pode levar até 1 minuto para acordar) |
| Vídeo de demonstração | [demonstracao/](demonstracao/README.md), com o arquivo e o link do Google Drive |
| Documentação completa | [docs/documentacao-do-projeto.md](docs/documentacao-do-projeto.md) |
| Tecnologias usadas | [docs/tecnologias.md](docs/tecnologias.md) |
| Passo a passo da demonstração | [Guia de uso](docs/anexos/sistema/como-usar-a-demonstracao.md) |

Logins fictícios da demonstração:

| Perfil | E-mail | Senha |
|---|---|---|
| Associado (Ana Souza) | `ana@raiz.demo` | `Ana@123` |
| Associado (Bruno Lima) | `bruno@raiz.demo` | `Bruno@123` |
| Analista (Carla Reis) | `carla@raiz.demo` | `Carla@123` |

## O projeto em poucas linhas

Quando uma compra no cartão é sinalizada como suspeita, o associado precisa decidir se a reconhece, muitas vezes com pouco contexto. O Raiz apresenta a compra e os motivos do alerta em linguagem simples, oferece três respostas explícitas (**Reconheço e autorizo**, **Não reconheço** e **Estou em dúvida**) e um copiloto de IA que tira dúvidas consultando apenas os dados daquele associado. A IA não autoriza compras: só os botões registram a resposta. Os casos de dúvida, contestação ou pedido de atendimento vão para a analista de prevenção a fraudes, que decide com o score do modelo de risco e registra uma justificativa.

O protótipo usa dados sintéticos e operações simuladas. A melhoria da experiência ainda precisa ser testada com pessoas; as pendências estão em [critérios e pendências](docs/anexos/gestao/o-que-falta-concluir.md).

## Como navegar pelo repositório

### Por onde começar

| Quero... | Comece por |
|---|---|
| Entender o projeto do início ao fim | [Documentação principal](docs/documentacao-do-projeto.md): problema, persona, decisões, custos, dados, construção, testes e entrega |
| Usar a aplicação | [Site publicado](https://raiz-jq28.onrender.com) e [guia de uso](docs/anexos/sistema/como-usar-a-demonstracao.md) |
| Rodar no meu computador | [Guia de uso](docs/anexos/sistema/como-usar-a-demonstracao.md) (Docker) ou os READMEs do [backend](watson/backend/README.md) e do [frontend](watson/frontend/README.md) |
| Saber quais tecnologias usamos e por quê | [Tecnologias do Raiz](docs/tecnologias.md) |
| Ler o código | [watson/README.md](watson/README.md) e a [visão geral da arquitetura](docs/anexos/sistema/arquitetura/visao-geral.md) |
| Ver os dados e o modelo de risco | [notebooks/](notebooks/) e [dados e modelo](docs/anexos/dados-e-modelo/README.md) |
| Ver como o time usou o IBM Bob | [bob_sessions/](bob_sessions/) (relatórios por integrante) e [.bob/rules/](.bob/rules/) (regras do projeto para o Bob) |
| Ver a integração com watsonx.ai e Orchestrate | [Teste do deploy no watsonx.ai](docs/anexos/sistema/specs/teste-historico-watsonx.md), [scripts/deploy_watsonx.py](scripts/deploy_watsonx.py) e [agente/](agente/) |
| Consultar contratos, evidências e registros originais | [Índice dos anexos](docs/anexos/README.md) |

### Mapa das pastas

```text
Inteli-Raiz/
├── README.md              ← esta página: acesso rápido e navegação
├── docs/                  ← documentação em português
│   ├── documentacao-do-projeto.md   leitura principal (11 seções)
│   ├── tecnologias.md               cada tecnologia usada, para que serve e onde está
│   └── anexos/                      detalhes por assunto
│       ├── produto/                 problema, escolha da solução e proposta de valor
│       ├── experiencia-do-usuario/  persona, jornada, telas, roteiros de pesquisa e design
│       ├── sistema/                 requisitos, arquitetura, contrato da API e guia da demonstração
│       ├── dados-e-modelo/          análise, preparação, avaliação do modelo e figuras
│       ├── gestao/                  regras do produto, entregas IBM, pendências e orçamento
│       ├── evidencias/              logs de testes e registros de ambiente
│       └── historico/               planos antigos recuperados do Git
├── watson/                ← código da aplicação (nomes em inglês)
│   ├── frontend/                    React + Vite + Carbon: telas do associado e da analista
│   ├── backend/                     FastAPI + SQLAlchemy: API, regras, agente de IA e modelo de risco
│   └── infra/                       Docker Compose local e imagem única usada na publicação
├── notebooks/             ← 01 análise exploratória, 02 base balanceada, 03 modelo Random Forest
├── data/                  ← orientações e dicionário do case; bases processadas em processed/
├── outputs/               ← modelo treinado (modelo_rf.joblib) e triagem de colunas
├── scripts/               ← publicar o modelo no watsonx.ai, calcular custos e gerar figuras da documentação
├── agente/                ← agente e ferramenta de teste do watsonx Orchestrate (ADK)
├── demonstracao/          ← vídeo de demonstração da plataforma
├── bob_sessions/          ← relatórios das sessões no IBM Bob, uma pasta por integrante
├── contexto/              ← materiais do programa IBM (desafio, guia e aulas, em PDF)
└── .bob/rules/            ← regras que orientam o Bob no backend e na documentação
```

### Arquivos da raiz

| Arquivo | Para que serve |
|---|---|
| `render.yaml` | Configuração da publicação no Render ([passo a passo](watson/infra/README.md#publicar-no-render)) |
| `.dockerignore` | O que entra no build da imagem única publicada |
| `requirements.txt` | Dependências Python dos notebooks (scikit-learn 1.6, a mesma versão do modelo publicado no watsonx.ai) |
| `.bobignore` | Pastas que o Bob não precisa ler (PDFs, dados brutos, dependências) |
| `.gitattributes` | Padroniza quebras de linha e marca arquivos binários |
| `package-lock.json` | Arquivo vazio do npm, sem uso; as dependências do frontend ficam em `watson/frontend/` |

Os arquivos `.md` são textos em Markdown. No GitHub, clique no arquivo para ler a versão formatada. Cada pasta com `README.md` tem uma página de entrada própria.

## Rodar localmente

Com Docker Desktop, a partir da pasta `watson/`:

```bash
cp backend/.env.example backend/.env    # troque SESSION_SECRET; GROQ_API_KEY ativa o chat
docker compose -f infra/docker-compose.yml up --build
# aplicação: http://localhost:8080 · API: http://localhost:8000/docs
```

Para rodar sem Docker, siga os READMEs do [backend](watson/backend/README.md) e do [frontend](watson/frontend/README.md). O backend precisa de Python 3.12 ou 3.13: o scikit-learn 1.6.1, exigido pelo modelo, não tem pacote pronto para o Python 3.14.

## Convenções

- Código, rotas, pastas e tabelas em inglês; textos da tela e documentação em português.
- Trabalho em branches a partir de `develop`, com pull request e revisão humana.
- Chaves e segredos ficam só no `.env` local ou no painel do Render, nunca no repositório.
