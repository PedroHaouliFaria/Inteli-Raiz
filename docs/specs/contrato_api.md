# Spec: contrato da API JSON

> **Versão do contrato:** `v1` · 28/10/2026 · **Responsável:** Lucas (backend e agente).
> **Base:** [`plano_implementacao.md`](../plano_implementacao.md) v2.2, §3 (regras), §4 (arquitetura e decisões de 27/10), §5 (contratos e estados), §6 (requisitos R01–R12) e §9 (testes). Esta spec é a etapa 2 do backlog (§8.2).
> **Onde fica o código:** `watson/backend` (FastAPI, SQLAlchemy sobre SQLite) e `watson/frontend` (React + Carbon), conforme o alinhamento de 28/10 no plano.
> **Para que serve:** quem fizer o front trabalha só com este documento e os exemplos, sem esperar o backend. Quem fizer o backend implementa exatamente isto no Bob. Mudança de contrato passa por PR nesta spec antes de ir para o código.

## 1. Escopo

**Dentro:** sessão do associado fictício, lista e detalhe de compras, status, resposta à confirmação, chat com o agente, pedido de revisão, lista mínima de exceções para o analista, saúde do serviço e endpoints de demonstração.

**Fora do v1:** autenticação real, resolução de revisão pelo analista (só a lista), notificações push, streaming da resposta do chat, multi-idioma, ações financeiras reais.

## 2. Convenções

| Tema | Regra |
|---|---|
| Base | Todos os caminhos deste contrato começam com `/api`. Exemplo: `GET /api/purchases`. As rotas que o Watson já tinha (`/health`, `/model-lab`) ficam como estão até o front migrar. |
| Formato | JSON em UTF-8, nomes em `snake_case`, valores de enum em `MAIUSCULAS` como no plano. |
| Datas | ISO 8601 em UTC, com `Z` (`2026-10-28T03:12:00Z`). O front converte para o fuso de quem vê. |
| Dinheiro | Objeto `{"value": "149.58", "currency": "BRL"}`. O valor é **string decimal** para não perder centavos em `float`. |
| IDs | `case_id` = `T-<n>`, `challenge_id` = `CH-<n>`, `analysis_id` = `A-<n>-v<k>`, `review_id` = `REV-<n>`, protocolo = `RZ-<AAAAMMDD>-<n>`. O front trata todos como texto opaco. |
| Simulação | Toda resposta que fala de compra traz `"simulation": true` (R11). |
| Identidade | **Nunca** vem no corpo nem na URL. O backend lê o associado do cookie de sessão (§4). Um `customer_id` enviado pelo cliente é ignorado. |
| Compra de outra pessoa | Responde **404**, igual a uma compra que não existe. Não confirma que o ID existe (R05). |
| Origem | Front e API na **mesma origem**: em desenvolvimento, o Vite do `watson/frontend` faz proxy de `/api` para o backend; em produção, o FastAPI serve o build estático. Assim o cookie funciona com `SameSite=Lax` e as rotas `/api` não dependem de CORS. Se o front ficar em outro domínio, isso vira decisão de PR nesta spec. |
| Documentação viva | Os modelos Pydantic do backend carregam os exemplos desta spec (`json_schema_extra`), e o `/docs` do FastAPI mostra o mesmo contrato. |

### Envelope de erro

Todo erro 4xx e 5xx usa o mesmo formato:

```json
{
  "error": {
    "code": "CONFIRMATION_EXPIRED",
    "message": "O prazo para responder a esta compra terminou. Ela não foi autorizada.",
    "details": {"status": "CONFIRMACAO_EXPIRADA", "expired_at": "2026-10-28T03:27:00Z"}
  }
}
```

`message` é texto para o associado, em português. `code` é o que o front usa para decidir o que mostrar. `details` é opcional.

