# Sessão 3 no Bob — Lucas

Mesmo processo das sessões 1 e 2 (Bob Shell no Windows, orquestrado pelo Claude Code; tarefas em **Tasks → All workspaces** no Bob IDE).

| Tarefa | ID | Início | Custo | Chamadas de ferramenta |
|---|---|---|---|---|
| Tarefa 4a: score gravado, revisão, lista da analista, chat com agente Pydantic AI e health | `6b3c4145fa7a21edc2e13c511500cf73` | 29/10 12:21 UTC | 18.62 | 105 |
| Tarefa 4b: testes sem vazar ambiente (prazo de 1 s herdado causava falha intermitente) | `e65c01f40f50f8b66fb3081a44342344` | 29/10 12:47 UTC | 3.28 | 34 |
| Tarefa 4c: modelo gpt-oss-120b e instruções reforçadas depois do teste com o Groq real | `4bcdfbf8f1a35805aaa363e6fd991d93` | 29/10 12:58 UTC | 0.92 | 18 |
| **Total** | | | **22.83** | |

## O que a revisão corrigiu ou verificou

- A 4a disse "todos passando", mas a suíte falhou 1 vez em 4: testes gravavam o prazo de 1 s no ambiente e o teste seguinte herdava. A 4b isolou o ambiente; a ordem que expunha a falha passou.
- Teste com o Groq real (6 perguntas, incluindo pedir porcentagem, pedir para autorizar e pedir a compra do Bruno): o `llama-3.3-70b-versatile` não existe mais no Groq e o chat devolveu 503 com a compra intacta (caminho de falha comprovado). Com `openai/gpt-oss-120b`, quatro falhas de texto apareceram (rotulou a compra da Ana como "T-011", ofereceu o score, inventou botão, não consultou a compra). A 4c reforçou as instruções e a repetição passou nas seis.
- Em todas as conversas o estado da compra ficou `AGUARDANDO_ASSOCIADO`; o pedido de revisão gerou protocolo sem mudar o estado.

## Resumo final de cada tarefa

### Tarefa 4a: score gravado, revisão, lista da analista, chat com agente Pydantic AI e health

`6b3c4145fa7a21edc2e13c511500cf73`

```text
**165 passed, 0 failed** (era 125 antes, +40 novos testes).

---

Aqui está o resumo de tudo que foi feito, item por item:

---

## Resumo da Sessão 3

### Item 0 — Bug `normalize`: binário `"0"` → `1` (corrigido)
**Causa:** `int(bool("0")) == 1` — qualquer string não-vazia era truthy.  
**Correção em [`app/risk/features.py`](watson/backend/app/risk/features.py):** só aceita `{0, 1, "0", "1"}`; vazio/None → `None`; qualquer outro valor → `ValueError`.  
**Teste:** [`tests/unit/test_features_normalize.py`](watson/backend/tests/unit/test_features_normalize.py) (9 casos).

### Item 1 — Análise gravada
- Colunas `analysis_score`, `analysis_score_source`, `analysis_model_version`, `analysis_decision`, `analysis_policy_version`, `analysis_gaps_json`, `analysis_evaluated_at` em [`purchases`](watson/backend/app/db/tables/purchases.py).  
- Migração Alembic [`a1b2c3d4e5f6`](watson/backend/app/db/migrations/versions/a1b2c3d4e5f6_add_analysis_and_chat.py).  
- [`run_seed`](watson/backend/app/db/seed.py) chama `LocalRiskModel` uma vez por fixture; se falhar, score fica `null`.  
- T-007 ≈ 0.9917, T-003 ≈ 0.0089 (tolerância 0.001). Score nunca aparece em rotas do associado.

### Item 2 — Revisão (§8)
- Serviço de domínio [`app/domain/reviews/__init__.py`](watson/backend/app/domain/reviews/__init__.py) com `create_or_get_review(created_by=...)`.  
- [`POST /api/purchases/{case_id}/review`](watson/backend/app/api/routes/reviews.py): 201 nova / 200 existente; não muda status.  
- [`GET /api/reviews`](watson/backend/app/api/routes/reviews.py): analista only (403 para associado); inclui `analysis.score`.

### Items 3–5 — Chat (§7 e §10)
- Tabela [`chat_messages`](watson/backend/app/db/tables/purchases.py) + [`ChatRepository`](watson/backend/app/db/repositories/chat.py).  
- Agente Pydantic AI em [`app/domain/agent/__init__.py`](watson/backend/app/domain/agent/__init__.py): `AgentDeps(customer_id, case_id, db)`, 4 ferramentas sem args de identidade, instruções fixas §10, timeout 30 s, `LLM_MODEL`/`GROQ_API_KEY` na config.  
- [`GET /api/purchases/{case_id}/chat`](watson/backend/app/api/routes/chat.py): histórico; grava saudação na primeira leitura.  
- [`POST /api/purchases/{case_id}/chat`](watson/backend/app/api/routes/chat.py): salva mensagem do usuário *antes* de chamar LLM; 503 `AGENT_UNAVAILABLE` em erro/timeout; 429 `RATE_LIMITED` após 20 msgs/10min; `tools_used` e `review_protocol` na resposta.

### Item 6 — `GET /api/health` (§9)
- [`/api/health`](watson/backend/app/
```

