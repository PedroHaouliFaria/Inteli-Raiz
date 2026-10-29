# D12 — Protótipo da Experiência e Decisões de Interface

**ID:** D12 · **Versão:** 0.2 · **Data:** 28/10/2026 (corrigido após revisão do Codex)
**Responsável:** Pessoa 4 (consolida); Leonardo (execução técnica C10/C13); Pessoa 2 (revisão)  
**Estado:** **revisado documentalmente** — percurso especificado; interface `212655c` inspecionada; tela atual diverge do plano em pontos críticos; adaptações necessárias identificadas.  
**Fontes:** plano vigente `8942cc5` §§1–5; D06 `8a7aefc`; `MemberPhone.jsx` `212655c`; `store.jsx` `212655c`; D09/D10 `f732159`.

---

## 1. Percurso principal da confirmação

O associado percorre as etapas abaixo em sequência linear, sem desvios desnecessários. Cada tela tem um único objetivo.

```
[Carregando] → [Compra + Alerta + Pergunta] → [Respondendo] → [Resultado]
                         ↓ (dúvida contextual)
                   [Chat com agente]
                         ↓ (pedido de atendimento)
                   [Revisão aberta — confirmação continua válida]
```

**Entradas no percurso:**
- Alerta no app autenticado → associado abre a notificação.
- Link direto de demonstração (sessão fictícia identificada como tal).

**Saídas possíveis:**
- `LIBERADA_SIMULACAO` (após `AUTHORIZE` válido)
- `RECUSADA_SIMULACAO` (após `DENY` válido)
- `REVISAO_PENDENTE` (exclusivamente após `UNSURE`)
- `CONFIRMACAO_EXPIRADA` (sem resposta antes do prazo, inclusive quando revisão já foi solicitada por pedido de atendimento)

---

## 2. Mapa de telas e estados

| Tela / estado | Objetivo do associado | Dados exibidos | Ações disponíveis | Resultado / transição | Requisito | Implementação observada (212655c) | Adaptação necessária |
|---|---|---|---|---|---|---|---|
| **Carregando** | Aguardar a compra aparecer | Indicador de carregamento | Nenhuma | → Compra + Alerta | R02, R09 | Não existe como tela separada | Adicionar estado de carregamento antes de exibir compra |
| **Compra + Alerta + Pergunta** (`AGUARDANDO_ASSOCIADO`) | Entender a compra e decidir | Estabelecimento (disponível ou limite), valor, data, cartão parcial, motivo do alerta, sinais disponíveis, prazo | Três botões + "Quero falar com alguém" + campo de chat | → uma das três respostas | R02, R03, R07, R11 | Tela `notice`: dois botões (`Sim, fui eu` / `Não reconheço`) + link "Por que recebi este aviso?" | Três botões; remover biometria; link com ação real |
| **Chat com agente** | Esclarecer dúvida sobre a compra | Resposta contextualizada com base nas ferramentas | Enviar mensagem; fechar chat; usar os três botões | → continua na tela principal | R07, R08, R09 | Não existe | Implementar `POST /api/purchases/{case_id}/chat` + componente no frontend |
| **Revisão solicitada** (após `POST /api/purchases/{case_id}/review`, sem responder) | Ver protocolo e entender que **pode ainda responder** | Protocolo da revisão, status da confirmação (`AGUARDANDO_ASSOCIADO`), prazo restante | Voltar (confirmação **continua em `AGUARDANDO_ASSOCIADO`** enquanto válida; pedido de revisão não muda o status da compra) | → continua em `AGUARDANDO_ASSOCIADO` se ainda válido | R03, R08 | Link "Prefiro falar com uma pessoa" sem ação | Implementar ação: chamar `POST /api/purchases/{case_id}/review`; mostrar protocolo retornado; status da compra não muda |
| **Respondendo** (processando) | Aguardar confirmação do servidor | Indicador de envio | Nenhuma | → Resultado | R06, R09 | Não existe | Adicionar estado de envio/feedback |
| **Resultado — Liberada** (`LIBERADA_SIMULACAO`) | Entender que a compra foi autorizada | "Compra liberada (simulação) — esta é uma demo; nenhuma transação real foi feita." Status da compra, não do cartão. | Fechar / ver histórico | — | R03, R10, R11 | Tela `released`: "Obrigado, Valdir. Seu cartão continua funcionando." | Texto: focar na compra, não no cartão; identificar simulação |
| **Resultado — Recusada** (`RECUSADA_SIMULACAO`) | Entender que a compra foi recusada e que existe um próximo passo | "A compra foi recusada na simulação. **Seu cartão não foi bloqueado**. Um caso de revisão foi aberto." | Fechar / ver histórico | — | R03, R10, R11 | Tela `protected`: **"Bloqueamos o cartão final 4821 e nada foi cobrado. Um cartão novo chega em até 7 dias úteis."** | Corrigir mensagem: remover bloqueio de cartão e promessa de novo cartão. **Nota:** `DENY` → compra fica em `RECUSADA_SIMULACAO`; revisão de proteção abre em paralelo; a compra **não** transita para `REVISAO_PENDENTE`. |
| **Resultado — Revisão pendente** (`REVISAO_PENDENTE`) | Entender que a dúvida foi registrada (resposta `UNSURE`) | Status, protocolo (se houver), próximo passo | Fechar / ver histórico | — | R03, R10 | Tela `reviewing`: "uma analista vai conferir a compra. Ela segue pausada e nada foi cobrado." | Texto adequado; remover "nada foi cobrado" (promessa operacional). **Nota:** `UNSURE` → compra transita para `REVISAO_PENDENTE`; pedir atendimento **não** chega a este estado — a compra fica em `AGUARDANDO_ASSOCIADO`. |
| **Confirmação expirada** (`CONFIRMACAO_EXPIRADA`) | Entender que o prazo passou e que existe uma saída | "O prazo para responder expirou. Nenhuma autorização foi feita. Você pode solicitar revisão." | Solicitar revisão | — | R04, R10 | Não existe | Implementar tela de expiração |
| **Serviço indisponível** | Entender o erro e saber que pode tentar novamente | Mensagem de erro genérica; opção de revisão ainda disponível | Tentar novamente / solicitar revisão | — | R09 | Não existe | Implementar tratamento de erro de rede/backend |