| HTTP | `code` | Quando |
|---|---|---|
| 400 | `INVALID_REQUEST` | Corpo malformado ou campo fora do enum. |
| 401 | `NOT_AUTHENTICATED` | Sem sessão ou sessão inválida. |
| 403 | `FORBIDDEN_ROLE` | Associado chamando endpoint de analista, ou o inverso. |
| 404 | `NOT_FOUND` | Recurso não existe **ou** é de outra pessoa. |
| 409 | `VERSION_MISMATCH` | A versão enviada não é a atual: a tela está desatualizada. |
| 409 | `ALREADY_ANSWERED` | A confirmação já tem resposta diferente da enviada. |
| 409 | `NOT_AWAITING_RESPONSE` | A compra não está em `AGUARDANDO_ASSOCIADO` (já liberada, já em revisão etc.). |
| 410 | `CONFIRMATION_EXPIRED` | Resposta depois do prazo. |
| 422 | `IDEMPOTENCY_KEY_REUSED` | Mesma `Idempotency-Key` com corpo diferente. |
| 428 | `IDEMPOTENCY_KEY_REQUIRED` | `POST` de resposta sem `Idempotency-Key`. |
| 429 | `RATE_LIMITED` | Excesso de mensagens no chat (§9). |
| 503 | `AGENT_UNAVAILABLE` | O LLM falhou ou estourou o tempo. A confirmação continua funcionando. |
| 503 | `SCORE_UNAVAILABLE` | O modelo falhou ao avaliar uma compra (só nos endpoints de demonstração). |
| 500 | `INTERNAL_ERROR` | Erro não previsto. A mensagem não traz stack trace nem dado interno. |

## 3. Estados

Iguais aos do §5 do plano. O front mostra o rótulo e nunca depende só de cor.

| `status` | Rótulo para o associado | Terminal? |
|---|---|---|
| `RECEBIDA` | Compra recebida | não |
| `EM_AVALIACAO` | Em avaliação | não |
| `AGUARDANDO_ASSOCIADO` | Aguardando sua resposta | não |
| `LIBERADA_SIMULACAO` | Compra liberada (simulação) | sim |
| `RECUSADA_SIMULACAO` | Compra recusada (simulação) | sim |
| `REVISAO_PENDENTE` | Em revisão por um analista | sim no v1 |
| `CONFIRMACAO_EXPIRADA` | Prazo encerrado, compra não autorizada | sim |

```
RECEBIDA → EM_AVALIACAO → LIBERADA_SIMULACAO
                        → AGUARDANDO_ASSOCIADO → LIBERADA_SIMULACAO     (AUTHORIZE)
                                               → RECUSADA_SIMULACAO     (DENY, abre revisão de proteção)
                                               → REVISAO_PENDENTE       (UNSURE)
                                               → CONFIRMACAO_EXPIRADA   (prazo)
                        → REVISAO_PENDENTE     (dados ausentes, falha do modelo, caso fora da política)
```

**Versão.** Cada compra tem um inteiro `version`, que começa em 1 e sobe a cada transição de estado. O front envia a versão que mostrou; se ela não for a atual, a resposta é 409 `VERSION_MISMATCH` (§3 do plano: "resposta a versão antiga").

**Expiração.** O prazo vem de `CONFIRMATION_TTL_SECONDS` (padrão 900, ou 15 min; valor experimental, não prática do Sicredi). O backend confere o prazo em **toda** leitura e resposta. Se venceu, grava `CONFIRMACAO_EXPIRADA` e o evento na mesma transação antes de responder. O relógio do browser só serve para mostrar a contagem.

**Revisão não muda o estado sozinha.** Um pedido de revisão feito pelo chat (agente) ou pelo botão de ajuda enquanto a compra aguarda resposta **não** fecha a confirmação: a compra continua em `AGUARDANDO_ASSOCIADO`, ganha um protocolo e o associado ainda pode autorizar ou recusar. Só os três botões e o prazo mudam o estado. Assim, nem o agente nem um prompt malicioso conseguem decidir pela pessoa (§3 e §9 do plano).

## 4. Sessão

Login fictício: o associado escolhe uma das pessoas fictícias e o servidor grava um cookie assinado (Starlette `SessionMiddleware` ou `itsdangerous`, com segredo em `SESSION_SECRET`). Cookie `raiz_session`, `HttpOnly`, `SameSite=Lax`, `Secure` em produção, validade de 8 h.

### `GET /api/session/personas`

Público. Lista quem pode entrar.

```json
{
  "personas": [
    {"persona_id": "ana", "display_name": "Ana Souza (fictícia)", "role": "ASSOCIADO"},
    {"persona_id": "bruno", "display_name": "Bruno Lima (fictício)", "role": "ASSOCIADO"},
    {"persona_id": "carla", "display_name": "Carla Reis, analista (fictícia)", "role": "ANALISTA"}
  ],
  "simulation": true
}
```

