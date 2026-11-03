# D05, D07 e D08 — Conceito, Ideia e Proposta de Valor

**ID:** D05 · D07 · D08 · **Versão:** 0.1 · **Data:** 03/11/2026
**Responsável:** Pessoa 1
**Revisores:** D05 → Pessoa 2; D07 → Pessoa 4; D08 → Pessoa 3
**Estado:** rascunho
**Fontes principais:** FON-01 (plano §§2–4, 7), FON-P1-01 (desafio pp.6–10), FON-P1-02 (D09), FON-P1-03 (D10), FON-P1-04 (D12)
**Depende de:** D01, D04 · **Alimenta:** D07, D08, D09 (revisão PEN-P3-01), D10, D12
**Nota:** D05, D07 e D08 estão neste arquivo por compartilharem conteúdo, conforme o direcional orienta. Cada seção tem seu próprio cabeçalho e pode ser referenciada independentemente.

---

# D05 — Conceito da solução: confirmação assistida de compras

**Revisor:** Pessoa 2 · **Estado:** rascunho

---

## 1. Usuário e situação

**Usuário:** o associado do Sicredi que recebe uma solicitação de confirmação de uma compra sinalizada pelo sistema.

**Situação:** o associado recebe uma notificação no app enquanto está em qualquer lugar — balcão, campo, madrugada. A compra tem valor real, mas o nome do estabelecimento pode ser irreconhecível. Ele precisa decidir se reconhece e autoriza, não reconhece ou está em dúvida — e saber o que acontece depois.

---

## 2. Problema

O associado não tem, hoje, um canal direto confiável para entender a compra sinalizada, pedir ajuda contextual e registrar sua resposta explícita sem precisar ligar para ninguém. Quando o canal é incerto (parece golpe) ou a informação é insuficiente (nome ambíguo), o associado ignora, comete um erro ou vai à agência. (D01 §4–5; HIP-04; HIP-03)

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

O assistente não inventa a identidade do estabelecimento (DEC-09, Pessoa 2). O associado ainda pode responder com qualquer uma das três opções.

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

O agente **consulta** (não decide): chama ferramentas para buscar score, sinais, contexto da compra e status da confirmação. **Explica** com base apenas no que as ferramentas retornam. **Informa o limite** quando o contexto é insuficiente. **Solicita revisão** quando a dúvida não pode ser resolvida.

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
| Backend FastAPI + SQLite com rotas de confirmação | Implementado e testado (FON-P1-05; backend `b39bbb9`) |
| Frontend React + Carbon com três botões e consumo da API | Em adaptação (PEN-01/PEN-03 da Pessoa 4; C10/C13 ativos) |
| Agente Pydantic AI com LLM externo | Planejado; LLM não confirmado; `pydantic_ai` com pendência de instalação (PEN-04 da Pessoa 4) |
| Modelo RF serializado | A serializar do notebook 03; com pendências técnicas (FON-P1-02 §8) |

| Hipótese | Impacto se falsa |
|---|---|
| HIP-P1-05: texto fixo insuficiente para nome ambíguo | Justificativa de IA agêntica precisa de outro caso |
| HIP-01: associado confunde recusa com bloqueio do cartão | Texto de resultado é a decisão de design mais urgente |

---

---

# D07 — Ideia preliminar: assistente de confirmação de compras

**Revisor:** Pessoa 4 · **Estado:** rascunho

---

## 1. Ficha da ideia

