# D10 ÔÇö Arquitetura t├®cnica e limites de autonomia

**ID:** D10 ┬À **Vers├úo:** 0.1 ┬À **Data:** 29/10/2026
**Respons├ível:** Pessoa 3 ┬À **Revisor:** Pessoa 4
**Estado:** rascunho
**Depende de:** D09 (estrutura e requisitos); **Alimenta:** D11, D13

---

## 1. Vis├úo geral

```mermaid
flowchart TD
    C[Compra sint├®tica] --> M[Modelo RF no backend\noutputs/modelo_rf.joblib]
    M --> P[Pol├¡tica determin├¡stica\n+ m├íquina de estados]
    P -->|score baixo / crit├®rio de libera├º├úo| L[LIBERADA_SIMULACAO]
    P -->|crit├®rio de confirma├º├úo| I[Interface do associado\nReact + Carbon]
    P -->|falha / fora da pol├¡tica| R[REVISAO_PENDENTE]
    I -->|d├║vida contextual| A[Agente Pydantic AI\nno backend]
    A --> T1[avaliar_transacao\nscore, sinais, vers├úo]
    A --> T2[consultar_compra\ncontexto da sess├úo]
    A --> T3[consultar_status\nestado e pr├│ximos passos]
    A --> T4[solicitar_revisao\nprotocolo de exce├º├úo]
    T1 & T2 & T3 & T4 --> A
    A -->|explica├º├úo + limite ou revis├úo| I
    I -->|resposta humana expl├¡cita\nPOST /confirmations/{id}/response| B[Backend FastAPI\nvalida sess├úo, vers├úo, expira├º├úo]
    B --> H[SQLite ÔÇö estado e eventos\npersist├¬ncia dur├ível]
    L --> H
    R --> H
    I -->|pedido de atendimento\nn├úo ├® UNSURE| R
```

> Este diagrama representa a arquitetura planejada. Os componentes com estado **planejado** ainda n├úo foram implementados ou integrados.

---

## 2. Componentes e pap├®is

