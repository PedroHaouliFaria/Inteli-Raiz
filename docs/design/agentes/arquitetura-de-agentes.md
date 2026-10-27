# Arquitetura de agentes para desenhar o Watson

Proposta de como dividir o trabalho de interface entre agentes que rodam em paralelo, cada um com **uma técnica e uma metodologia** claras. O desenho segue o próprio IBM Enterprise Design Thinking: o **Loop** (Observe → Reflect → Make) define as fases, os **Keys** (Hills, Playbacks, Sponsor Users) definem os pontos de alinhamento, e o princípio de **times diversos e empoderados** vira agentes com papéis diferentes.

## Visão geral

```
                    ┌──────────────────────────────┐
                    │  Orquestrador (Facilitador DT)│  ← guarda Hills, roda Playbacks,
                    │  dono do canvas e do checklist│     pede a escolha do Leo
                    └──────────────┬───────────────┘
        ┌──────────────┬───────────┼────────────┬──────────────┐
        ▼              ▼           ▼            ▼              ▼
  Pesquisador UX   Estrategista  Designers de   Guardião do    Crítico /
  (Observe)        (Reflect)     versão A/B/C   estilo IBM     Avaliador
                                 (Make)         (Carbon)       (Playback)
```

| Agente | Fase do Loop | Técnicas (toolkit IBM / UX) | Entrega | Roda em paralelo com |
|---|---|---|---|---|
| **Orquestrador · Facilitador de DT** | todas | Hills, Playbacks, Prioritization Grid, decisão do Leo | plano, checklist, canvas, pedido de escolha | coordena todos |
| **Pesquisador UX** | Observe | Interviews, Contextual Inquiry, roteiro de entrevista, análise do dataset do case | achados, citações, dados de apoio | Estrategista |
| **Estrategista de produto** | Reflect | Empathy Map, As-is Scenario, Needs Statements / POV, HMW, Assumptions and Questions, teste "por que precisa ser IA agêntica" | personas, Hills, premissas | Pesquisador |
| **Designer da versão A, B e C** (um agente por versão) | Make | Big Idea Vignettes → Wireframes → Mockup → Protótipo, cada um defendendo uma direção diferente | 3 versões por etapa | entre si |
| **Guardião do estilo IBM** | Make | Carbon Design System (tokens, IBM Plex, 2x Grid, componentes), IBM Design Language (fotografia e ilustração de pessoas), WCAG 2.2 AA | revisão de conformidade, correções | Designers |
| **Crítico / Avaliador** | Reflect | Cognitive Walkthrough com as personas, heurísticas de Nielsen, Feedback Grid (gostei / críticas / perguntas / ideias) | parecer comparativo das 3 versões | depois dos Designers |
| **Pesquisador de referências e skills** | apoio | pesquisa na web, curadoria de fontes | skills reutilizáveis | todos |

## Fluxo por etapa (wireframe, mockup, protótipo, alta fidelidade)

1. **Briefing** (Orquestrador): relembra Hills e personas, define o que muda nessa etapa.
2. **Make em paralelo**: três Designers geram as versões A, B e C ao mesmo tempo, cada um com uma hipótese diferente (ex.: tela dividida, agente conversacional, quadro de triagem).
3. **Revisão em paralelo**: o Guardião do estilo checa Carbon e acessibilidade; o Crítico faz o cognitive walkthrough de cada versão com a Camila e o Valdir e preenche a Feedback Grid.
4. **Playback** (Orquestrador): apresenta as três versões lado a lado, com o parecer do Crítico e uma recomendação.
5. **Decisão do Leo** (Sponsor User interno do time): escolhe uma versão ou mistura. Só então a próxima etapa começa, construída sobre a escolha.
6. **Retrospectiva curta**: o que aprendemos, o que muda no próximo ciclo (Restless Reinvention).

## Regras de convivência entre agentes
- Cada agente escreve só nos seus arquivos (ex.: Designer B só mexe em `WF-B-*`); o Orquestrador é o único que publica o canvas, para não haver conflito de versão.
- Toda entrega cita a técnica usada e qual Hill ela atende.
- Decisão de produto é humana: agentes recomendam, o Leo e o time decidem.
- Material visual sempre no guia de estilo IBM (Carbon + IBM Design Language).

## Como estamos aplicando agora
- Rodando em paralelo: **Designer B** e **Designer C** (wireframes das versões B e C) e o **Pesquisador de referências** (skills de Design Thinking, UX e estilo IBM).
- O Orquestrador fez a descoberta (personas, empatia, as-is, Hills) e a versão A, e vai montar o Playback das três versões para a sua escolha.

## Observação
Esta é a arquitetura dos agentes que **desenham** o Watson. A arquitetura dos agentes **dentro do produto** (ex.: agente de risco, agente investigador, agente de contato com o associado) é outro tema; posso propor em seguida se fizer sentido.
