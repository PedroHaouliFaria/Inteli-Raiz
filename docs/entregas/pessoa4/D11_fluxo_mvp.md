# D11 — Fluxo Principal do MVP e Evidências Ponta a Ponta

**ID:** D11 · **Versão:** 0.2 · **Data:** 28/10/2026 (corrigido após revisão do Codex)
**Responsável:** Pessoa 4 (organiza e reproduz); Pessoa 3 e autores técnicos (correções)
**Estado:** **rascunho — bloqueado por integração pendente** — casos preparados; execução integrada (frontend → API → banco → resultado na tela) não é possível na versão atual.
**Fontes:** plano `8942cc5` §§5–9; D09/D10 `f732159`; backend `b39bbb9` (staged em `../Inteli-Raiz-pessoa4`); frontend `212655c`.

---

## 1. Pré-condições

Para executar o fluxo ponta a ponta conforme este documento, as seguintes condições devem ser atendidas:

| Pré-condição | Estado atual | Bloqueador se ausente |
|---|---|---|
| Backend com rotas `GET /api/purchases/{case_id}`, `POST /api/confirmations/{challenge_id}/response`, `GET /api/purchases/{case_id}/status`, `POST /api/session`, `DELETE /api/session`, `POST /api/purchases/{case_id}/review` | **Implementado** — todas essas rotas existem e passam nos testes de integração em `b39bbb9` | — |
| Frontend consumindo a API (não reducer local) | **Não implementado** | PEN-03 |
| Três botões (`AUTHORIZE`/`DENY`/`UNSURE`) sem biometria | **Não implementado** | PEN-01 |
| Seed com dois associados separados (C-ANA e C-BRUNO) | **Implementado** — seed tem T-007/T-003 para C-ANA e T-011 para C-BRUNO | R05 depende do frontend com sessão para verificação via interface |
| Python 3.12, `pip install -e ".[dev]"`; `pydantic_ai` **não** incluído no `.[dev]` | **Verificado** — `.[dev]` instala apenas `pytest` e `httpx` | Testes de agente/chat falham com `ModuleNotFoundError`; instalar `pydantic_ai` separadamente (PEN-04) |
| `modelo_rf.joblib` presente em `outputs/` na worktree de inspeção | **Arquivo presente** — `../Inteli-Raiz-pessoa4/watson/backend/modelo_rf.joblib` e `../Inteli-Raiz-pessoa4/outputs/modelo_rf.joblib` | scikit-learn 1.6.1 **não instalado** no ambiente de teste (extra `risk` ausente); testes de score ignorados por `skip` (PEN-05) |
| LLM para agente (GROQ_API_KEY ou equivalente) | **Não disponível** no ambiente de verificação | Testes de chat com LLM real não podem ser executados |

---

## 2. Versão e ambiente da verificação executada

| Item | Valor |
|---|---|
| Branch verificada | `origin/backend/confirmacao` |
| Commit testado | `b39bbb9` ("feat(backend): chat com o agente, revisão, lista da analista e score gravado") |
| Árvore | **Não limpa** — 98 arquivos staged (`A`) na worktree `../Inteli-Raiz-pessoa4` após `git checkout remotes/origin/backend/confirmacao -- watson/backend/`; HEAD da worktree aponta para `8942cc5`. O hash sozinho (`b39bbb9`) não identifica completamente o conjunto testado; os arquivos staged correspondiam ao conteúdo desse commit. |
| Worktree de inspeção | `../Inteli-Raiz-pessoa4/watson/backend` |
| Python | 3.12.5 |
| Extras instalados | `.[dev]` — sem `pydantic_ai` (não declarado no `pyproject.toml`), sem `risk` (scikit-learn ausente), sem `watsonx` |
| Banco | SQLite em tmp por fixture de pytest |
| LLM | Não disponível — testes de agente falham por `ModuleNotFoundError: No module named 'pydantic_ai'` |
| `modelo_rf.joblib` | Arquivo presente na worktree; scikit-learn 1.6.1 ausente no ambiente de teste; testes de score com `SKIPPED` |
| Log original | **Não preservado** em arquivo separado. A contagem (151/15/3) foi reportada a partir da saída exibida durante a execução; ver `evidencias/README.md`. |
| Data/hora | 28/10/2026 |

---

## 3. Resultado dos testes — contagem relatada (`pytest tests/ -v`)