---

## 3. Textos candidatos

As colunas distinguem **o que já está na tela** (interface `212655c`) e **texto proposto** para a versão adaptada.

### 3.1 Tela principal — Compra + Alerta

| Elemento | Texto já na tela (212655c) | Texto proposto | Observação |
|---|---|---|---|
| Aviso de autenticidade | "Nunca pedimos senha ou código por telefone." | "Nunca pedimos senha ou código por telefone ou mensagem. Esta solicitação veio do seu app autenticado." | Identificar origem para reduzir desconfiança (HIP-04 de D06) |
| Cabeçalho da compra | "Aviso de compra no seu cartão final 4821" | "Compra sinalizada no cartão final \{last4\}" | Usar dados reais da sessão |
| Detalhes da compra | "R$ 2.349,90 · Loja Exemplo Eletrônicos / São Paulo, SP · hoje, 03:14" | "\{estabelecimento disponível ou 'Identificação não disponível'\} · R$ \{valor\} · \{data\} · \{canal_label\}" | Substituir dado fixo por dado da API; indicar limite quando não houver nome |
| Pergunta | "Foi você que comprou?" | "Você reconhece e autoriza esta compra?" | Texto explícito sobre as duas dimensões: reconhecimento e autorização (R02) |
| Indicação de simulação | Ausente | "Esta é uma demonstração. Nenhuma transação financeira real será realizada." | Obrigatório (R11) |
| Prazo | Ausente | "Válida até \{expires_at\} (horário do servidor)" | Responsabilidade de prazo no servidor, não no browser |

### 3.2 Três botões de resposta

| Botão | Rótulo curto | Descrição de efeito (abaixo do botão ou tooltip) | Status técnico | Texto atual (212655c) |
|---|---|---|---|---|
| `AUTHORIZE` | "Reconheço e autorizo" | "A compra será liberada na simulação e registrada." | `LIBERADA_SIMULACAO` | "Sim, fui eu" (+ biometria em seguida) |
| `DENY` | "Não reconheço" | "A compra será recusada na simulação. Um caso de revisão será aberto. **Seu cartão não será bloqueado automaticamente.**" | `RECUSADA_SIMULACAO` (compra); revisão de proteção abre **em paralelo** — compra **não** vai para `REVISAO_PENDENTE` | "Não reconheço" (→ tela de bloqueio de cartão) |
| `UNSURE` | "Estou em dúvida" | "A compra ficará em revisão. Você pode usar o chat para esclarecer antes de responder." | `REVISAO_PENDENTE` | Ausente |

