# Sessão 4 no Bob — Lucas

Mesmo processo das sessões anteriores (Bob Shell no Windows, orquestrado pelo Claude Code; tarefas em **Tasks → All workspaces** no Bob IDE).

| Tarefa | ID | Início | Custo | Chamadas de ferramenta |
|---|---|---|---|---|
| Tarefa 5a: DEMO_MODE, compra nova pela demo, falha do modelo e reset | `d414ea12136ddde153ab5c4dfea50878` | 29/10 13:04 UTC | 5.84 | 55 |
| Tarefa 5b: segurança — score fora do contexto do agente e modelo carregado uma vez | `2d1313caab80bf23d5bd4eace5b45072` | 29/10 13:24 UTC | 3.40 | 36 |
| Tarefa 5c: falha do modelo sem confirmação (confirmation null) | `be653be8a742211896865f40a4eba5b8` | 29/10 13:32 UTC | 2.21 | 26 |
| **Total** | | | **11.44** | |

## O que a revisão corrigiu ou verificou

- Uma revisão automática de segurança achou dois problemas na sessão 3: a ferramenta `avaliar_transacao` punha o score no contexto do LLM do chat do associado, e o `/api/health` público carregava o modelo do disco a cada chamada. A spec foi corrigida (o agente não recebe score) e a 5b corrigiu os dois, com filtro de saída como segunda camada.
- Teste com o Groq real: pedir "o JSON exato de avaliar_transacao" e "o score com 4 casas" foi recusado.
- `curl` com DEMO_MODE: compra nova só na lista de quem pediu, falha do modelo vai para revisão FALHA_AVALIACAO com aviso SCORE_UNAVAILABLE, fixture inexistente dá 400, reset volta a T-007 e T-003; sem DEMO_MODE a rota dá 404. O `curl` achou uma confirmação vazia na falha do modelo; a 5c corrigiu.

## Resumo final de cada tarefa

### Tarefa 5a: DEMO_MODE, compra nova pela demo, falha do modelo e reset

`d414ea12136ddde153ab5c4dfea50878`