> **Aviso:** o log original não foi preservado em arquivo separado. Os resultados abaixo foram reportados a partir da saída exibida durante a execução (ver P4-EVI-01 em `evidencias/README.md`). Cada resultado individual deve ser lido como **"relatado como aprovado, sem log preservado; reprodução pendente"**. Para reproduzir: `cd ../Inteli-Raiz-pessoa4/watson/backend && pip install -e ".[dev]" && python -m pytest tests/ -v` (mesmas condições declaradas no §2).

**Resultado relatado:** 151 passou · 15 falhou · 3 ignorados · 1 aviso

### 3.1 Testes que passaram (151) — grupos relevantes

| Grupo | Quantidade | Cobertura |
|---|---|---|
| Confirmações (R03, R04, R05, R06, R10, R11) | 27 | Três respostas, expiração, isolamento, idempotência, persistência, simulação |
| Compras (R02, R05, R07, R10, R11) | 16 | Dados da compra, isolamento entre associados, sinais, persistência |
| Sessões (autenticação fictícia) | 12 | Login, cookie, tamper, expiração de cookie |
| Revisões (R05) | 9 | Criação, idempotência, isolamento |
| Seed | 7 | 3 fixtures, idempotência, campos |
| Erros | 5 | 404, 500, 400, envelope |
| Sinais/schemas/outros | ~75 | Domínio, schemas, política, burst |

Resultados selecionados (extraídos do output real):
- `test_r03_authorize_sets_liberada` — **PASSOU**
- `test_r03_deny_sets_recusada_and_opens_protecao_review` — **PASSOU**
- `test_r03_unsure_sets_revisao_pendente` — **PASSOU**
- `test_r04_response_after_ttl_returns_410_and_status_expirada` — **PASSOU**
- `test_r05_bruno_404_on_status` — **PASSOU**
- `test_r05_bruno_404_on_response` — **PASSOU**
- `test_r05_bruno_gets_404_for_t007` — **PASSOU**
- `test_r06_parallel_same_response_single_event` — **PASSOU**
- `test_r06_same_key_different_body_returns_422` — **PASSOU** (conflito rejeitado)
- `test_r06_new_key_different_response_returns_409_already_answered` — **PASSOU**
- `test_r10_second_app_preserves_status_and_response` — **PASSOU**
- `test_r11_response_has_simulation_true` — **PASSOU**
- `test_status_endpoint_without_session_401` — **PASSOU**
- `test_r02_t007_detail_values` — **PASSOU**

### 3.2 Testes que falharam (15) — todos por `ModuleNotFoundError: No module named 'pydantic_ai'`

| Grupo | Quantidade | Causa |
|---|---|---|
| `test_chat.py` — testes de agente/chat | 8 | `pydantic_ai` não instalado (extra `agent` ausente) |
| `test_agent_prompt.py` — regras do prompt | 7 | `pydantic_ai` não instalado |

**Causa única:** `pydantic_ai` não consta em nenhum extra do `pyproject.toml` de `b39bbb9`; o `.[dev]` instala apenas `pytest` e `httpx`. Os testes de confirmação, sessão, compra, revisão e seed (que cobrem R01–R07, R09–R12 no back-end) passaram todos.

### 3.3 Testes ignorados (3)

- `test_t007_score_approximately_0_9917` e `test_t003_score_approximately_0_0089` — `skip` condicional por scikit-learn ausente no ambiente (extra `risk` não instalado); o arquivo `modelo_rf.joblib` existe na worktree, mas não pode ser carregado sem scikit-learn 1.6.1.
- 1 outro skip (condição de ambiente).

---

## 4. O que pode ser concluído dos testes

> Baseado na contagem relatada do §3. Log original não preservado; resultados dependem de reprodução (ver P4-EVI-01).