### 3.3 Pedido de atendimento

| Elemento | Texto proposto | Notas |
|---|---|---|
| Link / botão | "Quero falar com alguém" | Separado dos três botões de resposta |
| Tela após clicar | "Sua solicitação de atendimento foi registrada. Protocolo: \{protocol\}. **Você ainda pode responder à pergunta da compra enquanto o prazo não expirar.**" | HIP-02 de D06; DEC-05 do plano |
| Prazo visível | "Confirmação válida até \{expires_at\}." | Não prorrogar; não repetir o prazo original como garantia |

### 3.4 Resultados

| Status | Título | Corpo | Próximo passo |
|---|---|---|---|
| `LIBERADA_SIMULACAO` | "Compra autorizada (simulação)" | "Registramos que você reconhece e autoriza esta compra. Nenhuma transação real foi feita." | — |
| `RECUSADA_SIMULACAO` | "Compra recusada (simulação)" | "Registramos que você não reconhece esta compra. Um caso de revisão foi aberto. **Seu cartão não foi bloqueado automaticamente.**" | "Se precisar de mais informações, acesse o atendimento da cooperativa." |
| `REVISAO_PENDENTE` | "Compra em revisão" | "Registramos sua resposta. Um analista vai avaliar o caso." | Protocolo se disponível |
| `CONFIRMACAO_EXPIRADA` | "Prazo encerrado" | "O prazo para responder a esta solicitação expirou. Nenhuma autorização foi feita." | "Você pode solicitar uma revisão pelo atendimento." |
| Erro de serviço | "Não foi possível enviar sua resposta" | "Tente novamente. Se o problema persistir, use o botão abaixo para solicitar revisão." | Botão "Tentar novamente" + link de revisão |

### 3.5 Erros e limites do agente

| Situação | Texto proposto |
|---|---|
| Nome do estabelecimento não disponível | "Não tenho informações sobre o nome fantasia deste estabelecimento. Os dados disponíveis são: categoria MCC \{label\}, região \{regiao\}." |
| Pergunta fora do contexto | "Não tenho informações sobre isso neste contexto. Você pode usar uma das três opções de resposta ou solicitar atendimento." |
| LLM indisponível | "O assistente está temporariamente indisponível. Você ainda pode responder à compra pelos botões abaixo ou solicitar revisão." |
| Agente não pode autorizar | "Não posso registrar uma autorização em seu nome. Use o botão 'Reconheço e autorizo' para confirmar." |

---

## 4. Revisão da interface atual (`212655c`)

### 4.1 Divergências críticas em relação ao plano

| Elemento | Comportamento atual | Comportamento esperado (plano §3, §5) | Prioridade |
|---|---|---|---|
| Respostas | `itWasMe` → tela de biometria → `biometrics` → confirmação | `AUTHORIZE` diretamente, sem biometria | P0 — PEN-01 |
| Biometria | Tela intermediária obrigatória para "Sim, fui eu" | Biometria fora do MVP (alinhamento 28/10, decisão 4) | P0 — PEN-01 |
| Terceira resposta | Ausente | `UNSURE` ("Estou em dúvida") obrigatório | P0 — PEN-01 |
| Mensagem após `notMe` | "Bloqueamos o cartão final 4821 e nada foi cobrado. Um cartão novo chega em até 7 dias úteis." | "A compra foi recusada na simulação. Seu cartão não foi bloqueado." | P0 — PEN-01 |
| Pedido de atendimento | Link sem ação (`href="#"`) | Ação real: chamar `solicitar_revisao`; mostrar protocolo; confirmação continua aberta | P0 — PEN-02 |
| Consumo de API | Reducer no browser; estado não persiste após recarga | Chamar API; estado persistido no banco | P0 — PEN-03 |

### 4.2 O que já funciona bem e pode ser aproveitado

- Estrutura visual de "celular do associado" com Card/Tile do Carbon — layout adequado para o MVP.
- `InlineNotification` para avisos ("Nunca pedimos senha...") — padrão certo, texto a ajustar.
- Separação visual entre painel do associado e console da analista — estrutura correta.
- Uso de tokens de motion do Carbon — já preparado para reduzir animação.