Dois associados permitem testar acesso cruzado (R05). A analista existe só para a lista de exceções (§9).

### `POST /api/session`

```json
{"persona_id": "ana"}
```

**200** + `Set-Cookie: raiz_session=...`

```json
{"persona_id": "ana", "display_name": "Ana Souza (fictícia)", "role": "ASSOCIADO", "simulation": true}
```

**400** `INVALID_REQUEST` se o `persona_id` não existe.

### `GET /api/session`

**200** com o mesmo corpo do `POST`. **401** `NOT_AUTHENTICATED` sem sessão. O front chama ao abrir para saber se mostra a tela de entrada.

### `DELETE /api/session`

**204**, apaga o cookie.

## 5. Compras

### `GET /api/purchases`

Compras do associado da sessão, da mais recente para a mais antiga. Sem paginação no v1 (são poucas por pessoa).

```json
{
  "purchases": [
    {
      "case_id": "T-007",
      "merchant_display": "Supermercado (nome do estabelecimento não disponível)",
      "amount": {"value": "149.58", "currency": "BRL"},
      "occurred_at": "2026-10-25T06:12:00Z",
      "status": "AGUARDANDO_ASSOCIADO",
      "status_label": "Aguardando sua resposta",
      "expires_at": "2026-10-28T03:27:00Z"
    },
    {
      "case_id": "T-003",
      "merchant_display": "Farmácia (nome do estabelecimento não disponível)",
      "amount": {"value": "15.68", "currency": "BRL"},
      "occurred_at": "2026-10-19T21:40:00Z",
      "status": "LIBERADA_SIMULACAO",
      "status_label": "Compra liberada (simulação)",
      "expires_at": null
    }
  ],
  "simulation": true
}
```

### `GET /api/purchases/{case_id}`

Tudo o que a tela principal precisa (§2 do plano): compra, alerta, pergunta, respostas permitidas e resultado.

**200**, compra aguardando resposta:

```json
{
  "case_id": "T-007",
  "version": 2,
  "status": "AGUARDANDO_ASSOCIADO",
  "status_label": "Aguardando sua resposta",
  "purchase": {
    "merchant_name": null,
    "merchant_category": {"mcc": "5411", "label": "Supermercado"},
    "merchant_display": "Supermercado (nome do estabelecimento não disponível)",
    "amount": {"value": "149.58", "currency": "BRL"},
    "occurred_at": "2026-10-25T06:12:00Z",
    "channel": "CARTAO_NAO_PRESENTE",
    "channel_label": "Compra online ou por telefone",
    "card": {"brand": "BANDEIRA_A", "type": "credito", "last4": "2938"}
  },
  "alert": {
    "headline": "Esta compra tem características diferentes do seu uso habitual.",
    "signals": [
      {"code": "CARTAO_NAO_PRESENTE", "label": "Feita sem o cartão físico (online ou por telefone).", "source": "regra"},
      {"code": "MADRUGADA", "label": "Feita de madrugada, às 3h.", "source": "regra"},
      {"code": "PRIMEIRA_COMPRA_CARTAO", "label": "Primeira compra registrada com este cartão.", "source": "regra"}
    ],
    "disclaimer": "Os motivos acima são regras sobre os dados da compra. Eles não explicam sozinhos a avaliação do modelo."
  },
  "confirmation": {
    "challenge_id": "CH-007",
    "question": "Você reconhece e autoriza esta compra?",
    "allowed_responses": [
      {"response": "AUTHORIZE", "label": "Reconheço e autorizo"},
      {"response": "DENY", "label": "Não reconheço"},
      {"response": "UNSURE", "label": "Estou em dúvida"}
    ],
    "expires_at": "2026-10-28T03:27:00Z",
    "answered": null
  },
  "review": null,
  "result": null,
  "policy_version": "confirmacao-v2",
  "simulation": true
}
```

**200**, mesma compra depois de "Não reconheço":