| Campo | Conteúdo |
|---|---|
| **Nome descritivo** | Assistente de confirmação de compras |
| **Problema** | O associado não tem canal confiável para entender e responder a uma compra sinalizada sem ligar para ninguém |
| **Usuário** | Associado do Sicredi com uma compra sinalizada aguardando confirmação |
| **Solução em uma frase** | Um assistente no app que mostra a compra, esclarece dúvidas com o contexto disponível e registra a resposta explícita do associado — com revisão humana das exceções |
| **Três capacidades essenciais** | (1) Apresentar a compra com o contexto disponível e o motivo do alerta; (2) responder dúvidas contextuais sobre a compra sem inventar informação; (3) registrar a resposta explícita do associado (autorizar / recusar / dúvida) e mostrar o desfecho |
| **Resultado esperado** | O associado conclui a confirmação sem ligar para ninguém, entendendo o que autorizou e o que acontece a seguir |
| **Estágio** | Protótipo em desenvolvimento; integração frontend-backend pendente |
| **Maior hipótese aberta** | HIP-P1-05: o agente faz diferença real nos casos de nome ambíguo. Se a confirmação com texto fixo resolver bem, a necessidade do agente precisa ser demonstrada em outro cenário |

---

## 2. Versão de ~30 segundos (pitch falado)

> **Nota:** os "30 segundos" são o tempo do pitch oral, não uma meta de tempo de uso do produto. As metas de tempo de uso (Hills do Leonardo) são aspirações de design, não resultados medidos.

---

"Quando o sistema identifica uma compra suspeita, o associado recebe uma notificação no app. A tela mostra os detalhes da compra, o motivo do alerta e três opções: autorizar, não reconhecer ou informar dúvida. Se tiver uma pergunta — por exemplo, 'esse nome na fatura é o restaurante que fui?' — o assistente responde com o contexto disponível. Se não souber, ele diz que não sabe e oferece revisão humana. A resposta é sempre do associado. Tudo é simulado — nenhuma transação financeira real é executada."

---

## 3. Mini-roteiro de teste da explicação

> **Objetivo:** verificar se alguém de fora do grupo entende a ideia após ouvir o pitch de 30 s acima.

| Pergunta | O que quer verificar |
|---|---|
| "Quem usa esse produto?" | O associado está claro (não o analista, não o banco) |
| "O que o produto faz?" | As três capacidades estão presentes |
| "O que acontece quando o associado não reconhece a compra?" | Distinção entre recusa e bloqueio do cartão |
| "O agente pode autorizar a compra por você?" | Limite do agente está claro |
| "Alguma transação financeira real acontece?" | Simulação está clara |

**Estado:** pendente — não executado. Executar antes de fechar D07.

---

## 4. Coerência com D05 e D11/D12

- D07 descreve o mesmo assistente de D05, em linguagem acessível.
- As três capacidades de D07 mapeiam para os momentos 1–3 de D05.
- D11 (Pessoa 4) documenta o fluxo técnico que implementa essas capacidades; D12 (Pessoa 4) documenta a interface.
- Divergência identificada: frontend atual tem dois botões + biometria (PEN-01 da Pessoa 4); D07 descreve três respostas + sem biometria. Registrado como PEN-D07-01 no README.

---

---

# D08 — Proposta de valor e necessidade de IA agêntica

**Revisor:** Pessoa 3 · **Estado:** rascunho — será atualizado após D13.

---

## 1. Tabela da proposta de valor

