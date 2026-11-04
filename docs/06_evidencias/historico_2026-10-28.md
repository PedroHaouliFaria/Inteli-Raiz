# Índice de Evidências — Pessoa 4

**Data:** 28/10/2026
**Responsável:** Pessoa 4

Este diretório contém apenas registros realmente produzidos nesta execução. Evidências futuras (capturas de tela, logs de sessão integrada, resultados de D13) serão adicionadas após suas respectivas atividades.

---

## Evidências produzidas nesta execução

| ID | Tipo | Origem | Conteúdo | Data |
|---|---|---|---|---|
| P4-EVI-01 | Resultado de testes automatizados — **contagem relatada, sem log preservado** | Backend `origin/backend/confirmacao` commit `b39bbb9`; arquivos staged na worktree `../Inteli-Raiz-pessoa4` (98 entradas `A`, árvore **não limpa**); Python 3.12.5; `pip install -e ".[dev]"` | 151 testes passaram · 15 falharam (todos por `ModuleNotFoundError: No module named 'pydantic_ai'`) · 3 ignorados (scikit-learn ausente; `modelo_rf.joblib` existe mas não carregável). Contagem reportada a partir da saída exibida durante a execução; **o log original não foi salvo em arquivo separado** — não há arquivo `P4-EVI-01_pytest_summary.txt`; se necessário, reproduzir com as mesmas condições. | 28/10/2026 |
| P4-EVI-02 | Inspeção de código (referência) | Frontend `origin/watson` `212655c`; `watson/frontend/src/features/member-app/MemberPhone.jsx`; `watson/frontend/src/state/store.jsx` | Divergências P4-OBS-01 a P4-OBS-10 identificadas; ver `../matriz_cenarios_e_evidencias.md` §3 | 28/10/2026 |
| P4-EVI-03 | Inspeção de código (referência) | Backend commit `b39bbb9`; `app/main.py`, `app/api/routes/`, `app/db/tables/`, `app/db/seed.py`, `app/fixtures/purchases.json`, `app/domain/reviews/__init__.py`, `app/db/repositories/confirmations.py` | Rotas ativas identificadas (sessão, compras, confirmações, revisões, chat); tabelas e seed verificados; schemas do contrato inspecionados; lógica de estados confirmada (`DENY` → `RECUSADA_SIMULACAO` + revisão PROTECAO em paralelo; pedido de atendimento não muda status da compra) | 28/10/2026 |

---

## P4-EVI-01 — Resumo dos testes (contagem relatada)

> **Aviso:** o log original não foi preservado em arquivo. O resumo abaixo foi reportado a partir da saída exibida durante a execução. Para reproduzir: `cd ../Inteli-Raiz-pessoa4/watson/backend && pip install -e ".[dev]" && python -m pytest tests/ -v`.

**Ambiente declarado:**
- Worktree: `../Inteli-Raiz-pessoa4/watson/backend` (98 arquivos staged de `origin/backend/confirmacao` commit `b39bbb9`; HEAD da worktree = `8942cc5`; **árvore não limpa**)
- Python: 3.12.5
- pytest: 9.2.0
- Extras instalados: `.[dev]` — `pytest` e `httpx`; sem `pydantic_ai`, sem `risk` (scikit-learn), sem `watsonx`
- Banco: SQLite em tmp via fixture `tmp_path`
- Comando: `python -m pytest tests/ -v`
- `modelo_rf.joblib`: arquivo presente na worktree; scikit-learn 1.6.1 **não instalado**

**Resultado:**
```
platform darwin -- Python 3.12.5, pytest-9.2.0
151 passed, 15 failed, 3 skipped, 1 warning in 12.85s
```