### 4.3 Verificação de acessibilidade (inspeção documental)

Não foi executada uma revisão com aplicação em execução. Com base no código inspecionado:

- `aria-label="Celular do associado"` presente — adequado.
- Botões com `renderIcon` e rótulo de texto — legíveis.
- Status de resultado não depende apenas de cor (`kind="success"` + texto).
- **Não verificado:** foco visível ao navegar por teclado; legibilidade em tela pequena real; tamanho mínimo de área de toque nos botões de resposta.

Uma revisão manual não comprova conformidade integral com nenhum padrão de acessibilidade. Registrar como pendência de verificação para C18.

---

## 5. Diagrama de estados

```
AGUARDANDO_ASSOCIADO
  ├─ AUTHORIZE (válido, no prazo)       → LIBERADA_SIMULACAO
  ├─ DENY (válido, no prazo)            → RECUSADA_SIMULACAO
  │                                        + revisão PROTECAO abre em paralelo
  │                                        (compra NÃO vai para REVISAO_PENDENTE)
  ├─ UNSURE (válido, no prazo)          → REVISAO_PENDENTE
  │                                        + revisão DUVIDA abre em paralelo
  ├─ pedido de atendimento              → compra PERMANECE em AGUARDANDO_ASSOCIADO
  │   (POST /api/purchases/{id}/review)    revisão abre; associado pode ainda responder
  ├─ resposta fora do prazo             → rejeição 410 (sem transição de estado da compra)
  └─ expiração (sem resposta)           → CONFIRMACAO_EXPIRADA
      (inclusive se revisão já aberta por pedido de atendimento anterior)

LIBERADA_SIMULACAO        → terminal
RECUSADA_SIMULACAO        → terminal (revisão PROTECAO aberta em paralelo)
REVISAO_PENDENTE          → terminal no fluxo do associado (revisão DUVIDA aberta em paralelo)
CONFIRMACAO_EXPIRADA      → terminal (revisão disponível via atendimento)
```

---

## 6. Especificação das adaptações do Watson — resumo para Leonardo

| Card | O que fazer | Arquivo / componente | Aceite verificável |
|---|---|---|---|
| C10 | Substituir 2 botões + biometria por 3 botões (`AUTHORIZE`/`DENY`/`UNSURE`); remover tela `biometrics`; alterar tela `protected` para mostrar compra recusada sem bloqueio de cartão | `MemberPhone.jsx`, `store.jsx` | Pessoa 4 percorre os três cenários sem biometria e sem mensagem de bloqueio |
| C10 | Implementar ação real para "Quero falar com alguém": chamar `POST /api/purchases/{case_id}/review`; exibir protocolo retornado; manter tela em `AGUARDANDO_ASSOCIADO` com botões de resposta ativos | `MemberPhone.jsx`, `store.jsx` | Pessoa 4 pede ajuda e vê protocolo; botões de resposta continuam ativos |
| C10 | Adicionar indicação visível de simulação e prazo do servidor | `MemberPhone.jsx` | Inspeção visual: texto aparece na tela principal |
| C13 | Substituir reducer local por chamadas à API: `GET /api/purchases/{case_id}`, `POST /api/confirmations/{challenge_id}/response`, `GET /api/purchases/{case_id}/status` | `src/api/`, `store.jsx` ou hooks | Recarregar página mantém o estado; dois usuários não veem compras um do outro |
| C18 | Corrigir textos de resultado, adicionar tela de expiração, tratar erro de serviço | `MemberPhone.jsx` | Textos da §3.4 aparecem nos estados correspondentes |
| C27 | Retestar após C10/C13/C18: três respostas, expiração, conflito, falha do chat, recarga | Todos os componentes | Casos P4-T01 a P4-T08 passam |

---

## 7. Aceite de D12

**D12 permanece em "revisado documentalmente".** Para avançar para "verificado em protótipo":

- [ ] Leonardo implementa C10 (três botões, sem biometria, sem mensagem de bloqueio).
- [ ] Pessoa 4 percorre o percurso completo (os 6 cenários da §2) na aplicação adaptada.
- [ ] Pessoa 2 revisa textos e fluxo.
- [ ] Evidências reais (capturas da aplicação na versão declarada) registradas em `evidencias/`.

Screenshots de telas desconectadas da API ou do reducer local não avançam o estado de D12.
