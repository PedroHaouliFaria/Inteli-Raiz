# D04 — Alternativas de solução e decisão de prioridade

**ID:** D04 · **Versão:** 0.2 · **Data:** 04/11/2026
**Responsável:** Produto · **Revisor principal:** Arquitetura
**Estado:** rascunho
**Fontes principais:** FON-01 (plano §§2–3), FON-P1-01 (desafio arquétipos pp.7–10), D01 (HMW e oportunidades), D09/D10 (Arquitetura)
**Decisões que sustenta:** DEC-P1-02 (direção escolhida)
**Depende de:** D01 · **Alimenta:** D05, D08

---

## Sumário

- [1. HMW de partida](#1-hmw-de-partida)
- [2. Registro de ideias — sementes para a discussão](#2-registro-de-ideias--sementes-para-a-discussão)
- [3. Discussão em grupo — roteiro pendente](#3-discussão-em-grupo--roteiro-pendente)
- [4. Alternativas comparáveis](#4-alternativas-comparáveis)
- [5. Premissa frágil e experimento inversor](#5-premissa-frágil-e-experimento-inversor)
- [6. O que foi descartado e por quê](#6-o-que-foi-descartado-e-por-quê)
- [7. Matriz de rastreabilidade (contribuição D04)](#7-matriz-de-rastreabilidade-contribuição-d04)

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

**Objetivo da sessão:** cada pessoa propõe ideias individualmente (5 min), depois compartilha em grupo. A facilitadora (Produto) agrupa por necessidade, não por semelhança de solução.

**Roteiro sugerido:**
1. Cada pessoa escreve 3–5 ideias para o HMW acima, sem filtrar por viabilidade. Individualmente, sem ver as dos outros.
2. Compartilhamento em rodada: cada um apresenta suas ideias; sem crítica nesta etapa.
3. Agrupamento por necessidade/capacidade: quais ideias resolvem "confiança no canal"? Quais resolvem "contexto insuficiente"? Quais resolvem "desconhecimento das consequências"?
4. Avaliar ao menos três direções comparáveis usando a matriz da seção 4.
5. Confirmar ou ajustar a decisão já tomada no plano.

**Resultado esperado:** confirmação ou ajuste da direção B (abaixo), com registro do que foi debatido e descartado.

---

## 4. Alternativas comparáveis

<p align="justify">&ensp;&ensp; Revisão documental da escolha já feita no plano. A equipe ainda precisa discutir as alternativas; não houve brainstorming coletivo nem teste comparativo nesta revisão. "Ter IA" não recebe pontuação de qualidade. As três opções usam os mesmos detalhes, sinais calculados, consequências das respostas e opção de revisão.</p>

| Critério | A — Interface sem conversa | B — Mesma interface com agente | C — Atendimento humano como caminho principal |
|---|---|---|---|
| Necessidade atendida | Compra, sinais, prazo, três respostas, limite de dados e revisão por texto determinístico | Tudo de A mais perguntas em linguagem natural e escolha de ferramentas | Esclarecimento com atendente, preservando resposta explícita e registro |
| Impacto humano | Pode ser suficiente; clareza e acerto ainda não medidos | Pode reduzir esforço para interpretar contexto; vantagem ainda não medida | Pode ajudar casos complexos; espera e disponibilidade não medidas |
| Inteligência necessária | Regras e dados estruturados; não exige LLM para apresentar sinais específicos | Consulta e diálogo contextual; não cria identidade de estabelecimento ausente | Julgamento humano; não exige agente para todos os casos |
| Valor organizacional | Menor complexidade técnica; potencial de resolver casos simples | Possível redução de dúvidas repetidas; custo extra e falhas do LLM | Maior dependência de disponibilidade humana; custo ainda desconhecido |
| Viabilidade atual | API e frontend implementados; ensaio independente pendente | Chat/ferramentas implementados; LLM real depende de configuração e rastro de execução | Revisão/protocolo implementados; operação de atendimento real fora do MVP |
| Risco | Texto insuficiente para dúvida não prevista | Resposta incorreta, contexto insuficiente, latência e custo | Fila/espera e repetição de contexto |
| Decisão provisória | Base obrigatória e baseline competitivo | Camada opcional selecionada para investigar HIP-P1-05 | Manter revisão humana para exceções, sem construir central de atendimento |

<p align="justify">&ensp;&ensp; <strong>DEC-P1-02 revisada:</strong> manter A como núcleo e B como experimento de ajuda contextual. B só demonstra vantagem se melhorar compreensão/conclusão sem aumentar decisões equivocadas em D13, com as mesmas informações em A/B. A aderência ao tema IA do desafio é um critério de escopo separado; não prova utilidade nem torna A incapaz de atender o usuário.</p>

<p align="justify">&ensp;&ensp; Nome ambíguo permanece sem identificação verificável em A, B e C quando ninguém dispõe de fonte adicional. O agente pode comunicar melhor o limite; não pode resolver a ausência de informação inventando um nome.</p>

## 5. Premissa frágil e experimento inversor

<p align="justify">&ensp;&ensp; <strong>Premissa frágil da direção B (HIP-P1-05):</strong> o agente demonstra valor real no piloto — o associado chega a uma decisão melhor quando usa a ajuda contextual do que quando usa apenas os três botões.</p>

<p align="justify">&ensp;&ensp; <strong>Experimento que poderia inverter a escolha:</strong> no piloto de D13, alternar fluxo básico (A) × fluxo com agente (B) com casos equivalentes. Se as contagens e observações do piloto não mostrarem vantagem consistente em compreensão e decisão correta, a necessidade de IA agêntica precisa ser justificada por outro cenário.</p>

<p align="justify">&ensp;&ensp; <strong>Alternativa que assumiria se B fosse invertido:</strong> A (texto fixo) como entrega principal, com o agente como funcionalidade opcional a ser testada em versão futura.</p>

---

## 6. O que foi descartado e por quê

| Ideia / direção | Motivo do descarte |
|---|---|
| URA de confirmação por telefone | Canal de voz não integrado ao fluxo; risco de phishing via número falso (HIP-04); fora do escopo |
| FAQ contextual estático | Pode compor A; sua suficiência precisa ser comparada antes de justificar conversa com LLM |
| Notificação preventiva antes da compra | Muda a arquitetura radicalmente; exige integração em tempo real com POS; fora do escopo do MVP |
| RAG (base de conhecimento) | Sem necessidade demonstrada no recorte atual; o contexto necessário é da compra específica, não de documentos externos |
| Múltiplos agentes | Sem necessidade demonstrada; um agente com ferramentas é suficiente para o cenário definido (FON-P1-03 §4) |

---

## 7. Matriz de rastreabilidade (contribuição D04)

| Evidência / hipótese | Necessidade (D01) | Decisão | Requisito do plano | Como verificar | Resultado / versão |
|---|---|---|---|---|---|
| HIP-P1-05: texto fixo insuficiente para nome ambíguo | N1 — contexto da compra | DEC-P1-02: B sobre A | R08 (dúvida contextual) | Alternância de fluxo no piloto D13 | Pendente |
| HIP-P1-02: compreensão recusa × bloqueio do cartão | N3 — saber o efeito de cada resposta | DEC-P1-02: texto de resultado explícito como parte de A+B | R03, R11 | Tarefa "não reconheço" + pergunta de compreensão | Pendente |