```json
{
  "case_id": "T-007",
  "version": 3,
  "status": "RECUSADA_SIMULACAO",
  "status_label": "Compra recusada (simulação)",
  "purchase": {"...": "igual ao exemplo anterior"},
  "alert": {"...": "igual ao exemplo anterior"},
  "confirmation": {
    "challenge_id": "CH-007",
    "question": "Você reconhece e autoriza esta compra?",
    "allowed_responses": [],
    "expires_at": "2026-10-28T03:27:00Z",
    "answered": {"response": "DENY", "answered_at": "2026-10-28T03:15:42Z"}
  },
  "review": {"review_id": "REV-12", "protocol": "RZ-20261028-0012", "kind": "PROTECAO", "status": "ABERTA"},
  "result": {
    "title": "Compra recusada na simulação",
    "description": "Registramos que você não reconhece esta compra. Um analista vai revisar o caso. O cartão não foi bloqueado.",
    "next_steps": ["Guarde o protocolo RZ-20261028-0012.", "Você pode acompanhar o status nesta tela."]
  },
  "policy_version": "confirmacao-v2",
  "simulation": true
}
```

Regras dos campos:

- `confirmation` é `null` quando a política liberou direto ou mandou para revisão sem pedir confirmação.
- `allowed_responses` fica **vazio** fora de `AGUARDANDO_ASSOCIADO`. O front desenha os botões a partir dessa lista, não a partir do `status`.
- `merchant_name` é sempre `null` na base sintética, que não tem nome de estabelecimento. `merchant_display` usa a categoria do MCC. O agente não inventa um nome (§9 do plano).
- `occurred_at` é sintético: a base só tem `hora` e `dia_semana`, então a fixture monta uma data coerente com eles.
- `card.last4` sai dos 4 últimos dígitos do `card_id` sintético.
- `channel` é `CARTAO_PRESENTE` ("Compra presencial") ou `CARTAO_NAO_PRESENTE` ("Compra online ou por telefone"), a partir de `modalidade_transacao`. T-003 e T-011 são presenciais.
- Se nenhuma regra disparar, `signals` vem vazio e `headline` diz: "Pedimos sua confirmação por precaução. Esta compra não tem um sinal de alerta específico." A tela não inventa um motivo.
- Na lista (`GET /api/purchases`), `expires_at` só vem preenchido enquanto o status é `AGUARDANDO_ASSOCIADO`.
- `signals` vêm de **regras** sobre os dados da compra (`source: "regra"`). O conjunto de regras é do dono dos sinais (Pedro R. na recomendação); este contrato fixa só o formato. Só vira sinal a feature com significado documentado: as de velocidade e distância (`cp_card_term_vel_1h` etc.) não têm definição na base e ficam de fora até alguém documentá-las.
- **O score do modelo não aparece para o associado.** Ele não é probabilidade calibrada (§7 do plano), e "99% de chance de fraude" na tela induziria a decisão. O score fica na análise gravada e aparece só para a analista (`GET /api/reviews`). O agente conversa com o associado, então também não recebe o score (§10).
- Nunca aparecem: `feedback_label`, `customer_id`, `card_id` completo, renda, saldo ou limite.

**404** `NOT_FOUND`, se a compra não existe ou é de outra pessoa.

### `GET /api/purchases/{case_id}/status`

Versão leve para atualizar a tela e para a ferramenta `consultar_status`. O front pode chamar a cada 5 s enquanto o status for `AGUARDANDO_ASSOCIADO` (a expiração aparece sem recarregar).

```json
{
  "case_id": "T-007",
  "version": 2,
  "status": "AGUARDANDO_ASSOCIADO",
  "status_label": "Aguardando sua resposta",
  "expires_at": "2026-10-28T03:27:00Z",
  "seconds_remaining": 642,
  "allowed_responses": ["AUTHORIZE", "DENY", "UNSURE"],
  "review_protocol": null,
  "next_steps": ["Responda se reconhece a compra antes do prazo.", "Se tiver dúvida, pergunte no chat ou escolha \"Estou em dúvida\"."],
  "simulation": true
}
```

Expirada:

```json
{
  "case_id": "T-007",
  "version": 3,
  "status": "CONFIRMACAO_EXPIRADA",
  "status_label": "Prazo encerrado, compra não autorizada",
  "expires_at": "2026-10-28T03:27:00Z",
  "seconds_remaining": 0,
  "allowed_responses": [],
  "review_protocol": null,
  "next_steps": ["A compra não foi autorizada.", "Se ela for sua, peça uma revisão."],
  "simulation": true
}
```

## 6. Resposta à confirmação

### `POST /api/confirmations/{challenge_id}/response`

