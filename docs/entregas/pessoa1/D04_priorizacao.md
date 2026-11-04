# D04 — Alternativas de solução e decisão de prioridade

**ID:** D04 · **Versão:** 0.1 · **Data:** 03/11/2026
**Responsável:** Pessoa 1 · **Revisor principal:** Pessoa 3
**Estado:** rascunho
**Fontes principais:** FON-01 (plano §§2–3), FON-P1-01 (desafio arquétipos pp.7–10), D01 (HMW e oportunidades), D09/D10 (Pessoa 3)
**Decisões que sustenta:** DEC-P1-02 (direção escolhida)
**Depende de:** D01 · **Alimenta:** D05, D08

---

> **Nota sobre o processo:** o direcional §D04 orienta que cada integrante proponha ideias individualmente antes da discussão em grupo. Esse brainstorming **não foi executado** nesta versão — a seção 3 ("Discussão em grupo") está como roteiro a facilitar. A análise abaixo usa como ponto de partida a direção já escolhida no plano vigente (FON-01 §2) e a registra como **revisão da decisão**, conforme o direcional orienta quando a discussão ocorre após a escolha.

---

## 1. HMW de partida

> De D01 §8:

"Como poderíamos ajudar o associado a decidir sobre uma compra sinalizada com clareza sobre o que está autorizando e sobre o próximo passo quando continua em dúvida?"

---

## 2. Registro de ideias — sementes para a discussão

> Estas sementes foram propostas pelo direcional §D04 como ponto de partida. Não representam brainstorming executado pelo grupo.

| Agrupamento | Ideias |
|---|---|
| **Resposta direta** | Confirmação com texto fixo e três botões; SMS de confirmação com link; URA de confirmação por telefone |
| **Ajuda contextual** | Agente no app que responde dúvidas sobre a compra; explicação automática dos sinais do alerta; FAQ contextual por categoria de compra |
| **Escalada humana** | Encaminhamento direto para atendente especializado; chatbot que coleta o problema e repassa à central; opção "ligue agora" integrada ao app |
| **Prevenção antecipada** | Notificação antes do bloqueio para o associado confirmar no momento da compra; alert preditivo antes de a compra ser feita |

---

## 3. Discussão em grupo — roteiro pendente

> **Estado: não executado.** Usar este roteiro antes de fechar D04.

**Objetivo da sessão:** cada pessoa propõe ideias individualmente (5 min), depois compartilha em grupo. A facilitadora (Pessoa 1) agrupa por necessidade, não por semelhança de solução.

**Roteiro sugerido:**
1. Cada pessoa escreve 3–5 ideias para o HMW acima, sem filtrar por viabilidade. Individualmente, sem ver as dos outros.
2. Compartilhamento em rodada: cada um apresenta suas ideias; sem crítica nesta etapa.
3. Agrupamento por necessidade/capacidade: quais ideias resolvem "confiança no canal"? Quais resolvem "contexto insuficiente"? Quais resolvem "desconhecimento das consequências"?
4. Avaliar ao menos três direções comparáveis usando a matriz da seção 4.
5. Confirmar ou ajustar a decisão já tomada no plano.

**Resultado esperado:** confirmação ou ajuste da direção B (abaixo), com registro do que foi debatido e descartado.

---

## 4. Alternativas comparáveis

> Âncoras das notas de impacto humano, necessidade de inteligência e valor organizacional (critérios das aulas, S2 pp.35–45):
>
> **1 — Mínimo:** resolve a necessidade de forma básica ou não resolve  
> **3 — Parcial:** resolve em parte; exige complemento ou deixa lacuna relevante  
> **5 — Forte:** resolve bem a necessidade com base em evidência ou justificativa clara

