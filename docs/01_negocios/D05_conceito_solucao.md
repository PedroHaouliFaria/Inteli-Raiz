# D05 — Conceito da solução: confirmação assistida de compras

**ID:** D05 · **Versão:** 0.2 · **Data:** 04/11/2026
**Responsável:** Produto · **Estado:** rascunho revisado documentalmente; revisão cruzada pendente
**Fontes:** registro de evidências, plano de implementação e direcional.

**Revisor:** Pesquisa · **Estado:** rascunho

---

## 1. Usuário e situação

**Usuário:** o associado do Sicredi que recebe uma solicitação de confirmação de uma compra sinalizada pelo sistema.

**Situação:** o associado recebe uma notificação no app enquanto está em qualquer lugar — balcão, campo, madrugada. A compra tem valor real, mas o nome do estabelecimento pode ser irreconhecível. Ele precisa decidir se reconhece e autoriza, não reconhece ou está em dúvida — e saber o que acontece depois.

---

## 2. Problema

Hipótese do cenário investigado: o associado pode não encontrar um canal que reconheça como confiável para entender a compra e registrar sua resposta. Canal incerto ou informação insuficiente podem provocar abandono, erro ou busca de atendimento. A existência e suficiência dos canais atuais da instituição não foram pesquisadas. (D01 §4–5; HIP-04; HIP-03)

---

## 3. Solução em uma frase

Um assistente no app que apresenta a compra sinalizada, ajuda o associado a esclarecer dúvidas com o contexto disponível e permite registrar autorização, recusa ou dúvida — com revisão humana das exceções.

> Ponto de partida do plano (FON-01 §2). O modelo avalia sinais → a política define o tratamento → o agente consulta e explica → o associado responde explicitamente → o backend valida e registra.

---

## 4. Capacidade nova

**O que o associado passa a conseguir:** resolver a confirmação com clareza diretamente no app — sem ligar para a central — mesmo quando o nome do estabelecimento é ambíguo, porque o assistente apresenta o contexto disponível e informa o limite quando não há informação verificável.

**O que não muda:** a resposta final é sempre do associado. O assistente não autoriza, não recusa e não informa dúvida por ele. Ações financeiras são simuladas.

---

## 5. Experiência em três momentos

### Momento 1 — Recebe a solicitação
O associado abre o app e vê:

- Compra: estabelecimento ou identificação disponível, valor, data e cartão parcialmente identificado.

- Motivo do alerta: escrito com base nos sinais realmente disponíveis — sem inventar.

- Pergunta: "Você reconhece e autoriza esta compra?"

- Três respostas: "Reconheço e autorizo" · "Não reconheço" · "Estou em dúvida".

- Ação separada: "Quero falar com alguém" — não é uma quarta resposta à compra.

### Momento 2 — Entende ou pede ajuda
**Cenário A — Reconhece imediatamente:** toca em "Reconheço e autorizo". Fluxo direto; sem agente.

**Cenário B — Tem dúvida sobre o nome do estabelecimento:**
> Associado: "Pode ser o nome da empresa que aparece na fatura?"
> Assistente consulta o contexto disponível. Responde: "Não consigo confirmar o nome fantasia — tenho o código MCC 5411 e a região registrada. Os sinais disponíveis são: compra na madrugada, cartão não presente, primeiro uso do cartão. Se quiser, posso encaminhar para revisão."

O assistente não inventa a identidade do estabelecimento (DEC-09, Pesquisa). O associado ainda pode responder com qualquer uma das três opções.

**Cenário C — O agente não sabe responder:**
O associado pergunta algo fora do contexto disponível. O assistente declara explicitamente o limite: "Não tenho essa informação disponível. Posso encaminhar para revisão ou você pode escolher uma das respostas acima." Nunca inventa uma resposta.

### Momento 3 — Vê o resultado e o próximo passo
Após qualquer resposta, o app mostra:

- O que aconteceu com a **compra** (não com o cartão).

- Status: liberada, recusada, em revisão ou expirada.

- Próximo passo: o que o associado pode fazer agora.

Exemplos de resultado:

- `AUTHORIZE` → "Compra confirmada. Liberação registrada (simulação)."

- `DENY` → "Compra recusada. Um analista vai avaliar o caso. Protocolo: REV-0042."

- `UNSURE` → "Compra em revisão. Um analista vai avaliar."

- Expirada → "O prazo para responder terminou. A compra não foi autorizada. Um analista pode revisar o caso."

---

## 6. Papel do agente

O agente consulta ferramentas para obter sinais, disponibilidade da avaliação, contexto da compra e status. Escolhe ferramentas e pode solicitar revisão; não decide a resposta à confirmação. A ferramenta atual não devolve o valor numérico do score. **Explica** com base apenas no que as ferramentas retornam. **Informa o limite** quando o contexto é insuficiente. **Solicita revisão** quando a dúvida não pode ser resolvida.

O agente **não pode:** autorizar, recusar ou registrar dúvida em nome do associado; inventar identidade de estabelecimento; pressionar o associado a autorizar; pedir senha, PIN ou dados completos do cartão. (FON-P1-03 §4)

---

## 7. Limites

- Ações financeiras são simuladas. Nenhuma transação, bloqueio ou estorno real ocorre.

- O modelo de risco é experimental: PR-AUC 0,146 no teste com dados sintéticos; meta 0,80 não atingida (FON-P1-02 §5).

- Sem biometria e sem verificação de aparelho no MVP.

- O agente depende de LLM externo; se falhar, o caminho de confirmação (três botões) continua funcionando.

- Não há integração bancária real nem autenticação produtiva.

- Dados de entrada são sintéticos.

---

## 8. Dependências e hipóteses

| Dependência | Estado |
|---|---|
| Backend FastAPI + SQLite com rotas de confirmação | Implementado; testes atuais e log em D11 |
| Frontend React + Carbon com três respostas e API | Implementado em SessionGate/AssociateApp/PurchaseDetail; ensaio humano pendente |
| Agente Pydantic AI | Implementado; dependência principal declarada; padrão Groq; execução real depende de chave e registro |
| Modelo RF serializado | Arquivo presente e carregamento implementado; limitações de avaliação em D09 |

| Hipótese | Impacto se falsa |
|---|---|
| HIP-P1-05: texto fixo insuficiente para nome ambíguo | Justificativa de IA agêntica precisa de outro caso |
| HIP-01: associado confunde recusa com bloqueio do cartão | Texto de resultado é a decisão de design mais urgente |

---


**Revisão necessária:** Pesquisa confere conceito/cenários; registro central de aceite identifica o estado da revisão cruzada.