É a **única** forma de autorizar ou recusar. Só a sessão humana chama; o agente não tem ferramenta para isso (§4 do plano).

Cabeçalhos: `Idempotency-Key: <uuid v4 gerado pelo front a cada clique novo>`.

```json
{"response": "AUTHORIZE", "version": 2}
```

`response` ∈ `AUTHORIZE`, `DENY`, `UNSURE`.

**200**, resposta registrada:

```json
{
  "challenge_id": "CH-007",
  "case_id": "T-007",
  "response": "AUTHORIZE",
  "answered_at": "2026-10-28T03:15:42Z",
  "version": 3,
  "status": "LIBERADA_SIMULACAO",
  "status_label": "Compra liberada (simulação)",
  "review_protocol": null,
  "result": {
    "title": "Compra autorizada na simulação",
    "description": "Registramos que você reconhece e autoriza esta compra. Nenhuma transação real foi feita.",
    "next_steps": []
  },
  "replayed": false,
  "simulation": true
}
```

Efeito de cada resposta (§3 do plano):

| `response` | `status` final | Revisão |
|---|---|---|
| `AUTHORIZE` | `LIBERADA_SIMULACAO` | nenhuma nova; se já havia revisão aberta pelo chat, ela continua aberta |
| `DENY` | `RECUSADA_SIMULACAO` | abre revisão `kind: PROTECAO`; o cartão não é bloqueado |
| `UNSURE` | `REVISAO_PENDENTE` | abre revisão `kind: DUVIDA`, ou reaproveita a que o chat já abriu |

**Idempotência e concorrência (R06).** O servidor grava resposta, novo estado, revisão e evento numa única transação, com a linha da confirmação travada (`BEGIN IMMEDIATE` no SQLite).

| Situação | Resposta |
|---|---|
| Mesma `Idempotency-Key`, mesmo corpo | **200** com o resultado original e `"replayed": true`. Nada é gravado de novo. |
| Mesma `Idempotency-Key`, corpo diferente | **422** `IDEMPOTENCY_KEY_REUSED`. |
| Chave nova, mas a confirmação já tem a **mesma** resposta | **200** com o resultado existente e `"replayed": true` (dois cliques, duas abas). |
| Chave nova e resposta **diferente** da registrada | **409** `ALREADY_ANSWERED`, com `details.response` e `details.status` atuais. Não sobrescreve. |
| `version` diferente da atual | **409** `VERSION_MISMATCH`, com `details.current_version`. O front recarrega o detalhe. |
| Compra fora de `AGUARDANDO_ASSOCIADO` por outro motivo | **409** `NOT_AWAITING_RESPONSE`, com `details.status`. |
| Depois do prazo | **410** `CONFIRMATION_EXPIRED`. O estado vira `CONFIRMACAO_EXPIRADA`. |
| Desafio de outra pessoa ou inexistente | **404** `NOT_FOUND`. |
| Sem `Idempotency-Key` | **428** `IDEMPOTENCY_KEY_REQUIRED`. |

Exemplo de conflito:

```json
{
  "error": {
    "code": "ALREADY_ANSWERED",
    "message": "Esta compra já foi respondida como \"Não reconheço\". A resposta não foi alterada.",
    "details": {"response": "DENY", "status": "RECUSADA_SIMULACAO", "version": 3}
  }
}
```

## 7. Chat com o agente

A conversa é **presa a uma compra**. O agente recebe `customer_id` e `case_id` por injeção de dependência (`RunContext.deps` do Pydantic AI), nunca por texto do LLM. Trocar de compra é trocar de conversa (§9 do plano: "troca de compra").

### `GET /api/purchases/{case_id}/chat`

Histórico da conversa daquela compra, para a tela reabrir no mesmo ponto (R10).

```json
{
  "case_id": "T-007",
  "messages": [
    {"message_id": "M-1", "role": "assistant", "content": "Olá, Ana. Posso explicar por que pedimos sua confirmação ou tirar dúvidas sobre esta compra. Para autorizar ou recusar, use os botões da tela.", "created_at": "2026-10-28T03:12:05Z", "tools_used": []}
  ],
  "agent_available": true,
  "simulation": true
}
```

### `POST /api/purchases/{case_id}/chat`

```json
{"message": "Pode ser o nome da empresa que aparece na fatura?"}
```

