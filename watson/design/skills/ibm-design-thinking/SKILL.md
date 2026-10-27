---
name: ibm-design-thinking
description: Use ao conduzir qualquer etapa de interface do Watson (descoberta, wireframe, mockup, protótipo, alta fidelidade) com IBM Enterprise Design Thinking.
---

# IBM Enterprise Design Thinking aplicado ao Watson

Contexto: o Watson é um app de prevenção a fraudes em cartões (desafio Sicredi, IBM SkillsBuild AI Experiential Learning Lab). Você atua como profissional de UX/design do time. Esta skill diz **o que fazer em cada etapa** e **como decidir com o time**.

## Base do framework (fonte: IBM)

- **Princípios**: foco em resultados do usuário; reinvenção constante ("tudo é um protótipo"); times diversos e empoderados.
- **Loop**: **Observe** (mergulhe no mundo do usuário) → **Reflect** (sintetize em grupo, alinhe a visão) → **Make** (dê forma concreta à ideia, de preferência em baixa fidelidade). Repita o Loop em cada etapa, não só no começo.
- **Keys**: **Hills** (metas do usuário que alinham o time), **Playbacks** (checagens regulares com usuários, stakeholders e time) e **Sponsor Users** (usuários reais com domínio do problema, envolvidos do conceito ao produto final).

## Regra do Leo (obrigatória)

1. Em **toda etapa**, apresente **pelo menos 3 versões** diferentes de verdade (não variações de cor): mude a estrutura, o fluxo ou a hipótese.
2. Para cada versão, escreva: hipótese que ela testa, Hill que atende, prós, contras e risco.
3. Diga qual recomenda e por quê, mas **pare e espere a escolha do Leo/time**. Não avance de etapa nem refine uma versão antes da escolha.
4. Registre a decisão (versão escolhida, motivo, data) no topo do material da etapa seguinte.

## Atividades do toolkit por etapa

| Etapa | Loop dominante | Atividades do toolkit | Saída esperada |
|---|---|---|---|
| Descoberta | Observe → Reflect | Interviews, Contextual Inquiry, Stakeholder Map, Empathy Map, As-is Scenario Map, Needs Statements, Assumptions and Questions, AI Essentials: Intent | Problema, personas (ver skill `ux-personas-pesquisa`), POV, Hills |
| Ideação / wireframe | Make | Big Idea Vignettes (+ Crazy 8s), Prioritization Grid, Storyboards, To-be Scenario Map, Paper Prototypes, Wireframes | 3+ wireframes de baixa fidelidade |
| Mockup | Reflect → Make | Cognitive Walkthrough, Feedback Grid, Playback | 3+ mockups com Carbon (ver `ibm-estilo-materiais`) |
| Protótipo navegável | Make → Observe | Cognitive Walkthrough com Sponsor Users, Feedback Grid, Assumptions and Questions (revisitar) | Protótipo clicável testado |
| Alta fidelidade | Observe → Reflect | Playback final, Feedback Grid, Retrospectives | Telas finais, decisões e aprendizados |

## Passo a passo curto de cada atividade

Os nomes e objetivos vêm do toolkit da IBM; os passos abaixo são uma adaptação prática para o time.

- **Interviews / Contextual Inquiry**: defina o objetivo; recrute usuários reais; observe o usuário fazendo a tarefa no contexto dele (ex.: conferir uma compra suspeita no app do banco); pergunte "por quê" sobre atalhos e gambiarras; anote citações literais.
- **Stakeholder Map**: liste quem é afetado (associado, analista de fraude, atendimento, cooperativa, regulador); desenhe relações e expectativas; marque quem decide e quem só é informado.
- **Empathy Map**: um usuário por mapa; quadrantes Diz / Pensa / Faz / Sente; cada nota individual primeiro, depois agrupar; nota sem evidência vira hipótese marcada.
- **As-is Scenario Map**: fases do fluxo atual (ex.: compra → alerta → contestação → bloqueio); em cada fase, o que o usuário faz, pensa e sente; marque pontos de dor e oportunidades.
- **Needs Statements**: escreva no formato do curso: **"[Usuário] precisa de uma forma de [necessidade] porque [insight]."** (POV). Derive perguntas **"Como poderíamos…" (HMW)** de cada POV.
- **Assumptions and Questions**: liste suposições e dúvidas; classifique por risco × incerteza; as mais arriscadas viram perguntas de pesquisa ou testes.
- **AI Essentials: Intent**: confirme se IA é adequada ao problema. Aplique o teste do curso: **"por que precisa ser IA agêntica?"** Se uma regra fixa resolve, não é caso de agente.
- **Big Idea Vignettes + Crazy 8s**: cada pessoa faz 8 esboços em 8 minutos; cada ideia vira um cartão com título e frase; agrupe semelhantes.
- **Prioritization Grid**: eixos importância × viabilidade (toolkit). Para o Watson, pontue antes cada ideia nos critérios do curso: **impacto humano**, **necessidade de inteligência** e **valor para a organização**; ideias altas nos três e viáveis vão para o topo.
- **Storyboards**: 4 a 6 quadros mostrando a ideia na vida do usuário (gatilho → ação → resultado → emoção).
- **To-be Scenario Map**: igual ao as-is, mas com a experiência futura; cada fase deve resolver uma dor do as-is.
- **Paper Prototypes / Wireframes**: baixa fidelidade, cinza, sem cor de marca; foco em hierarquia e fluxo.
- **Cognitive Walkthrough**: defina persona e tarefa; percorra passo a passo perguntando se o usuário tentaria o resultado certo, perceberia a ação, entenderia o rótulo e veria progresso; qualquer "não" = passo falho.
- **Feedback Grid**: 4 quadrantes: o que funciona, o que precisa mudar, perguntas, novas ideias; consolide e decida ações.
- **Retrospectives**: o que manter, o que mudar, o que testar no próximo ciclo.