| Critério | Alternativa A — Confirmação com texto fixo | Alternativa B — Ajuda contextual com agente | Alternativa C — Encaminhamento humano assistido |
|---|---|---|---|
| **Descrição** | Tela com detalhes da compra (valor, data, estabelecimento disponível) e três botões fixos. Sem conversa; sem explicação dinâmica | Tela de confirmação com agente que responde dúvidas usando o contexto disponível (score, sinais, dados da compra). Três respostas explícitas + pedido de atendimento separado | Tela com botão "Falar com atendente" como caminho principal. O app coleta o contexto e repassa à central; o atendente resolve |
| **Impacto humano + evidência** | **3** — Resolve N2 (canal legítimo) e N5 (desfecho visível) bem. Não resolve N1 (nome ambíguo) nem N3 (consequência da resposta) sem texto de apoio explícito. (HIP-P1-05: texto fixo pode ser insuficiente para nome ambíguo) | **5** — Resolve N1 (agente informa o contexto disponível ou o limite), N2, N3, N4 e N5. Hipótese mais forte de resolução completa das necessidades. Condicionada à HIP-P1-05: se texto fixo resolver N1, a vantagem cai para 4 | **3** — Resolve N2, N4 e N6 bem; preserva a qualidade humana do atendimento. Não escala: cada caso exige um atendente; não reduz esforço de atendimento |
| **Necessidade de inteligência (raciocínio / autonomia / coordenação)** | **1** — Sem inteligência contextual; apenas política determinística. Não demonstra IA agêntica | **5** — Requer raciocínio sobre qual ferramenta usar para cada dúvida; autonomia limitada e controlada (não autoriza); coordenação entre ferramentas e política. Demonstra IA agêntica com limites explícitos (FON-P1-03 §4) | **1** — A inteligência está no atendente humano; o app só coleta e repassa. Não demonstra IA agêntica |
| **Valor organizacional** | **3** — Pode reduzir contatos simples; sem diferenciação; falha no caso ambíguo pode gerar mais contatos pós-decisão | **4** — Hipótese: reduz contatos de dúvida contextual sem escalar o custo com atendentes (HIP-P1-03). Valor depende da frequência de casos ambíguos (HIP-03) | **2** — Não reduz esforço de atendimento; pode aumentá-lo se o volume crescer. Custo de atendente por caso é alto |
| **Viabilidade e risco** | **Alta viabilidade** — Backend e frontend já existem para o caminho de confirmação; texto fixo é o núcleo já implementado no Watson (FON-P1-04) | **Média viabilidade** — Backend e agente estão planejados; LLM não confirmado; `pydantic_ai` com pendência de instalação (PEN-04 da Pessoa 4). Risco: agente falha e bloqueia o fluxo se não houver fallback | **Alta viabilidade técnica; baixa viabilidade de escala** — Requer disponibilidade de atendente; fora do escopo do MVP; viola objetivo de reduzir dependência da central |
| **Decisão** | **Combinada como base:** o caminho de texto fixo (três botões + tela de resultado) é o núcleo obrigatório. Funciona sem agente e atende R01–R07, R09–R12 | **Selecionada:** camada adicional ao texto fixo. O agente só é chamado quando há dúvida contextual; a confirmação funciona sem ele (R08 não bloqueia o caminho principal) | **Descartada para o MVP:** fora do escopo; contradiz o objetivo de resolução autônoma |

### Resumo da decisão (DEC-P1-02)

A direção escolhida é **B sobre A**: texto fixo como base + agente como camada de ajuda contextual. Essa é a direção já definida no plano (FON-01 §2). Esta matriz a registra como revisão da decisão, confirmando-a com critérios explícitos.

**Por que não só A:** A não demonstra IA agêntica e não resolve o caso de nome ambíguo — o cenário central de risco identificado em D01 §9 e D03 §4.

**Por que não C:** C é uma direção de negócio diferente (central ampliada), não um MVP de IA agêntica. Não atende o desafio.

**Combinação:** B inclui A. A base (texto fixo + política) funciona sem agente. O agente acrescenta valor exatamente quando A falha.

---

## 5. Premissa frágil e experimento inversor

**Premissa frágil da direção B (HIP-P1-02):** o agente demonstra valor real no piloto — o associado chega a uma decisão melhor quando usa a ajuda contextual do que quando usa apenas os três botões.

**Experimento que poderia inverter a escolha:** no piloto de D13, alternar fluxo básico (A) × fluxo com agente (B) com casos equivalentes. Se a diferença em compreensão e decisão correta for insignificante, a necessidade de IA agêntica precisa ser justificada por outro cenário.

**Alternativa que assumiria se B fosse invertido:** A (texto fixo) como entrega principal, com o agente como funcionalidade opcional a ser testada em versão futura.

---

## 6. O que foi descartado e por quê

| Ideia / direção | Motivo do descarte |
|---|---|
| URA de confirmação por telefone | Canal de voz não integrado ao fluxo; risco de phishing via número falso (HIP-04); fora do escopo |
| FAQ contextual estático | Não responde à dúvida específica sobre a compra em questão; equivale à Alternativa A sem os botões explícitos |
| Notificação preventiva antes da compra | Muda a arquitetura radicalmente; exige integração em tempo real com POS; fora do escopo do MVP |
| RAG (base de conhecimento) | Sem necessidade demonstrada no recorte atual; o contexto necessário é da compra específica, não de documentos externos | 
| Múltiplos agentes | Sem necessidade demonstrada; um agente com ferramentas é suficiente para o cenário definido (FON-P1-03 §4) |

---

## 7. Matriz de rastreabilidade (contribuição D04)

| Evidência / hipótese | Necessidade (D01) | Decisão | Requisito do plano | Como verificar | Resultado / versão |
|---|---|---|---|---|---|
| HIP-P1-05: texto fixo insuficiente para nome ambíguo | N1 — contexto da compra | DEC-P1-02: B sobre A | R08 (dúvida contextual) | Alternância de fluxo no piloto D13 | Pendente |
| HIP-P1-02: compreensão recusa × bloqueio do cartão | N3 — saber o efeito de cada resposta | DEC-P1-02: texto de resultado explícito como parte de A+B | R03, R11 | Tarefa "não reconheço" + pergunta de compreensão | Pendente |
