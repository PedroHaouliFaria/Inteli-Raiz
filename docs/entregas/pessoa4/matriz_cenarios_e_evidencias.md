# Matriz de Cenários e Evidências

**Versão:** 0.2 · **Data:** 28/10/2026 (corrigido após revisão do Codex)
**Responsável:** Pessoa 4
**Fontes:** plano `8942cc5` §9; D09 `f732159` §4; testes backend `b39bbb9` (staged em `../Inteli-Raiz-pessoa4`; executados em 28/10/2026).

Legenda de resultado: **passou** · **falhou** · **bloqueado por dependência** · **não executado** · **verificado no backend**

> **Nota sobre execução:** os resultados marcados como "verificado no backend" foram relatados a partir da saída exibida durante a execução de `pytest tests/ -v`. O log original não foi preservado em arquivo separado (ver P4-EVI-01 em `evidencias/README.md`). Esses resultados devem ser lidos como "relatado como aprovado, sem log preservado; reprodução pendente". As referências a nomes de teste identificam o caso que passou conforme relatado — não substituem a reprodução com log salvo.

---

## 1. Casos e resultados

| ID | Cenário | Requisitos | Método | Resultado | Evidência | Limitação |
|---|---|---|---|---|---|---|
| P4-T01 | Reconhece e autoriza (`AUTHORIZE`) | R03, R10, R11 | Interface + API | **bloqueado por dependência** | — | Frontend usa reducer local; PEN-01/PEN-03 |
| P4-T02 | Não reconhece (`DENY`) → compra fica em `RECUSADA_SIMULACAO`; revisão de proteção abre em paralelo (compra **não** vai para `REVISAO_PENDENTE`) | R03, R10, R11 | Interface + API | **bloqueado por dependência** | — | Frontend usa reducer local; PEN-01/PEN-03 |
| P4-T03 | Está em dúvida (`UNSURE`) → compra vai para `REVISAO_PENDENTE`; revisão de dúvida abre em paralelo | R03, R10 | Interface + API | **bloqueado por dependência** | — | PEN-01 (botão ausente) |
| P4-T04 | Pede ajuda (`POST /api/purchases/{case_id}/review`) sem responder; compra **permanece `AGUARDANDO_ASSOCIADO`**; confirmação continua válida | R03, R08 | Interface + API | **bloqueado por dependência** | — | PEN-02 (ação não implementada no frontend) |
| P4-T05 | Responde depois de pedir ajuda; resposta válida no prazo | R03, R04, R08 | Interface + API | **bloqueado por dependência** | — | PEN-01/PEN-02/PEN-03 |
| P4-T06 | Expira sem resposta (inclusive após pedir ajuda); resposta tardia rejeitada; prazo não reiniciado por pedido de revisão anterior | R04 | Teste de integração do backend | **verificado no backend** | `test_r04_response_after_ttl_returns_410_and_status_expirada` passou; `test_r04_detail_after_ttl_shows_expirada` passou | Verificado na API, não pela interface |
| P4-T07 | Duplo clique / resposta duplicada com mesma chave | R06 | Teste de integração do backend | **verificado no backend** | `test_r06_same_key_same_body_returns_200_replayed` passou; `test_r06_parallel_same_response_single_event` passou | Verificado na API, não pela interface |
| P4-T07b | Resposta conflitante com chave nova | R06 | Teste de integração do backend | **verificado no backend** | `test_r06_new_key_different_response_returns_409_already_answered` passou | — |
| P4-T08 | Outro associado fictício (C-BRUNO) não acessa compra de C-ANA | R05 | Teste de integração do backend | **verificado no backend** | `test_r05_bruno_404_on_response` passou; `test_r05_bruno_gets_404_for_t007` passou | Verificado na API; sem sessão via interface |
| P4-T09 | Chat falha / agente indisponível; confirmação continua | R09 | Teste de integração (parcial) | **parcialmente verificado** | `test_get_chat_agent_available_false_without_key` passou; `test_r09_after_llm_503_confirmation_still_works` bloqueado por `pydantic_ai` ausente | Agente não instalado |
| P4-T10 | Modelo falha; sem score inventado | R09, R01 | Teste de integração do backend | **verificado no backend** | `test_analysis_null_when_model_fails` passou | Modelo real não integrado ao fluxo de confirmação |
| P4-T11 | Reinício preserva status e resposta | R10 | Teste de integração do backend | **verificado no backend** | `test_r10_second_app_preserves_status_and_response` passou; `test_r10_second_app_sees_same_data_no_re_seed` passou | Verificado na API; sem teste via interface |
| P4-T12 | Agente não autoriza compra pelo associado | R09 | Teste de integração (preparado) | **bloqueado por dependência** | `test_s9_authorize_in_chat_does_not_change_status` preparado; falha por `pydantic_ai` ausente | Extra `agent` não instalado |

---

## 2. Cobertura de requisitos