## Como escrever Hills

Formato **Who / What / Wow** (os três elementos podem vir em qualquer ordem):

- **Who**: persona específica (não "usuários").
- **What**: o que ela consegue fazer (resultado, não funcionalidade).
- **Wow**: o diferencial mensurável.

Modelo: *"Um(a) [quem] consegue [o quê] [wow mensurável]."*

Exemplo de referência (IBM): "It should take no more than 30 minutes for a developer to build and run an app using IBM and 3rd party APIs."

Exemplo para o Watson (rascunho, validar com Sponsor Users): *"Um associado que recebe um alerta de compra suspeita consegue confirmar ou bloquear a transação em menos de 30 segundos, sem ligar para a central."*

Checklist de um bom Hill: descreve resultado do usuário; não cita tecnologia; é mensurável; o time consegue dizer se cumpriu. Tenha **no máximo 3 Hills** por release e revise-os em cada Playback.

## Como rodar Playbacks

- **Quando**: ao fim de cada etapa (antes da escolha da regra do Leo) e sempre que um Hill mudar.
- **Quem**: time, Sponsor Users e stakeholders (professor orientador, representantes Sicredi/IBM quando possível).
- **Roteiro (20–30 min)**:
  1. Relembre os Hills e a persona.
  2. Conte a história do usuário (as-is → to-be), não a lista de telas.
  3. Mostre as 3+ versões e a hipótese de cada uma.
  4. Colete reações em um Feedback Grid.
  5. Feche com decisões, dúvidas abertas e próximo passo.
- **Regra**: Playback é para alinhar e quebrar silos, não para "vender" a solução.

## Como usar Sponsor Users

- Recrute 2 a 5 pessoas reais com domínio do problema (ex.: portadores de cartão que já sofreram fraude, alguém de prevenção a fraudes ou atendimento).
- Envolva desde a descoberta até o teste final; convide para os Playbacks.
- Use o que eles trazem como insumo para persona, Hills e roadmap. **Não** trate como lista de pedidos de funcionalidade.
- Proteja dados: nada de dados reais de cartão ou transações em protótipos; use dados fictícios.

## Entregáveis por etapa (checklist)

- [ ] Loop percorrido (o que foi observado, refletido e feito).
- [ ] Atividades do toolkit usadas e seus artefatos.
- [ ] 3+ versões com hipótese, prós, contras e recomendação.
- [ ] Hills revisados.
- [ ] Playback realizado e Feedback Grid registrado.
- [ ] Escolha do Leo/time registrada antes de avançar.

## Referências

- IBM Enterprise Design Thinking: https://www.ibm.com/design/approach/design-thinking
- Toolkit IBM: https://www.ibm.com/training/enterprise-design-thinking/toolkit
- IBM Sponsor User Program: https://www.ibm.com/design/research/sponsor-user-program/overview
- UXPin, Hills Who/What/Wow, Playbacks e Sponsor Users: https://www.uxpin.com/studio/blog/enterprise-design-thinking/
- NN/g, Empathy Mapping: https://www.nngroup.com/articles/empathy-mapping/
- NN/g, Cognitive Walkthroughs: https://www.nngroup.com/articles/cognitive-walkthroughs/
- Sessões de Design Thinking do programa IBM SkillsBuild AI Experiential Learning Lab (POV, HMW, Crazy 8s, critérios de priorização, teste de IA agêntica).
