# Sessão 8 no Bob — Pedro Rodrigues

Tarefas rodadas no Bob IDE (modo agent), branch `develop` (migração de `main` feita nesta semana).

| Tarefa | Início | Commit |
|---|---|---|
| `docs`: adicionar plano de implementação com confirmação pelo associado | 23/10 13:43 UTC | `70310de` |
| `docs`: detalhar entregas IBM e dividir responsabilidades entre quatro pessoas | 27/10 11:14 UTC | `0985e0b` |
| `docs`: alinhar planejamento e backlog ao associado e equipe de quatro pessoas | 27/10 11:19 UTC | `3f95da9` |
| `docs`: separar pedido de ajuda e ativar integração do frontend Watson | 28/10 10:49 UTC | `5812997` |

## O que a revisão humana verificou

- Leitura dos slides da aula (S3 — Empreendedorismo em IA, S4 — Primeira sessão técnica) antes de escrever o plano; seções §§1–10 estruturadas para cobrir produto, contrato, agente, testes e demonstração.
- `docs/plano_implementacao.md`: documento de 301 linhas aprovado pela equipe como referência de produto; cobre personas, fluxo, contrato da API (§§4–5), regras de segurança (§3), modelo de risco (§6), agente (§7), casos de teste (§9) e roteiro de demo (§10).
- `docs/direcional_entregas.md`: 13 entregas (D01–D13) distribuídas por função — produto, pesquisa/design, arquitetura, integração/testes — com saída esperada, critério de aceite e dependências.
- `artifacts/planejamento/backlog.md` e `plano_15_dias.md`: backlog de cards em Kanban e cronograma por dia; revisados para refletir equipe de quatro pessoas com papéis distintos.
- `5812997`: ajuste fino no plano para explicitar que o frontend Watson (React + Carbon) já existe e pode ser adaptado; commit separado para não misturar plano com backlog.
- Verificado que nenhum campo de `customer_id` ou dado sensível (saldo, renda, score) foi listado como retorno de rota para o associado nos contratos rascunhados.

## Resumo final de cada tarefa

### `docs`: adicionar plano de implementação

`70310de`

```text
docs/plano_implementacao.md  (novo, 301 linhas)

§1  Produto: assistente de confirmação de compras pelo associado
§2  Personas: Ana (associada), Bruno (analista), três perfis para demo
§3  Regras que não se negociam: identidade por cookie, nunca expor score
    ou customer_id, recusa não bloqueia cartão
§4  Contrato do associado: GET /purchases, GET /purchases/{id},
    GET /purchases/{id}/status, POST /confirmations/{id}/response,
    GET/POST /purchases/{id}/chat, POST /purchases/{id}/review
§5  Contrato do analista: GET /reviews, GET /reviews/{id},
    POST /reviews/{id}/decision
§6  Modelo de risco: LocalRiskModel, features, política de limiar
§7  Agente: Pydantic AI, 4 ferramentas, instruções, limites de autonomia
§8  Implementação faseada: fundação → sessão → compras → confirmação
    → agente → chat → demo → analista → segurança
§9  Casos de teste obrigatórios T-001–T-012 com entrada e resultado
§10 Roteiro de demonstração em 10 passos

docs/plano_implementacao.pdf  (gerado para leitura offline)
docs/README.md  — link adicionado
```

### `docs`: detalhar entregas IBM e dividir responsabilidades

`0985e0b`

```text
docs/direcional_entregas.md  (novo, 445 linhas)

Tabela de visão geral: D01–D13 com título, resultado concreto e
origem nos slides.

Seções por entrega: orientação da aula, pergunta que resolve,
partes do artefato, como produzir, para concluir, para elevar
a qualidade, liderança sugerida e saída esperada.

Tabela de responsáveis: D01-D13 × [produto, pesquisa, arquitetura,
integração] com revisão cruzada.

Matriz de rastreabilidade de exemplo: evidência → necessidade →
decisão → requisito → como verificar → resultado/versão.

docs/plano_implementacao.md  — §9 e §10 referenciados como fontes
```

### `docs`: alinhar planejamento e backlog

`3f95da9`

```text
artifacts/planejamento/backlog.md       (novo, 89 linhas)
  Cards C01–C28 em formato Kanban: title, quem, entrada, saída,
  critérios. Cards de backend (C01–C09), agente (C10–C14),
  frontend (C15–C19), testes (C20–C24), docs (C25–C28).

artifacts/planejamento/plano_15_dias.md (novo, 117 linhas)
  Cronograma dia a dia: D1–D15 com cards planejados, decisões
  de risco e marcos de integração.

artifacts/planejamento/artefatos_materiais_contexto.md
  Lista de fontes (slides, guia IBM, desafio Sicredi) com
  paths locais verificados.

README.md  — seção de navegação atualizada
```

### `docs`: separar pedido de ajuda e ativar integração do frontend

`5812997`

```text
README.md
  Seção "Frontend Watson" adicionada: link para o repositório,
  instrução de adaptar o SessionGate e a lista de compras.

docs/plano_implementacao.md
  §8 atualizado: frontend Watson já existe; tarefa é adaptar
  componentes existentes, não construir do zero. Prioridade de
  integração antecipada para a semana 2.

docs/direcional_entregas.md
  D12: liderança de "Integração e validação" explicitada como
  quem consolida; Leonardo indicado como executor técnico do
  frontend existente.

artifacts/planejamento/backlog.md
  Cards C10/C13/C18/C27 marcados como ativos; demais como planejados.

artifacts/planejamento/plano_15_dias.md
  Dia 8 adicionado: ativação do frontend Watson + SessionGate.
```