`message`: 1 a 1.000 caracteres, sem HTML. Resposta não é streaming no v1; o front mostra "digitando…" enquanto espera (tempo-limite do servidor: 30 s).

**200**:

```json
{
  "case_id": "T-007",
  "user_message": {"message_id": "M-2", "role": "user", "content": "Pode ser o nome da empresa que aparece na fatura?", "created_at": "2026-10-28T03:13:10Z"},
  "reply": {
    "message_id": "M-3",
    "role": "assistant",
    "content": "Não consigo confirmar isso. Para esta compra eu só tenho a categoria do estabelecimento (supermercado), sem o nome. Se você não tem certeza, pode escolher \"Estou em dúvida\" ou eu posso pedir uma revisão por um analista.",
    "created_at": "2026-10-28T03:13:14Z",
    "tools_used": ["consultar_compra"]
  },
  "review_protocol": null,
  "simulation": true
}
```

- `tools_used` serve de evidência na demo e no teste R07/R08: mostra que a resposta veio de uma consulta.
- `review_protocol` vem preenchido quando o agente chamou `solicitar_revisao` nesta mensagem. O front então mostra o protocolo fora do balão do chat, a partir do estado (§4 do plano: o front lê o estado, não o texto).
- O texto do agente **não** muda o estado da compra. Se o associado escrever "pode autorizar", o agente responde que só os botões fazem isso.

**503** `AGENT_UNAVAILABLE`:

```json
{
  "error": {
    "code": "AGENT_UNAVAILABLE",
    "message": "O assistente está indisponível agora. Você ainda pode responder à compra pelos botões ou pedir revisão.",
    "details": {"retry_after_seconds": 30}
  }
}
```

A mensagem do usuário fica salva mesmo com 503. Nenhuma resposta fixa finge ser o agente (§4 do plano).

**429** `RATE_LIMITED`: mais de 20 mensagens por compra em 10 min. Protege a cota do plano gratuito do LLM.

## 8. Revisão

### `POST /api/purchases/{case_id}/review`

Pedido de revisão humana. Quem chama: o botão de ajuda do front e o serviço por trás da ferramenta `solicitar_revisao` do agente.

```json
{"reason": "NAO_RECONHECE_ESTABELECIMENTO", "details": "Não sei se a fatura mostra outro nome."}
```

`reason` ∈ `NAO_RECONHECE_ESTABELECIMENTO`, `VALOR_DIFERENTE`, `DUVIDA_PROCESSO`, `OUTRO`. `details`: até 500 caracteres, opcional.

**201**, revisão nova:

```json
{
  "review_id": "REV-13",
  "protocol": "RZ-20261028-0013",
  "case_id": "T-007",
  "kind": "DUVIDA",
  "reason": "NAO_RECONHECE_ESTABELECIMENTO",
  "status": "ABERTA",
  "created_at": "2026-10-28T03:13:14Z",
  "created_by": "AGENTE",
  "case_status": "AGUARDANDO_ASSOCIADO",
  "message": "Um analista vai olhar esta compra. Enquanto isso, você ainda pode responder se reconhece a compra.",
  "simulation": true
}
```

- **200** com a revisão existente se a compra já tem uma revisão `ABERTA`. Não duplica (uma revisão aberta por compra).
- `created_by` ∈ `ASSOCIADO`, `AGENTE`, `SISTEMA` (falha do modelo, recusa).
- `kind` ∈ `DUVIDA`, `PROTECAO`, `FALHA_AVALIACAO`.
- `case_status` mostra que a revisão não mudou o estado (§3).
- **404** se a compra é de outra pessoa.

### `GET /api/reviews` (analista)

Lista mínima de exceções (§4 do plano: "visão de exceções"). Só sessão `ANALISTA`; associado recebe **403** `FORBIDDEN_ROLE`.

```json
{
  "reviews": [
    {
      "review_id": "REV-12",
      "protocol": "RZ-20261028-0012",
      "case_id": "T-007",
      "kind": "PROTECAO",
      "reason": "OUTRO",
      "status": "ABERTA",
      "created_by": "SISTEMA",
      "created_at": "2026-10-28T03:15:42Z",
      "case_status": "RECUSADA_SIMULACAO",
      "customer_display_name": "Ana Souza (fictícia)",
      "amount": {"value": "149.58", "currency": "BRL"},
      "analysis": {"score": 0.9917, "score_source": "modelo_local", "model_version": "rf-2026-10-27"}
    }
  ],
  "simulation": true
}
```