| Parte | Conteúdo |
|---|---|
| **Dor e público** | O associado não consegue resolver uma compra sinalizada de forma autônoma quando o nome do estabelecimento é ambíguo ou o canal parece suspeito. Sem um caminho claro no app, o caso exige ligação para a central ou vai ao analista sem resposta do associado. (D01 N1–N4; HIP-03; HIP-04) |
| **Solução em uma frase** | Um assistente de confirmação no app que apresenta a compra, responde dúvidas contextuais e registra a resposta explícita do associado — com revisão humana das exceções. |
| **Quem usa** | **Associado:** usa diretamente o app de confirmação. **Analista:** recebe os casos de exceção (não reconhecimento, dúvida, expiração). |
| **Quem adota e quem paga** | Decisor: a instituição financeira (Sicredi ou equivalente). Hipótese de adoção: a instituição adotaria se o produto reduzisse contatos de atendimento por dúvida e melhorasse a experiência do associado. **Interesse comercial não confirmado** — trata-se de projeto acadêmico sem compromisso da instituição. (HIP-P1-01) |
| **Posicionamento** | Solução vertical de serviços financeiros cooperativos. Benefício ao associado (clareza e autonomia) e adoção pela instituição (redução de atendimento) são papéis diferentes. |
| **Valor para o associado** | Resolver a confirmação sem ligar; entender o que autorizou; saber o desfecho imediatamente. Hipóteses mensuráveis: ≥ 3/5 participantes concluem a tarefa sem ajuda do moderador; ≤ 1 decisão equivocada por sessão (D09 §5). |
| **Valor para a organização** | Hipótese: redução de contatos de atendimento para dúvidas sobre compras sinalizadas. **Não equivale a redução de perdas financeiras.** Valor das transações sinalizadas ≠ perdas evitadas. (DEC-P1-03) |
| **Por que IA e qual arquétipo** | Ver seção 2 abaixo. |
| **Por que agora** | O desafio Sicredi propõe "alerta preventivo e confirmação pelo associado" (FON-P1-01 p.6). O modelo RF treinado na base sintética fornece scores como ponto de partida. A plataforma de desenvolvimento (IBM Bob) e os LLMs de plano gratuito (Groq/Gemini) estão disponíveis. A ausência de IBM Cloud em runtime elimina uma barreira técnica. |
| **Evidência, custo e limites** | PR-AUC 0,146 no teste com dados sintéticos; meta 0,80 não atingida; modelo não calibrado (FON-P1-02 §5). Nenhuma evidência de redução de fraudes reais. Nenhum teste com usuários executado até esta versão. Ver seção 4 (premissas) e seção 5 (limites). |

---

## 2. Por que IA agêntica e qual arquétipo

### Comparação: texto fixo × agente

| Capacidade | Alternativa A (texto fixo) | Alternativa B (agente) |
|---|---|---|
| Apresentar compra com contexto disponível | ✓ — com texto pré-definido | ✓ — com contexto dinâmico da compra |
| Explicar por que a compra foi sinalizada | ✗ — texto genérico | ✓ — lista sinais retornados pelo modelo |
| Responder "esse nome é o restaurante que fui?" | ✗ — sem consulta contextual | ✓ — informa o máximo disponível; declara o limite se não souber |
| Resolver caso com nome de estabelecimento ambíguo | ✗ — associado fica sem resposta | ✓ — contexto + declaração de limite + opção de revisão |
| Encaminhar para revisão com protocolo | ✓ — via botão fixo | ✓ — via ferramenta `solicitar_revisao` |

**Justificativa:** o agente demonstra necessidade real no caso de dúvida contextual sobre o estabelecimento (HIP-P1-05). Se o piloto de D13 mostrar que texto fixo resolve esse caso igualmente bem, a justificativa precisa ser revisada.

### Arquétipos candidatos (DEC-P1-04)

> Interpretações candidatas dos arquétipos do desafio (FON-P1-01 pp.7–10), a confirmar pelo comportamento executado:

- **Especialista sensível ao contexto:** o agente responde dúvidas sobre a compra específica — não dá respostas genéricas. Consulta ferramentas (`avaliar_transacao`, `consultar_compra`) para basear a explicação nos dados reais.
- **Gestor da fronteira humano–IA:** o agente sabe o que pode resolver (explicar, informar limite, solicitar revisão) e o que não pode (autorizar, recusar, inventar informação). A fronteira é explícita e testável.

### Decomposição saber / decidir / fazer

| Dimensão | Conteúdo |
|---|---|
| **Saber** | Score e sinais descritivos da compra (`avaliar_transacao`); contexto da compra — estabelecimento disponível, valor, data, cartão parcial, MCC, região (`consultar_compra`); estado atual da confirmação e próximos passos (`consultar_status`) |
| **Decidir** | Qual ferramenta consultar para a dúvida específica; quando informar o limite (contexto insuficiente); quando solicitar revisão (dúvida irresolvível) |
| **Fazer** | Chamar ferramentas autorizadas; retornar explicação baseada nos dados; nunca chamar `responder_confirmacao` — essa operação é exclusiva do controle da interface humana |