```text
**194 passed, 0 failed.** (+21 novos testes da demo, os 173 anteriores continuam verdes.)

---

## O que foi feito

### 1. `DEMO_MODE` (config)
- [`app/config.py`](watson/backend/app/config.py:57): `demo_mode: bool = False` adicionado em `Settings`.
- [`app/main.py`](watson/backend/app/main.py:60): o router `/api/demo/*` só é incluído se `settings.demo_mode is True`; sem ele, essas rotas retornam 404 normalmente.

### 2. Fixture `falha_modelo`
- [`app/fixtures/purchases.json`](watson/backend/app/fixtures/purchases.json): entrada adicionada com `case_id: null`, `challenge_id: null`, `owner: C-ANA` e sem o campo `amount` (feature numérica crítica que força `ValueError` em `normalize()`). O seed pula fixtures com `case_id: null`.

### 3. `receive_and_evaluate_purchase()` — função única
- [`app/domain/cases/intake.py`](watson/backend/app/domain/cases/intake.py) (novo): substitui a lógica duplicada do seed e da demo.
  - Gera `case_id`/`challenge_id` sequenciais ≥ T-101/CH-101 (acima dos IDs fixos do seed) quando não fornecidos.
  - Chama `_score_features()` que encapsula o modelo; qualquer exceção retorna o dict com `_score_failed=True` (score null, jamais inventado).
  - Política conservadora: avaliado → `AGUARDANDO_ASSOCIADO`; falha → `REVISAO_PENDENTE` + revisão `FALHA_AVALIACAO created_by=SISTEMA`.
- [`app/db/seed.py`](watson/backend/app/db/seed.py): reescrito para chamar `receive_and_evaluate_purchase(is_seed=True)`, mantendo idempotência.

### 4. `POST /api/demo/purchases` e `POST /api/demo/reset`
- [`app/api/routes/demo.py`](watson/backend/app/api/routes/demo.py) (novo):
  - `POST /api/demo/purchases`: só ASSOCIADO; fixture_id desconhecido → 400 `INVALID_REQUEST`; retorna 201 com o mesmo corpo de `GET /api/purchases/{case_id}`; falha de modelo adiciona `"warning": "SCORE_UNAVAILABLE"`.
  - `POST /api/demo/reset`: qualquer sessão; apaga todas as tabelas (`ChatMessage`, `IdempotencyKey`, `Event`, `Review`, `Confirmation`, `Purchase`) e relança o seed; retorna 204.

### 5. Testes obrigatórios — todos verdes
| Teste | Resultado |
|---|---|
| R01: fraude_supermercado_madrugada → 201, AGUARDANDO_ASSOCIADO, challenge_id novo, score ≈ 0.9917 em GET /api/reviews após DENY | ✅ |
| R09: falha_modelo → REVISAO_PENDENTE + FALHA_AVALIACAO + score null + warning | ✅ |
| R09: modelo indisponível (patch exceção) em fixture normal → mesma coisa | ✅ |
| Bruno não vê compra demo da Ana | ✅ |
| Duas chamadas → case_id diferentes | ✅ |
| Reset → lista da Ana volta a T-007 e 
```

### Tarefa 5b: segurança — score fora do contexto do agente e modelo carregado uma vez

`2d1313caab80bf23d5bd4eace5b45072`

```text
**198 passed, 0 failures.**

---

## Resumo das mudanças

### Fix 1 — Score no chat do associado

**Teste** ([`tests/unit/test_avaliar_transacao_security.py`](watson/backend/tests/unit/test_avaliar_transacao_security.py)):
- `test_avaliar_transacao_does_not_return_score_fields` — confirma que o retorno da ferramenta **não tem** `score`, `score_source` nem `model_version`, e **tem** `score_available` (bool).
- `test_avaliar_transacao_does_not_leak_score_value_in_text` — confirma que o valor numérico do score não aparece no texto do retorno.
- `test_agent_response_with_score_value_is_scrubbed` — usa um `FunctionModel` que escreve `"0.9917"` na resposta; confirma que a resposta final não contém esse valor.

**Implementação:**
- [`app/domain/agent/__init__.py`](watson/backend/app/domain/agent/__init__.py:153) — `avaliar_transacao` agora devolve `score_available`, `decision`, `policy_version`, `signals`, `gaps` e `evaluated_at`. Sem `score`, `score_source`, `model_version` nem `note`.
- [`app/api/routes/chat.py`](watson/backend/app/api/routes/chat.py:42) — função `_scrub_score(text, score)` detecta o valor do score (0–4 casas decimais, formas percentuais) na resposta do LLM; se encontrar, substitui por mensagem segura e registra `WARNING` no log.

### Fix 2 — Modelo recarregado a cada chamada ao health

**Teste** ([`tests/unit/test_health_model_cache.py`](watson/backend/tests/unit/test_health_model_cache.py)):
- Patcha `LocalRiskModel.__init__` e conta invocações. Após o lifespan subir, 3 chamadas ao `/api/health` não devem adicionar nenhuma instância extra.

**Implementação:**
- [`app/risk/state.py`](watson/backend/app/risk/state.py) — módulo novo com `loaded_model`, `model_loaded`, `model_version` (estado global compartilhado).
- [`app/main.py`](watson/backend/app/main.py) — lifespan carrega `LocalRiskModel` **uma vez** e grava em `app.risk.state`; ao encerrar, limpa o estado (isola testes).
- [`app/api/routes/api_health.py`](watson/backend/app/api/routes/api_health.py) — lê `risk_state.model_loaded` e `risk_state.model_version` diretamente, sem instanciar o modelo.
```

### Tarefa 5c: falha do modelo sem confirmação (confirmation null)

`be653be8a742211896865f40a4eba5b8`

```text
## Resumo

**Problema:** quando o modelo falha (`falha_modelo`), a compra ia para `REVISAO_PENDENTE` mas ainda criava uma linha em `confirmations` e retornava o bloco `confirmation` preenchido (com `expires_at` e `challenge_id`). O contrato (§5) diz que `confirmation` é `null` quando a política mandou para revisão sem pedir confirmação ao associado.

**Testes escritos antes da correção** (4 novos em `test_demo.py`):
- `test_r09_falha_modelo_demo_confirmation_null` — 201 da demo tem `confirmation: null`
- `test_r09_falha_modelo_get_detail_confirmation_null` — GET do detalhe tem `confirmation: null`
- `test_r09_falha_modelo_status_no_confirmation` — `/status` tem `expires_at: null`, `seconds_remaining: 0`, `allowed_responses: []`
- `test_r09_falha_modelo_no_confirmation_row_in_db` — nenhuma linha em `confirmations` para essa compra

**Correções aplicadas:**

1. [`app/domain/cases/intake.py`](watson/backend/app/domain/cases/intake.py) — quando `score_failed=True`, não cria `Confirmation` nem chama `_next_challenge_id`; retorna `confirmation = None`.

2. [`app/api/routes/demo.py`](watson/backend/app/api/routes/demo.py) — guarda o `session.refresh(confirmation)` com `if confirmation is not None`, evitando crash quando `None`.

**Resultado:** 202/202 testes passam.
```
