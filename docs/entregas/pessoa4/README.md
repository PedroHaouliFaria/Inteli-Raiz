# Pacote Pessoa 4 — Protótipo, Fluxo e Validação

**Versão:** 0.1 · **Data:** 28/10/2026  
**Responsável:** Pessoa 4  
**Revisores:** Pessoa 2 (D12/D13), Pessoa 3 (D11)  
**Branch de trabalho:** `docs/pessoa4-prototipo-validacao` (criada a partir de `origin/develop` `8942cc5`)  
**Worktree local:** `../Inteli-Raiz-pessoa4`  
**Estado geral:** rascunho — verificação documental e inspeção de código executadas; integração frontend–backend não disponível nesta versão.

---

## 1. Índice de arquivos

| Arquivo | Entrega | Estado |
|---|---|---|
| `README.md` (este arquivo) | Índice, versões consultadas, cobertura e pendências | rascunho |
| `D12_prototipo_experiencia.md` | D12 — Protótipo da experiência | **revisado documentalmente** |
| `D11_fluxo_mvp.md` | D11 — Fluxo principal do MVP | **rascunho — bloqueado por integração pendente** |
| `D13_validacao_melhorias.md` | D13 — Validação e melhorias | **rascunho — protocolo pronto; execução não realizada** |
| `matriz_cenarios_e_evidencias.md` | Casos P4-T01–T12, requisitos e evidências | rascunho |
| `pendencias_e_aceite.md` | Alterações para Leonardo e backend | rascunho |
| `evidencias/README.md` | Índice de registros produzidos nesta execução | ver arquivo |

---

## 2. Versões consultadas

| Fonte | Branch / local | Hash | Observação |
|---|---|---|---|
| Plano vigente e Direcional | `origin/develop` | `8942cc5` | Fonte principal de produto; PR #8 integrado |
| Backlog | `origin/develop` | `8942cc5` | C01–C32, todos em Backlog |
| Pacote Pessoa 2 (D02/D03/D06/roteiro) | `origin/docs/pessoa2-pesquisa-associado` | `8a7aefc` | Worktree em `../Inteli-Raiz-pessoa2-pesquisa`; consultado via `git show`; não alterado |
| Frontend Watson — Leonardo | `origin/watson` | `212655c` | `watson/frontend` — React + Carbon; inspecionado via `git show`, não executado de forma integrada |
| Backend — Lucas — **versão testada** | `origin/backend/confirmacao` — commit `b39bbb9` | `b39bbb9` | Commit "feat(backend): chat com o agente, revisão, lista da analista e score gravado". Os arquivos do backend estão staged na worktree `../Inteli-Raiz-pessoa4` (98 entradas `A`, árvore **não limpa**). Testes executados sobre esse conjunto de arquivos, não sobre `099c9fa`. |
| D09/D10 — Pessoa 3 | `origin/entregas/p3-estrutura-arquitetura` | `f732159` | `entregas/09_estrutura_solucao.md` e `10_arquitetura.md`; estado: rascunho |

Nenhum merge entre branches foi realizado nesta tarefa. Fontes de outras branches foram consultadas exclusivamente via `git show <ref>:<caminho>`. Os arquivos do backend foram obtidos por `git checkout remotes/origin/backend/confirmacao -- watson/backend/` na worktree `../Inteli-Raiz-pessoa4`.

---

## 3. Estado de cada entrega

| Entrega | Estado nesta execução | Justificativa |
|---|---|---|
| **D12** Protótipo da experiência | **revisado documentalmente** | Percurso, mapa de telas/estados, textos candidatos e adaptações para o Watson especificados com base na inspeção do código `212655c` e nos documentos do plano. Interface real inspecionada; sem execução integrada. |
| **D11** Fluxo principal do MVP | **rascunho — bloqueado** | Casos preparados e pré-condições documentadas. Frontend `212655c` gerencia fluxo no reducer sem chamar API. Backend `b39bbb9` expõe as rotas necessárias, mas o frontend ainda não as consome. Execução integrada não é possível nesta versão. |
| **D13** Validação e melhorias | **protocolo pronto** | Tarefas, chave de avaliação e modelos de registro completos. Pesquisa não executada; sem participantes ou resultados reais. Protocolo constitui estado intermediário, não conclusão de D13. |

**Definição dos estados aplicados:**
- *rascunho*: estrutura presente, conteúdo parcial, sem revisão.
- *revisado documentalmente*: conteúdo completo, revisado com base em fontes escritas; sem teste com usuários ou execução integrada.
- *protocolo pronto*: método, critérios e instrumentos definidos; coleta não realizada.
- *verificado em protótipo*: dependente de D12 com execução real.
- *executado com integração*: dependente de D11 integrado.
- *validado neste piloto*: dependente de D13 com coleta real.

---

## 4. Resumo de cobertura — capacidades inspecionadas