**Dúvida fora do contexto:** se o associado fizer uma pergunta que nenhuma ferramenta resolve, o agente declara o limite explicitamente e mantém o caminho de revisão. Nunca inventa.

**RAG e múltiplos agentes:** não entram nesta versão — sem necessidade demonstrada para o escopo atual.

---

## 3. Posicionamento nos eixos (interpretação candidata)

| Eixo | Posição candidata | Fonte |
|---|---|---|
| Vertical / Horizontal | Vertical — serviços financeiros cooperativos | FON-P1-01 p.6 (desafio Sicredi específico) |
| Interno / Externo | Interno ao processo da cooperativa (experiência do associado) | Fluxo de confirmação é operação interna |

---

## 4. Premissas de viabilidade

> Cada premissa está marcada com fonte verificável ou `[a definir]`. Fórmula: **custo de IA = casos processados × chamadas médias por caso × custo médio por chamada**; infraestrutura e revisão humana computadas à parte.

| Premissa | Cenário conservador | Cenário base | Fonte |
|---|---|---|---|
| Volume de confirmações enviadas ao associado por mês | `[a definir]` | `[a definir]` | Dados operacionais da Sicredi; não disponíveis |
| Proporção de casos onde o associado usa o chat | 100% (todos usam o agente) | 30% (apenas casos com dúvida) | HIP-P1-04; sem medição real |
| Chamadas de LLM por sessão de chat | 4 mensagens/sessão | 2 mensagens/sessão | Estimativa; sem instrumentação |
| Custo por chamada de API do LLM | Groq gratuito = $0 no piloto; Gemini Flash ~$0,0001/1k tokens | Mesmo | Preços públicos; sujeitos a mudança |
| Esforço de atendimento evitado por caso resolvido autonomamente | `[a definir]` | `[a definir]` | Tempo médio de atendimento não levantado |
| Custo de revisão humana por exceção | `[a definir]` | `[a definir]` | Dados operacionais não disponíveis |

**Conclusão das premissas:** com Groq/Gemini gratuito no piloto, o custo de IA é próximo de zero. Para uma estimativa de produção, os campos `[a definir]` precisam ser preenchidos com dados reais da instituição. A economia eventual depende do tempo realmente evitado no atendimento — que só pode ser medido após o piloto.

---

## 5. Métricas do protótipo × efeitos operacionais

| Métrica | Pode ser medida no protótipo | Não pode ser medida no protótipo |
|---|---|---|
| Conclusão da tarefa sem ajuda do moderador | ✓ (D13 §4) | — |
| Compreensão da consequência de cada resposta | ✓ (perguntas de compreensão, D13) | — |
| Frequência de decisão equivocada | ✓ (D13 §4) | — |
| Redução de contatos de atendimento | ✗ — exige volume real e comparação com baseline operacional | — |
| Redução de perdas por fraude | ✗ — exige dados reais de fraude confirmada e período de medição | — |
| Eficácia do modelo RF em produção | ✗ — modelo treinado em dados sintéticos; PR-AUC 0,146 | — |

**Separação obrigatória (DEC-P1-03):** resultados do piloto (3–5 pessoas) não comprovam efeito operacional. Valor das transações sinalizadas ≠ perdas evitadas. Esta versão apresenta hipóteses mensuráveis, não resultados.

---

## 6. Este documento será atualizado após D13

Ao concluir D13 (validação), atualizar:
- Seção 1 (valor para o associado): substituir metas por resultados reais de compreensão e conclusão.
- Seção 1 (evidência): adicionar TST-xx com perfil dos participantes, versão testada e resultados.
- Seção 4 (premissas): incorporar contagem de mensagens de chat por caso se o piloto for instrumentado.
- Seção 2 (justificativa de IA): atualizar se o piloto mostrar que texto fixo resolve igualmente bem o caso de nome ambíguo.