### Tarefa 4b: testes sem vazar ambiente (prazo de 1 s herdado causava falha intermitente)

`e65c01f40f50f8b66fb3081a44342344`

```text
Done. Here's a summary of what was changed and the proof:

---

## What was done

### Root cause
Two independent sources of test contamination:
1. **`os.environ` writes without restoration** — `CONFIRMATION_TTL_SECONDS=1` set by an expiry test leaked into the next test's settings via `lru_cache`.
2. **`get_settings` / `get_engine` caches** — even when env was eventually reset, the old cached objects (with the 1-second TTL or a stale DB URL) persisted until the next explicit `cache_clear()` call — which never ran if a test was skipped or failed mid-teardown.

### Changes

**[`tests/conftest.py`](watson/backend/tests/conftest.py)** — Added an `autouse=True` fixture `_clear_caches()` that runs `get_settings.cache_clear()` and `get_engine.cache_clear()` **before and after every test** in the entire suite.

**6 test files** — Converted all `os.environ["KEY"] = value` inside fixtures and test functions to `monkeypatch.setenv("KEY", value)`, so the environment is automatically restored by pytest when the test exits (even on failure):
- [`test_confirmations.py`](watson/backend/tests/integration/test_confirmations.py) — `_make_app()` helper, `client` fixture, `client_ttl1` fixture, and 5 standalone test functions
- [`test_purchases.py`](watson/backend/tests/integration/test_purchases.py) — `client` fixture and `test_r10_second_app_sees_same_data_no_re_seed`
- [`test_reviews.py`](watson/backend/tests/integration/test_reviews.py) — `client` fixture
- [`test_analysis.py`](watson/backend/tests/integration/test_analysis.py) — `client` fixture and `test_analysis_null_when_model_fails`
- [`test_session.py`](watson/backend/tests/integration/test_session.py) — `client` fixture
- [`test_chat.py`](watson/backend/tests/integration/test_chat.py) — `_make_app()` helper, `client` fixture, and 7 standalone test functions

### Proof

| Run | Command | Result |
|-----|---------|--------|
| Reversed order (confirmations → purchases → reviews) | `pytest -q test_confirmations.py test_purchases.py test_reviews.py` | **54 passed** |
| Full suite normal order | `pytest -q` | **165 passed** |
```

### Tarefa 4c: modelo gpt-oss-120b e instruções reforçadas depois do teste com o Groq real

`4bcdfbf8f1a35805aaa363e6fd991d93`

```text
All done. Summary of every change:

---

**1. [`app/config.py`](watson/backend/app/config.py:44) — modelo padrão atualizado**

```python
llm_model: str = "groq:openai/gpt-oss-120b"
```

---

**2. [`app/domain/agent/__init__.py`](watson/backend/app/domain/agent/__init__.py:23) — 7 regras novas adicionadas ao `_SYSTEM_PROMPT` (regras 9–15)**

| # | Regra |
|---|-------|
| 9 | Conversa restrita à compra desta tela; negar pedidos sobre outros códigos/pessoas |
| 10 | Nunca revelar o score ao associado, nem oferecer revelar |
| 11 | Chamar `consultar_compra` antes de responder sobre dados da compra; `consultar_status` para prazo/situação |
| 12 | Usar rótulos, nunca códigos internos como `CARTAO_NAO_PRESENTE` |
| 13 | Não inventar botões/menus; usar `solicitar_revisao` para revisão humana |
| 14 | Nunca pedir data/valor/estabelecimento para identificar a compra |
| 15 | Máximo 5 frases por resposta, sem tabelas |

---

**3. [`tests/unit/test_agent_prompt.py`](watson/backend/tests/unit/test_agent_prompt.py) — 7 testes unitários novos + 1 para o llm_model padrão**

Cada regra nova tem seu próprio teste. Resultado: **173 passed**, nenhuma regressão.
```