| Capacidade | Fonte / commit | Status real | Lacuna / entrega afetada |
|---|---|---|---|
| Tabelas de compras, confirmações, revisões e eventos | Backend `b39bbb9` | **Implementado** — schema SQLAlchemy completo | — |
| Seed com 3 fixtures (T-007/C-ANA, T-003/C-ANA, T-011/C-BRUNO) | Backend `b39bbb9` | **Implementado e testado** | R05 depende do frontend com sessão para verificação via interface |
| Rotas HTTP de compras (`GET /api/purchases`, `GET /api/purchases/{case_id}`, `GET /api/purchases/{case_id}/status`) | Backend `b39bbb9` | **Implementado e testado** | Frontend não consome; PEN-03 |
| Rota `POST /api/confirmations/{challenge_id}/response` | Backend `b39bbb9` | **Implementado e testado** | Frontend não consome; PEN-03 |
| Rota `POST /api/purchases/{case_id}/review` | Backend `b39bbb9` | **Implementado e testado** | Frontend não consome; PEN-02/PEN-03 |
| Rota `GET /api/purchases/{case_id}/chat` e `POST /api/purchases/{case_id}/chat` | Backend `b39bbb9` | **Implementado**; testes de agente bloqueados por `pydantic_ai` ausente no extra `.[dev]` | PEN-04 (renumerado) |
| Sessão fictícia (`POST /api/session`, `GET /api/session`, `DELETE /api/session`, `GET /api/session/personas`) | Backend `b39bbb9` | **Implementado e testado** | Frontend não consome; PEN-03 |
| Expiração verificada pelo servidor (`expires_at` + lógica no `respond()`) | Backend `b39bbb9` | **Implementado e testado** | — |
| Três respostas explícitas (`AUTHORIZE`/`DENY`/`UNSURE`) na UI | Frontend `212655c` | **Não implementado** — `itWasMe`/`notMe` + biometria | PEN-01 |
| Separação entre pedido de atendimento e `UNSURE` | Frontend `212655c` | **Não implementado** — link sem ação | PEN-02 |
| Consumo da API pelo frontend | Frontend `212655c` | **Não implementado** — reducer local | PEN-03 |
| Agente conversacional com LLM real | Backend `b39bbb9` — `pydantic_ai` não no `.[dev]` | **Parcialmente bloqueado** — código presente; `pydantic_ai` não instalável via `.[dev]` | PEN-04 |
| `modelo_rf.joblib` presente | `outputs/` na worktree `../Inteli-Raiz-pessoa4` | **Arquivo presente** — scikit-learn 1.6.1 **não instalado** no ambiente de teste (extra `risk` ausente no `.[dev]`) | PEN-05 (renumerado) |
| Mensagem de bloqueio de cartão na UI | Frontend `212655c` | **Presente e incorreta** — tela `protected`: "Bloqueamos o cartão...nada foi cobrado...cartão novo em 7 dias" | PEN-01; viola §3 do plano |
| Biometria obrigatória para `itWasMe` | Frontend `212655c` | **Presente** — tela `biometrics` entre resposta e confirmação | PEN-01; viola §4 do plano |

---

## 5. Pendências prioritárias (resumo)

Ver tabela completa em `pendencias_e_aceite.md`.

| ID | Achado | Prioridade | Responsável por função |
|---|---|---|---|
| PEN-01 | UI: 2 botões + biometria + mensagem de bloqueio de cartão | P0 | Leonardo (frontend) |
| PEN-02 | UI: link de atendimento sem ação; sem separação de UNSURE | P0 | Leonardo (frontend) |
| PEN-03 | UI: sem chamadas à API; estado gerido só no reducer | P0 | Leonardo (frontend) |
| PEN-04 | `pydantic_ai` não instalável via `.[dev]`; testes de agente/chat falham | P1 | Lucas (backend) — adicionar ao `pyproject.toml` |
| PEN-05 | `scikit-learn` 1.6.1 ausente no ambiente de teste (extra `risk` fora do `.[dev]`); `modelo_rf.joblib` existe mas não pôde ser carregado | P1 | Lucas (backend) — documentar; extra `risk` exige instalação separada |
| PEN-06 | Isolamento entre associados verificado na API; não testável pela interface sem frontend integrado | P1 | Leonardo (frontend) — tela de seleção de persona |

---

## 6. Três próximos passos concretos

1. **Leonardo:** substituir `MemberPhone.jsx` pelos três botões (`AUTHORIZE`/`DENY`/`UNSURE`) sem biometria; implementar ação real para "Quero falar com alguém" (chamar `POST /api/purchases/{case_id}/review`); consumir `GET /api/purchases/{case_id}`, `POST /api/confirmations/{challenge_id}/response` e `GET /api/purchases/{case_id}/status`. Aceite: Pessoa 4 percorre o fluxo completo via API e recarrega a página com estado preservado.

2. **Lucas:** adicionar `pydantic-ai` ao extra `.[dev]` no `pyproject.toml` (ou criar extra `agent` e documentá-lo no README) para que `pytest tests/integration/test_chat.py` passe com `FunctionModel`. Aceite: todos os 15 testes antes bloqueados passam.

3. **Pessoa 4:** após o item 1, executar casos P4-T01 a P4-T08 pela interface e registrar evidências reais em `evidencias/`; atualizar estado de D11.

---

## 7. Exportação das sessões do Bob

Para exportar capturas desta tarefa: abrir Tasks no Bob IDE → selecionar esta tarefa → abrir o resumo no cabeçalho → capturar as sessões relevantes. Salvar em `bob_sessions/<seu_nome>/`. Não criar imagens que simulem evidências de uso do Bob.