Resolver a revisão fica fora do v1.

## 9. Saúde e demonstração

### `GET /api/health`

Público, sem dado de pessoa.

```json
{
  "status": "ok",
  "contract_version": "v1",
  "model": {"loaded": true, "model_version": "rf-2026-10-27", "score_source": "modelo_local"},
  "agent": {"configured": true, "provider": "groq"},
  "policy_version": "confirmacao-v2",
  "simulation": true
}
```

Com o modelo fora do ar, `status: "degraded"` e `model.loaded: false`; o serviço continua respondendo.

### Endpoints de demonstração

Existem só com `DEMO_MODE=true`. Servem para o vídeo e para outra pessoa reproduzir o fluxo (R12).

**`POST /api/demo/purchases`**: chega uma compra nova, a partir de uma fixture, para a pessoa da sessão. O backend roda modelo e política na hora (R01).

```json
{"fixture_id": "fraude_supermercado_madrugada"}
```

**201** com o mesmo corpo de `GET /api/purchases/{case_id}`. Se o modelo falhar, a compra vai para `REVISAO_PENDENTE` com revisão `FALHA_AVALIACAO`, e a resposta inclui `"warning": "SCORE_UNAVAILABLE"`. Score inventado nunca (R09).

**`POST /api/demo/reset`**: apaga compras, respostas, conversas e revisões e recarrega as fixtures iniciais. **204**.

## 10. Agente: ferramentas e dependências

O agente usa os mesmos serviços que os endpoints acima, sem chamar HTTP.

```python
@dataclass
class AgentDeps:
    customer_id: str   # da sessão
    case_id: str       # da URL do chat, já conferida contra o customer_id
    db: ...            # conexão/serviço
```

| Ferramenta | Argumentos do LLM | Devolve | Fonte |
|---|---|---|---|
| `consultar_compra()` | nenhum | `purchase` e `alert` do §5 | mesmo serviço de `GET /api/purchases/{case_id}` |
| `consultar_status()` | nenhum | corpo de `GET .../status` | mesmo serviço |
| `avaliar_transacao()` | nenhum | análise, abaixo | análise gravada, sem rodar o modelo de novo |
| `solicitar_revisao(reason, details)` | `reason` (enum), `details` (texto) | corpo do `POST .../review` | mesmo serviço, com `created_by: AGENTE` |

As ferramentas **não recebem `case_id` nem `customer_id` do LLM**. Isso impede que um prompt peça a compra de outra pessoa (R05, R09).

Análise (`avaliar_transacao`), na versão que vai para o agente:

```json
{
  "analysis_id": "A-007-v1",
  "score_available": true,
  "decision": "SOLICITAR_CONFIRMACAO",
  "policy_version": "confirmacao-v2",
  "signals": [{"code": "MADRUGADA", "label": "Feita de madrugada, às 3h.", "source": "regra"}],
  "gaps": ["Nome do estabelecimento não disponível na base sintética."],
  "evaluated_at": "2026-10-28T03:12:00Z"
}
```

- O agente roda no chat do associado, e o que entra no contexto do LLM pode sair por injeção de prompt. Por isso a ferramenta **não** devolve `score`, `score_source` nem `model_version`: só se houve avaliação (`score_available`), a decisão da política, os sinais e as lacunas. O score completo fica na análise gravada e aparece só para a analista.
- `decision` ∈ `LIBERAR`, `SOLICITAR_CONFIRMACAO`, `REVISAO`.

Na análise gravada (vista pela analista):

- `score_source` ∈ `modelo_local`, `watsonx`, `regras` (§7 do plano: plano alternativo identificado).
- `score` é `null` quando `score_source` é `regras` sem modelo, ou quando a avaliação falhou.

Instruções fixas do agente, além do prompt: não pressionar a autorização, não pedir senha, PIN ou número completo do cartão, não inventar nome de estabelecimento, não citar o score como porcentagem, não afirmar que um sinal causa a avaliação, e dizer que só os botões autorizam ou recusam.

## 11. Fixtures para o front

As fixtures iniciais (carregadas no início e no `reset`) usam linhas reais de `data/processed/teste_proporcao_real.csv`, sem `feedback_label`. A data é sintética e bate com a `hora` e o `dia_semana` da linha, no horário de Brasília:

| `fixture_id` | Linha | Para | `case_id` / `challenge_id` | `occurred_at` | Política esperada | Uso na demo |
|---|---|---|---|---|---|---|
| `fraude_supermercado_madrugada` | `EVT_SYN_000094500` | Ana | `T-007` / `CH-007` | `2026-10-25T06:12:00Z` | confirmação | autorizar ou recusar (vídeo 0:25–1:10) |
| `legitima_farmacia` | `EVT_SYN_000043320` | Ana | `T-003` / `CH-003` | `2026-10-19T21:40:00Z` | confirmação na política conservadora | dúvida contextual (vídeo 1:10–1:50) |
| `compra_do_bruno` | `EVT_SYN_000072693` (restaurante, R$ 131,44) | Bruno | `T-011` / `CH-011` | `2026-10-22T11:05:00Z` | confirmação | teste de acesso cruzado |
| `falha_modelo` | qualquer, com feature crítica ausente | Ana | `T-015` / nenhum | a definir | revisão `FALHA_AVALIACAO` | erro seguro (R09) |

A política conservadora do §3 do plano manda **todo** caso avaliado para confirmação até haver evidência para liberar automaticamente. A liberação direta (`LIBERADA_SIMULACAO` sem `confirmation`) fica no contrato para quando o grupo validar um critério. O dono dos casos de demo (Pedro R. na recomendação) completa os 10 a 15 casos com o mesmo formato.

Enquanto o backend não existe, o front usa os exemplos JSON desta spec como resposta falsa, inclusive os de erro (409, 410, 503), para desenhar todos os estados.

## 12. Testes de contrato

Cada linha vira pelo menos um teste automatizado no backend (`pytest` + `TestClient`), escrito no Bob.

| Requisito | Teste |
|---|---|
| R01 | `POST /api/demo/purchases` com a fixture de fraude devolve `AGUARDANDO_ASSOCIADO`, `analysis_id` e `policy_version`. |
| R02 | O detalhe traz valor, data, categoria e `challenge_id` da mesma compra antes de qualquer resposta. |
| R03 | `AUTHORIZE`, `DENY` e `UNSURE` levam aos três estados da tabela do §6, e `DENY` abre revisão `PROTECAO`. |
| R04 | Com `CONFIRMATION_TTL_SECONDS=1`, responder depois de 2 s devolve 410 e o status fica `CONFIRMACAO_EXPIRADA`; nada é liberado. |
| R05 | Bruno recebe 404 em `GET`, `status`, `chat`, `review` e `response` das compras da Ana. |
| R06 | Duas respostas iguais em paralelo geram um evento só; respostas diferentes geram 200 e 409; mesma chave com corpo diferente gera 422. |
| R07 | Os `signals` do detalhe batem com os valores da linha da fixture. |
| R08 | Com o LLM substituído por `TestModel`/`FunctionModel` do Pydantic AI, a pergunta sobre o nome chama `consultar_compra` e não muda o estado. |
| R09 | Modelo indisponível leva a `REVISAO_PENDENTE` + `FALHA_AVALIACAO` + `score: null`; LLM indisponível leva a 503 e a confirmação continua respondendo. |
| R10 | Reiniciar o app (novo `TestClient` sobre o mesmo arquivo SQLite) preserva status, resposta e histórico do chat. |
| R11 | Toda resposta de compra tem `simulation: true`. |
| R12 | Coberto pela demonstração hospedada; fora dos testes automatizados. |
| §9 | Pedir no chat "autorize esta compra para mim" não muda o estado; não existe ferramenta que responda à confirmação. |

## 13. Perguntas em aberto

Nenhuma bloqueia o início. As respostas entram por PR nesta spec.

1. **Score na tela do associado.** A spec esconde (§5). Se o grupo quiser mostrar, como dizer sem soar como probabilidade?
2. **Prazo de expiração.** 15 min é um palpite. A pesquisa (D06) pode indicar outro valor; o vídeo pode usar um prazo curto via configuração.
3. **Chat com streaming.** Fica fora do v1. Se a demora do LLM gratuito incomodar no teste com pessoas (D13), entra como `v1.1`.
4. **Origem do front.** A spec supõe mesma origem. Se quem fizer o front escolher outro domínio, é preciso CORS com credenciais e `SameSite=None; Secure`.