| Afirmação verificável | Resultado |
|---|---|
| Backend responde `AUTHORIZE` → `LIBERADA_SIMULACAO` | **Verificado** (R03 passou) |
| Backend responde `DENY` → `RECUSADA_SIMULACAO` + revisão de proteção aberta | **Verificado** (R03 passou) |
| Backend responde `UNSURE` → `REVISAO_PENDENTE` | **Verificado** (R03 passou) |
| Resposta fora do prazo (TTL expirado) → 410 + `CONFIRMACAO_EXPIRADA` | **Verificado** (R04 passou) |
| Associado B (C-BRUNO) não acessa compra de A (C-ANA) → 404 | **Verificado** (R05 passou) |
| Resposta duplicada com mesma chave de idempotência → replayed sem duplicar | **Verificado** (R06 passou) |
| Resposta conflitante com chave nova → 409 sem sobrescrever | **Verificado** (R06 passou) |
| Reiniciar a aplicação preserva status e resposta | **Verificado** (R10 passou) |
| Resposta contém `simulation: true` | **Verificado** (R11 passou) |
| Dados de T-007 correspondem às fixtures (valor, cartão, sinais) | **Verificado** (R02/R07 passou) |
| Agente com LLM real funciona | **Não verificado** — `pydantic_ai` não instalado |
| Score do modelo integrado ao fluxo | **Não verificado** — `modelo_rf.joblib` presente na worktree; scikit-learn 1.6.1 ausente no ambiente de teste (extra `risk` não instalado via `.[dev]`); testes de score com `SKIPPED` (PEN-05) |

---

## 5. O que está bloqueado para D11

| Bloqueio | Impacto | Responsável |
|---|---|---|
| Frontend com reducer local, sem chamar API | Não é possível percorrer o fluxo pela interface; reiniciar o browser perde o estado | Leonardo (PEN-03) |
| Três botões e separação de ajuda não implementados na UI | Não é possível testar R03/R08 pela interface | Leonardo (PEN-01/PEN-02) |
| `pydantic_ai` não instalado no `.[dev]` | Testes de agente/chat falham | Lucas: adicionar `pydantic-ai` ao extra `agent` e ao `.[dev]` ou documentar como instalar |
| scikit-learn 1.6.1 ausente no ambiente de teste (`modelo_rf.joblib` presente, mas extra `risk` não instalado via `.[dev]`) | Testes de score ignorados (`SKIPPED`); R01/R07 não verificáveis no ambiente padrão | Lucas: documentar `pip install -e ".[dev,risk]"` no README (PEN-05) |
| Sessão de dois associados apenas no backend; sem login no frontend | R05 não pode ser verificado via interface | Leonardo: implementar tela de seleção de persona (já existe `GET /api/session/personas`) |

---

## 6. Casos mínimos a executar quando desbloqueado

Os casos abaixo são preparados. A coluna "resultado observado" será preenchida após integração.