**Testes que passaram relevantes para D11 (seleção):**
```
tests/integration/test_confirmations.py::test_r03_authorize_sets_liberada PASSED
tests/integration/test_confirmations.py::test_r03_deny_sets_recusada_and_opens_protecao_review PASSED
tests/integration/test_confirmations.py::test_r03_unsure_sets_revisao_pendente PASSED
tests/integration/test_confirmations.py::test_r04_response_after_ttl_returns_410_and_status_expirada PASSED
tests/integration/test_confirmations.py::test_r04_detail_after_ttl_shows_expirada PASSED
tests/integration/test_confirmations.py::test_r05_bruno_404_on_status PASSED
tests/integration/test_confirmations.py::test_r05_bruno_404_on_response PASSED
tests/integration/test_confirmations.py::test_r06_same_key_same_body_returns_200_replayed PASSED
tests/integration/test_confirmations.py::test_r06_same_key_different_body_returns_422 PASSED
tests/integration/test_confirmations.py::test_r06_new_key_different_response_returns_409_already_answered PASSED
tests/integration/test_confirmations.py::test_r06_parallel_same_response_single_event PASSED
tests/integration/test_confirmations.py::test_r10_second_app_preserves_status_and_response PASSED
tests/integration/test_confirmations.py::test_r11_response_has_simulation_true PASSED
tests/integration/test_confirmations.py::test_status_r11_simulation_true PASSED
tests/integration/test_purchases.py::test_r02_t007_detail_values PASSED
tests/integration/test_purchases.py::test_r05_bruno_gets_404_for_t007 PASSED
tests/integration/test_purchases.py::test_r07_t007_signals_match_fixture PASSED
tests/integration/test_purchases.py::test_r10_second_app_sees_same_data_no_re_seed PASSED
tests/integration/test_purchases.py::test_r11_all_purchase_responses_have_simulation_true PASSED
tests/integration/test_session.py::test_post_session_ana_returns_200_and_cookie PASSED
tests/integration/test_seed.py::test_seed_creates_three_purchases PASSED
tests/integration/test_seed.py::test_seed_is_idempotent PASSED
tests/integration/test_chat.py::test_get_chat_agent_available_false_without_key PASSED
```

**Testes que falharam (todos por `ModuleNotFoundError: No module named 'pydantic_ai'`):**
```
tests/integration/test_chat.py::test_r08_function_model_calls_consultar_compra FAILED
tests/integration/test_chat.py::test_s9_authorize_in_chat_does_not_change_status FAILED
tests/integration/test_chat.py::test_s9_no_tool_for_confirming_purchase FAILED
tests/integration/test_chat.py::test_r09_llm_error_returns_503_and_saves_message FAILED
tests/integration/test_chat.py::test_r09_after_llm_503_confirmation_still_works FAILED
tests/integration/test_chat.py::test_r10_second_app_preserves_chat_history FAILED
tests/integration/test_chat.py::test_agent_solicitar_revisao_creates_review_with_created_by_agente FAILED
tests/integration/test_chat.py::test_rate_limit_429_on_21st_message FAILED
tests/unit/test_agent_prompt.py::test_prompt_single_purchase_scope FAILED
tests/unit/test_agent_prompt.py::test_prompt_no_score_disclosure FAILED
tests/unit/test_agent_prompt.py::test_prompt_call_tool_before_answering FAILED
tests/unit/test_agent_prompt.py::test_prompt_no_internal_codes_in_response FAILED
tests/unit/test_agent_prompt.py::test_prompt_no_invented_buttons FAILED
tests/unit/test_agent_prompt.py::test_prompt_no_ask_for_purchase_identification FAILED
tests/unit/test_agent_prompt.py::test_prompt_short_responses FAILED
```

**Testes ignorados:**
```
tests/integration/test_analysis.py::test_t007_score_approximately_0_9917 SKIPPED
tests/integration/test_analysis.py::test_t003_score_approximately_0_0089 SKIPPED
```
Motivo: scikit-learn 1.6.1 não instalado (extra `risk` ausente no `.[dev]`); `modelo_rf.joblib` existe na worktree mas não pode ser carregado sem scikit-learn.

---

## Evidências futuras a produzir

| ID reservado | Quando produzir | Conteúdo esperado |
|---|---|---|
| P4-EVI-04 | Após C10 (Leonardo) | Captura da tela adaptada com três botões, sem biometria, sem mensagem de bloqueio |
| P4-EVI-05 | Após C13 (Leonardo + Lucas) | Log sanitizado de chamada à API de confirmação; captura da tela com estado após recarga |
| P4-EVI-06 | Após D13 Bloco A | Notas anonimizadas das entrevistas de experiência (Bloco A do roteiro P2) |
| P4-EVI-07 | Após D13 Bloco B | Tabela de resultados de D13 preenchida; achados P4-ACH-xx |
| P4-EVI-08 | Após Bob IDE Tasks | Capturas dos resumos de tarefas no Bob; exportar para `bob_sessions/<nome>/` |

---

## Nota sobre dados

Nenhum dado pessoal real foi coletado nesta execução. Todos os dados usados nos testes são fictícios (`C-ANA`, `C-BRUNO`, `T-007`, `T-003`, `T-011`). Nenhum dado sensível aparece neste índice.