| Requisito | Descrição | Cobertura | Evidência disponível |
|---|---|---|---|
| R01 | Avaliação automática de compra | Parcial — tabelas e schema prontos; score não integrado ao fluxo de confirmação | `test_analysis_null_when_model_fails` (comportamento de falha) |
| R02 | Confirmação vinculada à compra | Verificado no backend | `test_r02_t007_detail_values` passou |
| R03 | Três respostas com resultados distintos | Verificado no backend; **não verificável pela interface** | `test_r03_authorize_sets_liberada`, `test_r03_deny_sets_recusada_and_opens_protecao_review`, `test_r03_unsure_sets_revisao_pendente` passaram |
| R04 | Expiração | Verificado no backend | `test_r04_response_after_ttl_returns_410_and_status_expirada` passou |
| R05 | Autorização por usuário | Verificado no backend | `test_r05_bruno_404_on_response` passou; `test_r05_bruno_gets_404_for_t007` passou |
| R06 | Idempotência e concorrência | Verificado no backend | `test_r06_*` (4 testes) passaram |
| R07 | Explicação fiel (sinais) | Verificado no backend | `test_r07_t007_signals_match_fixture` passou |
| R08 | Dúvida contextual (agente) | **Não verificado** — agente não instalado | — |
| R09 | Erro seguro | Parcial — falha de modelo verificada; falha de LLM bloqueada | `test_analysis_null_when_model_fails` passou |
| R10 | Histórico preservado | Verificado no backend | `test_r10_second_app_preserves_status_and_response` passou |
| R11 | Transparência (simulação) | Verificado no backend | `test_r11_response_has_simulation_true` passou; `test_status_r11_simulation_true` passou |
| R12 | Acesso reproduzível | **Não verificado** — integração bloqueada | — |

---

## 3. Achados de inspeção da interface (frontend `212655c`)

| ID | Achado | Tipo | Gravidade | Requisito | Referência |
|---|---|---|---|---|---|
| P4-OBS-01 | Dois botões (`itWasMe`/`notMe`) em vez de três (`AUTHORIZE`/`DENY`/`UNSURE`) | Divergência de código | Crítica | R03 | `MemberPhone.jsx` linha 30–33 |
| P4-OBS-02 | Tela `biometrics` obrigatória entre `itWasMe` e confirmação | Divergência de código | Crítica | R03, decisão 4 do plano | `MemberPhone.jsx` linha 34–40; `store.jsx` `itWasMe` case |
| P4-OBS-03 | Tela `protected`: "Bloqueamos o cartão...nada foi cobrado...cartão novo em 7 dias" | Texto incorreto — promessa operacional fora do escopo | Crítica | R11, §3 plano | `MemberPhone.jsx` linha 51 |
| P4-OBS-04 | Link "Prefiro falar com uma pessoa" sem ação (`href="#"`, `onClick e.preventDefault()`); endpoint correto: `POST /api/purchases/{case_id}/review`; ação **não** muda o status da compra — compra permanece `AGUARDANDO_ASSOCIADO` | Funcionalidade ausente | Alta | R08 | `MemberPhone.jsx` linha 55 |
| P4-OBS-05 | Estado gerido no reducer do browser; recarga da página perde o estado | Sem persistência via API | Crítica | R10 | `store.jsx` — todo o reducer usa estado in-memory |
| P4-OBS-06 | `screen='reviewing'`: "Ela segue pausada e nada foi cobrado" — promessa operacional | Texto incorreto | Média | R11 | `MemberPhone.jsx` linha 53 |
| P4-OBS-07 | `store.jsx` `notMe` case: adiciona evento "Cartão bloqueado pelo Watson" | Texto de evento incorreto (sem ser atualizado na UI pública) | Alta | R11 | `store.jsx` `notMe` case |
| P4-OBS-08 | Ausência de tela de expiração (`CONFIRMACAO_EXPIRADA`) | Estado não representado | Alta | R04 | `MemberPhone.jsx` — nenhum `screen='expired'` |
| P4-OBS-09 | Prazo da confirmação não exibido; relógio do browser seria a única referência | Prazo não visível | Média | R04 | Ausência em `MemberPhone.jsx` |
| P4-OBS-10 | `InlineNotification` de autenticidade existente ("Nunca pedimos senha") | Positivo — manter e refinar | — | R11 | `MemberPhone.jsx` linha 19 |

---

## 4. Vinculação com hipóteses da Pessoa 2

| Hipótese (P2) | Achado desta inspeção | Impacto no teste |
|---|---|---|
| HIP-01: confundir recusa com bloqueio de cartão | P4-OBS-03 — tela `protected` diz explicitamente que o cartão foi bloqueado | D13 Tarefa 2/C5 pode registrar falsos positivos causados pela tela atual, não por confusão genuína |
| HIP-02: não saber se pode responder após pedir ajuda | P4-OBS-04 — link sem ação; comportamento não testável | Bloco B do roteiro não pode ser executado sem C10/C13 |
| HIP-03: nome ambíguo gera decisão equivocada | P4-OBS-05 + ausência do agente | Tarefa 3 não pode ser testada sem agente real |
| HIP-05: não saber efeito de cada resposta | P4-OBS-01 — terceiro botão ausente | C2 só cobre dois efeitos no estado atual |
| HIP-09: não entender o desfecho | P4-OBS-03/P4-OBS-06 — textos de resultado com promessas incorretas | Compreensão medida em C1/C2 seria influenciada pelo texto errado |