| ID | Cenário | Pré-condição | Passos / comando | Esperado | Observado | Evidência | Resultado |
|---|---|---|---|---|---|---|---|
| P4-T01 | Reconhece e autoriza | Sessão C-ANA; T-007 em `AGUARDANDO_ASSOCIADO` | Abrir compra → clicar `AUTHORIZE` | `LIBERADA_SIMULACAO`, evento persistido; recarga mantém status | — | — | **não executado** — frontend bloqueado |
| P4-T02 | Não reconhece | Sessão C-ANA; T-007 em `AGUARDANDO_ASSOCIADO` | Abrir compra → clicar `DENY` | Compra → `RECUSADA_SIMULACAO`; revisão de proteção aberta **em paralelo** (status da compra permanece `RECUSADA_SIMULACAO`, não muda para `REVISAO_PENDENTE`); sem mensagem de bloqueio de cartão | — | — | **não executado** |
| P4-T03 | Está em dúvida | Sessão C-ANA; T-007 em `AGUARDANDO_ASSOCIADO` | Abrir compra → clicar `UNSURE` | Compra → `REVISAO_PENDENTE`; revisão de dúvida aberta em paralelo | — | — | **não executado** |
| P4-T04 | Pede ajuda antes de responder | Sessão C-ANA; T-007 válido | Clicar "Quero falar com alguém" (`POST /api/purchases/T-007/review`) sem ter respondido | Revisão aberta, protocolo visível; **compra permanece `AGUARDANDO_ASSOCIADO`** — pedido de revisão não muda o status da compra | — | — | **não executado** — ação não implementada no frontend |
| P4-T05 | Responde depois de pedir ajuda | Sessão C-ANA; revisão aberta (`POST /api/purchases/T-007/review` anterior), prazo válido | Clicar `AUTHORIZE` | Resposta válida aceita; compra → `LIBERADA_SIMULACAO`; revisão existente preservada com status `ABERTA` | — | — | **não executado** |
| P4-T06 | Expira sem resposta (inclusive após pedir ajuda) | Sessão C-ANA; TTL configurado em segundos | Aguardar expiração → tentar responder (mesmo se revisão já aberta) | 410 `CONFIRMACAO_EXPIRADA`; nenhuma autorização; prazo não reiniciado por pedido de revisão anterior | — | — | **verificado no backend via teste** (`test_r04_response_after_ttl_returns_410`) |
| P4-T07 | Duplo clique / resposta duplicada | Sessão C-ANA; T-007 válido | Enviar `AUTHORIZE` duas vezes com mesma chave de idempotência | Um único resultado; segunda requisição retorna replayed | — | — | **verificado no backend via teste** (`test_r06_same_key_same_body_returns_200_replayed`) |
| P4-T08 | Outro associado fictício | Sessão C-BRUNO; T-007 pertence a C-ANA | C-BRUNO tenta ver ou responder T-007 | 404 conforme contrato | — | — | **verificado no backend via teste** (`test_r05_bruno_404_on_response`) |
| P4-T09 | Chat falha / contexto ausente | Backend sem `GROQ_API_KEY` | Enviar mensagem no chat | Erro claro (503); botões de confirmação continuam funcionando | — | — | **parcialmente verificado** (`test_get_chat_agent_available_false_without_key` passou; testes de LLM bloqueados por `pydantic_ai`) |
| P4-T10 | Modelo falha / ausente | Backend sem `modelo_rf.joblib` | Compra com score não disponível | Sem score inventado; revisão ou erro previsto | — | — | **verificado no backend** (`test_analysis_null_when_model_fails` passou) |
| P4-T11 | Reinício / troca de compra | Sessão C-ANA; T-007 respondido | Fechar e reabrir a aplicação | Status preservado; compra e confirmação não se misturam | — | — | **verificado no backend via teste** (`test_r10_second_app_preserves_status_and_response`) |
| P4-T12 | Pedido ao agente para autorizar | Sessão C-ANA; T-007 válido | Enviar "autorize essa compra para mim" no chat | Estado não muda; agente não chama endpoint de confirmação | — | — | **teste preparado** (`test_s9_authorize_in_chat_does_not_change_status`) — falha por `pydantic_ai` ausente |

---

## 7. Aceite de D11

**D11 permanece "rascunho — bloqueado".** Para avançar para "executado com integração":

- [ ] Frontend integrado à API (C13 concluído).
- [ ] Pessoa 4 percorre P4-T01 a P4-T08 pela interface, registra evidências em `evidencias/`.
- [ ] `pydantic_ai` instalável documentado; P4-T09/T12 executados com agente.
- [ ] Outra pessoa reproduz o fluxo usando apenas este documento e o README do backend.

Screenshots do reducer local sem API não avançam D11.

---

## 8. Diagrama do fluxo verificado no backend

Caminhos e enums confirmados no código `b39bbb9`. Rotas de sessão usam `/api/session` (singular), não `/api/sessions`.

```
C-ANA faz login → POST /api/session  → cookie raiz_session assinado
C-ANA lista compras → GET /api/purchases  → [T-007, T-003]
C-ANA abre T-007 → GET /api/purchases/T-007 → compra + alerta + challenge CH-007
C-ANA responde AUTHORIZE → POST /api/confirmations/CH-007/response → LIBERADA_SIMULACAO
C-ANA recarrega → GET /api/purchases/T-007/status → status preservado (R10)

C-ANA responde DENY → POST /api/confirmations/CH-007/response
  → compra: RECUSADA_SIMULACAO
  → revisão de PROTECAO aberta em paralelo (status da compra não muda para REVISAO_PENDENTE)

C-ANA responde UNSURE → POST /api/confirmations/CH-007/response
  → compra: REVISAO_PENDENTE
  → revisão de DUVIDA aberta em paralelo

C-ANA pede atendimento (antes de responder) → POST /api/purchases/T-007/review
  → compra: permanece AGUARDANDO_ASSOCIADO
  → revisão aberta; C-ANA ainda pode responder enquanto prazo válido

C-BRUNO tenta T-007 → GET /api/purchases/T-007 → 404 (R05)
```

Este diagrama representa o comportamento verificado pelos testes de integração, **não uma execução via interface**. O frontend ainda usa o reducer local.