| Componente | Tecnologia | Papel | Estado |
|---|---|---|---|
| **Modelo RF** | scikit-learn 1.6 ┬À Python 3.12 | Produz score (0ÔÇô1) para a classe fraude, sem garantia de calibra├º├úo como probabilidade real; carregado em `outputs/modelo_rf.joblib` no processo do backend | A serializar do notebook 03 |
| **Pol├¡tica de decis├úo** | Python (determin├¡stico) | Transforma score em tratamento (`LIBERADA_SIMULACAO`, `AGUARDANDO_ASSOCIADO`, `REVISAO_PENDENTE`); limiares versionados e configur├íveis | Planejada |
| **Backend** | FastAPI ┬À SQLAlchemy ┬À SQLite | Valida sess├úo, vincula associado/compra, controla expira├º├úo, persiste estados/eventos, exp├Áe API JSON; roda no mesmo processo do modelo | Planejado |
| **Agente** | Pydantic AI ┬À LLM externo (Groq/Gemini/Granite) | Consulta ferramentas, explica sinais, informa limites, solicita revis├úo quando necess├írio; n├úo autoriza compras | Planejado |
| **Interface do associado** | React + Carbon (`watson/frontend`) | Mostra compra, alerta, pergunta, tr├¬s respostas e campo de d├║vida; l├¬ API JSON; console de exce├º├Áes limitado | Em adapta├º├úo (Leonardo, PR #7); cards C10/C13 |
| **Bob IDE** | IBM Bob | Desenvolvimento, revis├úo, testes e documenta├º├úo; sess├Áes exportadas em `bob_sessions/` | Em uso; obrigat├│rio |
| **watsonx.ai** | IBM Cloud (evid├¬ncia) | Deploy do modelo como prova de execu├º├úo em nuvem; `score_source=watsonx` dispon├¡vel; fora do runtime da demo | Testado em 27/10 |

---

## 3. Sequ├¬ncia de execu├º├úo ÔÇö fluxo principal

```mermaid
sequenceDiagram
    actor A as Associado
    participant F as Frontend
    participant B as Backend
    participant M as Modelo RF
    participant Pol as Pol├¡tica
    participant DB as SQLite
    participant Ag as Agente

    Note over B,DB: Pr├®-condi├º├úo: compra sint├®tica criada (T-007)

    B->>M: avaliar(features de T-007)
    M-->>B: {score: 0.97, vers├úo: "rf-v1"}
    Note over B: Sinais descritivos s├úo obtidos separadamente
    B->>Pol: decidir(score=0.97, policy_version="confirmacao-v2")
    Pol-->>B: AGUARDANDO_ASSOCIADO
    B->>DB: INSERT challenge CH-007 (status=AGUARDANDO_ASSOCIADO, expires_at=+15min)
    B-->>F: challenge CH-007 com compra e sinais dispon├¡veis

    A->>F: "Pode ser o nome da empresa na fatura?"
    F->>B: POST /chat {challenge_id: "CH-007", msg: "..."}
    B->>Ag: consultar(challenge_id="CH-007", msg)
    Ag->>B: consultar_compra("T-007")
    B-->>Ag: {estabelecimento: "BANDEIRA_A / MCC 5411", acceptor_risk: 70}
    Ag->>B: avaliar_transacao("T-007")
    B-->>Ag: {score: 0.97, sinais: ["madrugada", "cnp_credito", "primeira_compra_cartao"]}
    Ag-->>B: "N├úo consigo confirmar o nome fantasia. Os sinais dispon├¡veis s├úo: ..."
    B-->>F: resposta do agente

    A->>F: clica em "N├úo reconhe├ºo"
    F->>B: POST /confirmations/CH-007/response {response: "DENY", version: 1, idempotency_key: "xyz"}
    B->>DB: INSERT response; UPDATE challenge status=RECUSADA_SIMULACAO
    B->>DB: INSERT case REVISAO_PENDENTE
    B-->>F: {status: "RECUSADA_SIMULACAO", next_step: "Um analista vai avaliar o caso."}
```

---

## 4. Ficha do agente

| Campo | Descri├º├úo |
|---|---|
| **Objetivo** | Ajudar o associado a entender a compra sinalizada e tomar uma decis├úo informada ÔÇö autorizar, recusar ou encaminhar para revis├úo. |
| **Conhecimento permitido** | Dados retornados pelas ferramentas autorizadas: score, sinais, contexto da compra, status da confirma├º├úo. Nenhum dado al├®m do que as ferramentas retornam. |
| **Instru├º├Áes principais** | (1) Usar apenas informa├º├Áes das ferramentas; (2) n├úo inventar nomes de estabelecimentos, pol├¡ticas da institui├º├úo ou resultados de bloqueio; (3) declarar explicitamente quando n├úo houver contexto suficiente; (4) n├úo pressionar o associado a autorizar; (5) n├úo pedir senha, PIN ou dados completos do cart├úo; (6) nunca chamar `responder_confirmacao` ÔÇö quem autoriza ├® o associado pelo controle da interface. |
| **Ferramentas dispon├¡veis** | `avaliar_transacao`, `consultar_compra`, `consultar_status`, `solicitar_revisao` (ver cat├ílogo abaixo). |
| **Crit├®rio de escolha de ferramenta** | Perguntas sobre o motivo do alerta ÔåÆ `avaliar_transacao`; perguntas sobre o estabelecimento ou valor ÔåÆ `consultar_compra`; perguntas sobre o andamento ÔåÆ `consultar_status`; d├║vida irresolv├¡vel ou pedido de atendimento ÔåÆ `solicitar_revisao`. |
| **Limites de autonomia** | N├úo pode alterar o estado da confirma├º├úo. N├úo pode presumir identidade do estabelecimento. Se o LLM falhar, o backend retorna erro e o caminho expl├¡cito de confirma├º├úo continua funcionando. |

---

## 5. Cat├ílogo de ferramentas

### `avaliar_transacao(case_id: str)`

| Campo | Detalhe |
|---|---|
| **Finalidade** | Retornar score de fraude, sinais descritivos dispon├¡veis e vers├úo do modelo. Os sinais n├úo comprovam contribui├º├úo para o score; uma explica├º├úo por caracter├¡stica exige m├®todo e valida├º├úo espec├¡ficos. |
| **Entrada** | `case_id` ÔÇö identificador da compra na sess├úo atual. |
| **Sa├¡da** | `{score: float, sinais: list[str], lacunas: list[str], score_source: str, model_version: str}` |
| **Autoriza├º├úo** | Acess├¡vel ao agente; dados dispon├¡veis ao associado da sess├úo. R├│tulo hist├│rico de avalia├º├úo n├úo exposto. |
| **Erros** | `{"ok": false, "etapa": "modelo", "erro": "..."}` ÔÇö nunca retorna score inventado. |

### `consultar_compra(case_id: str)`

| Campo | Detalhe |
|---|---|
| **Finalidade** | Retornar o contexto permitido da compra: estabelecimento (identifica├º├úo dispon├¡vel), valor, data, cart├úo parcial, MCC e regi├úo. |
| **Entrada** | `case_id` ÔÇö validado contra a sess├úo do associado autenticado. |
| **Sa├¡da** | `{estabelecimento: str\|null, valor: float, data: str, cartao_parcial: str, mcc: str, acceptor_region: str\|null, acceptor_risk: float\|null}` |
| **Autoriza├º├úo** | S├│ retorna dados da compra vinculada ├á sess├úo ativa. Nunca retorna dados de outro associado. |
| **Erros** | `{"ok": false, "etapa": "consulta", "erro": "..."}` |

### `consultar_status(case_id: str)`

| Campo | Detalhe |
|---|---|
| **Finalidade** | Retornar o estado atual da confirma├º├úo e os pr├│ximos passos permitidos. |
| **Entrada** | `case_id` |
| **Sa├¡da** | `{status: str, allowed_responses: list[str]\|null, expires_at: str\|null, next_step: str}` |
| **Autoriza├º├úo** | Acess├¡vel ao agente e ao frontend. |
| **Erros** | `{"ok": false, "etapa": "status", "erro": "..."}` |

### `solicitar_revisao(case_id: str, reason: str)`

| Campo | Detalhe |
|---|---|
| **Finalidade** | Criar um caso de exce├º├úo para revis├úo humana e retornar o protocolo. |
| **Entrada** | `case_id`, `reason` ÔÇö motivo declarado pelo agente (ex: "contexto de estabelecimento insuficiente"). |
| **Sa├¡da** | `{protocolo: str, status: "REVISAO_PENDENTE", next_step: str}` |
| **Autoriza├º├úo** | O agente pode solicitar revis├úo; n├úo pode encerrar a confirma├º├úo nem autorizar. |
| **Erros** | `{"ok": false, "etapa": "revisao", "erro": "..."}` |

---

## 6. Contratos da API (exemplos)

### `GET /confirmations/{challenge_id}`

```json
{
  "challenge_id": "CH-007",
  "case_id": "T-007",
  "analysis_id": "A-007-v1",
  "version": 1,
  "status": "AGUARDANDO_ASSOCIADO",
  "allowed_responses": ["AUTHORIZE", "DENY", "UNSURE"],
  "expires_at": "2026-10-29T15:02:00Z",
  "policy_version": "confirmacao-v2",
  "simulation": true,
  "compra": {
    "estabelecimento": "BANDEIRA_A / MCC 5411",
    "valor": 149.58,
    "data": "2025-02-14T03:12:00Z",
    "cartao_parcial": "**** **** **** 1234"
  },
  "motivo_alerta": "A compra foi sinalizada. Dados dispon├¡veis: madrugada, cart├úo n├úo presente, primeiro uso do cart├úo e estabelecimento de risco elevado."
}
```

### `POST /confirmations/{challenge_id}/response`

**Request:**
```json
{
  "response": "DENY",
  "version": 1,
  "idempotency_key": "cli-xyz-001"
}
```

**Response 200:**
```json
{
  "challenge_id": "CH-007",
  "status": "RECUSADA_SIMULACAO",
  "next_step": "Um analista vai avaliar o caso. Protocolo: REV-0042.",
  "simulation": true
}
```

**Response 409 (resposta conflitante):**
```json
{
  "error": "conflict",
  "detail": "Confirma├º├úo j├í registrada com resposta diferente.",
  "current_status": "RECUSADA_SIMULACAO"
}
```

### `POST /chat`

**Request:**
```json
{
  "challenge_id": "CH-007",
  "message": "Esse estabelecimento ├® confi├ível?"
}
```

**Response 200:**
```json
{
  "reply": "N├úo consigo confirmar o nome fantasia do estabelecimento ÔÇö s├│ tenho o c├│digo MCC 5411 e a regi├úo registrada. Os sinais dispon├¡veis s├úo: compra na madrugada, sem cart├úo presente e primeiro uso do cart├úo. Se precisar de mais informa├º├Áes, posso encaminhar para revis├úo.",
  "tools_called": ["consultar_compra", "avaliar_transacao"]
}
```

---

## 7. Pol├¡tica e m├íquina de estados

### Pol├¡tica de decis├úo inicial

| Condi├º├úo | Tratamento | Status |
|---|---|---|
| Entrada v├ílida + avalia├º├úo dispon├¡vel + crit├®rio de libera├º├úo atendido | Liberar automaticamente na simula├º├úo | `LIBERADA_SIMULACAO` |
| Crit├®rio de confirma├º├úo atendido | Criar solicita├º├úo individual | `AGUARDANDO_ASSOCIADO` |
| Dados cr├¡ticos ausentes / servi├ºo falha / caso fora da pol├¡tica | Encaminhar para revis├úo; n├úo inventar score | `REVISAO_PENDENTE` |

> **Nota:** limiares num├®ricos ser├úo definidos na etapa de valida├º├úo (C16), n├úo neste documento. A pol├¡tica inicial conservadora envia todos os casos avaliados para confirma├º├úo.

### M├íquina de estados

```mermaid
stateDiagram-v2
    [*] --> RECEBIDA
    RECEBIDA --> EM_AVALIACAO
    EM_AVALIACAO --> LIBERADA_SIMULACAO : crit├®rio de libera├º├úo
    EM_AVALIACAO --> AGUARDANDO_ASSOCIADO : crit├®rio de confirma├º├úo
    EM_AVALIACAO --> REVISAO_PENDENTE : falha ou fora da pol├¡tica
    AGUARDANDO_ASSOCIADO --> LIBERADA_SIMULACAO : AUTHORIZE (antes da expira├º├úo)
    AGUARDANDO_ASSOCIADO --> RECUSADA_SIMULACAO : DENY
    AGUARDANDO_ASSOCIADO --> REVISAO_PENDENTE : UNSURE
    AGUARDANDO_ASSOCIADO --> CONFIRMACAO_EXPIRADA : prazo esgotado sem resposta
    LIBERADA_SIMULACAO --> [*]
    RECUSADA_SIMULACAO --> [*]
    REVISAO_PENDENTE --> [*]
    CONFIRMACAO_EXPIRADA --> [*]
```

**Regras de transi├º├úo:**
- Pedir atendimento (`talk_to_person`) ÔåÆ abre revis├úo sem registrar `UNSURE` nem encerrar a confirma├º├úo v├ílida.
- `solicitar_revisao` cria ou reaproveita uma revis├úo separada da confirma├º├úo; enquanto ela estiver v├ílida, a confirma├º├úo permanece em `AGUARDANDO_ASSOCIADO` e o prazo continua correndo.
- Resposta duplicada ÔåÆ retorna o resultado existente sem duplicar a├º├úo.
- Resposta a vers├úo antiga ou outra compra ÔåÆ rejeitar; orientar o associado a abrir a solicita├º├úo correta.
- O agente nunca provoca transi├º├úo de estado ÔÇö apenas `solicitar_revisao` cria um caso de exce├º├úo.

---

## 8. Persist├¬ncia e falhas

### O que ├® persistido (mesma transa├º├úo)

| Entidade | Campos m├¡nimos |
|---|---|
| `purchase` | `case_id`, `challenge_id`, `associate_id`, `amount`, `mcc`, `acceptor_risk`, `created_at` |
| `analysis` | `analysis_id`, `case_id`, `score`, `score_source`, `model_version`, `policy_version`, `created_at` |
| `challenge` | `challenge_id`, `case_id`, `status`, `version`, `expires_at`, `policy_version`, `simulation` |
| `response` | `response_id`, `challenge_id`, `associate_id`, `response`, `idempotency_key`, `created_at` |
| `event` | `event_id`, `challenge_id`, `type`, `payload`, `created_at` |

### Tratamento de falhas

| Falha | Comportamento esperado |
|---|---|
| Modelo indispon├¡vel | Retornar `REVISAO_PENDENTE`; log com `score_source=indisponivel`; nunca inventar score |
| LLM indispon├¡vel | Chat retorna erro expl├¡cito; caminho de confirma├º├úo (tr├¬s bot├Áes) continua funcionando |
| Resposta duplicada | Retornar resultado existente; n├úo duplicar estado |
| Sess├úo expirada | Rejeitar; orientar o associado |
| Banco de dados indispon├¡vel | Retornar 503; nenhuma transa├º├úo parcial |
| Rein├¡cio da aplica├º├úo | Estado preservado no SQLite com volume dur├ível; em hospedagem ef├¬mera, usar armazenamento persistente |

---

## 9. Uso de tecnologia IBM

| Tecnologia | Papel neste projeto | Estado |
|---|---|---|
| **IBM Bob** | Desenvolvimento, revis├úo, testes e documenta├º├úo; sess├Áes exportadas por integrante em `bob_sessions/` | Em uso; obrigat├│rio pelo guia |
| **watsonx.ai** | Deploy do modelo RF como evid├¬ncia de execu├º├úo em nuvem IBM; `score_source=watsonx` dispon├¡vel como op├º├úo | Testado em 27/10 (spec: `docs/specs/teste_integracao_orchestrate_wml.md`); fora do runtime da demo |

---

## 10. Decis├Áes t├®cnicas registradas

| # | Tema | Decis├úo | Motivo |
|---|---|---|---|
| DEC-01 | Runtime do modelo | Backend local via `joblib`; watsonx.ai como evid├¬ncia, n├úo runtime | Elimina depend├¬ncia de chave IBM Cloud e cota Lite em tempo de execu├º├úo |
| DEC-02 | Backend | FastAPI + SQLAlchemy + SQLite | Mesmo processo do modelo; SQLite atende R06 e R10; `DATABASE_URL` configur├ível para PostgreSQL |
| DEC-03 | Agente | Pydantic AI com LLM externo (Groq/Gemini/Granite) | Troca de provedor ├® configura├º├úo; Granite no watsonx.ai como op├º├úo se houver chave |
| DEC-04 | Autoriza├º├úo | `responder_confirmacao` ├® endpoint do backend acess├¡vel ├á sess├úo humana; o agente n├úo possui essa ferramenta | Mant├®m isolamento: s├│ o controle da interface registra a resposta do associado |
| DEC-05 | Frontend | React + Carbon existente do Watson (PR #7), adaptado por Leonardo | Evita reescrever do zero; backend exp├Áe s├│ API JSON e n├úo depende da escolha de frontend |
| DEC-06 | Identidade | Login fict├¡cio com 2ÔÇô3 associados identificados como fict├¡cios e cookie de sess├úo assinado | Atende R05 sem fingir autentica├º├úo banc├íria produtiva |

---

## 11. Evid├¬ncias de execu├º├úo (a preencher)

| Item | Descri├º├úo | Respons├ível | Estado |
|---|---|---|---|
| Deploy watsonx.ai | Resultado do teste 7.1 da spec | P3 | Conclu├¡do em 27/10 |
| Modelo local | Scores id├¬nticos ao notebook para casos fixos de `pontuar_transacao.py` | P3 | Planejado (C06) |
| Pol├¡tica + estados | Todos os cen├írios do ┬º9 do plano documentados e executados | P3 | Planejado (C12) |
| Isolamento de sess├úo | Dois associados fict├¡cios; acesso cruzado negado | P3 | Planejado (C26) |
| Expira├º├úo | Confirma├º├úo expirada n├úo libera; `CONFIRMACAO_EXPIRADA` persistido | P3 | Planejado (C17) |

---

## 12. Limita├º├Áes e pr├│ximos passos

- [ ] Publicar vers├úo revisada ap├│s C06 (viabilidade de acesso e interface) estar conclu├¡do.
- [ ] Definir e documentar os limiares da pol├¡tica ap├│s valida├º├úo (C16).
- [ ] Ampliar casos de demonstra├º├úo para cobrir todos os cen├írios do ┬º9 do plano.
- [ ] Confirmar provedor LLM e documentar substitui├º├úo como configura├º├úo.
- [ ] Ap├│s integra├º├úo (C13), adicionar diagrama de sequ├¬ncia para os casos de d├║vida e expira├º├úo.
- [ ] Registrar resultado real de cada evid├¬ncia da se├º├úo 11 ao executar os cards correspondentes.
