# Sistema

Como a solução funciona por dentro: componentes, agente, contratos, testes e reprodução do MVP. Responsáveis por função: **Arquitetura** (D09, D10) e **Integração e validação** (D11).

## Entregas

| Documento | Pergunta que responde |
|---|---|
| [Estrutura da solução](requisitos-da-solucao.md) | Quais capacidades, requisitos (R01–R12) e critérios de sucesso? |
| [Arquitetura e limites de autonomia](arquitetura-do-sistema.md) | Quais componentes, ferramentas do agente, contratos e falhas? |
| [Fluxo do MVP](reproducao-e-testes-do-fluxo.md) | Como rodar e reproduzir o fluxo ponta a ponta? |
| [Matriz de cenários e evidências](cenarios-e-evidencias-de-teste.md) | Qual teste cobre cada requisito e qual o limite da evidência? |

## Arquitetura e especificações

| Documento | Conteúdo |
|---|---|
| [Visão geral](arquitetura/visao-geral.md) | Camadas, árvore do repositório e regras de dependência |
| [Contrato da API](specs/contrato-da-api.md) | Endpoints, estados, erros e exemplos |
| [Teste watsonx.ai (histórico)](specs/teste-historico-watsonx.md) | Evidência do deploy do modelo no watsonx.ai; o Orchestrate saiu do escopo em 27/10 |

Decisões de arquitetura (ADR):

| # | Decisão | Status |
|---|---|---|
| [0001](arquitetura/decisoes/0001-backend-fastapi.md) | Backend em Python + FastAPI | incorporada ao plano |
| [0002](arquitetura/decisoes/0002-banco-trocavel.md) | Banco trocável via SQLAlchemy; SQLite na demo | incorporada ao plano |
| [0003](arquitetura/decisoes/0003-codigo-em-ingles.md) | Código e rotas em inglês | incorporada ao plano |
| [0004](arquitetura/decisoes/0004-aviso-automatico-risco-medio.md) | Aviso automático no risco médio | **substituída** pela política conservadora do [plano](../gestao/regras-do-produto.md) §3 |
