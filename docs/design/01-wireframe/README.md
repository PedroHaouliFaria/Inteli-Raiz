# 01 · Wireframe (Make, baixa fidelidade)

## Técnicas aplicadas
1. **Big Idea Vignettes** (toolkit IBM): geramos ideias rápidas a partir dos Hills.
2. **Prioritization Grid**: impacto humano × viabilidade, com o critério extra do curso "necessidade de inteligência" (raciocínio, autonomia, coordenação).
3. **To-be Scenario Map**: as três versões abaixo são três to-be diferentes para o mesmo fluxo.
4. **Wireframes** em escala de cinza, com anotações numeradas, para discutir estrutura antes de cor.
5. **Playback 1**: apresentação das 3 versões ao Leo para escolha.

## Big ideas e priorização
| Ideia | Impacto humano | Viabilidade no MVP | Precisa de IA? | Decisão |
|---|---|---|---|---|
| Fila priorizada por risco × valor | Alto | Alta | Sim (score do modelo) | Entra |
| Fatores explicáveis do risco | Alto | Alta | Sim (explicabilidade) | Entra |
| Recomendação do agente com confiança | Alto | Média | Sim (raciocínio) | Entra |
| Alerta "Foi você?" no app | Alto | Média | Sim (coordenação) | Entra |
| Justificativa gerada para auditoria | Médio | Alta | Sim (LLM) | Entra |
| Agrupar alertas do mesmo cartão | Médio | Média | Sim | Versão C |
| Chat com o agente sobre o caso | Médio | Média | Sim | Versão B |
| Monitoramento do modelo (drift, PR-AUC) | Médio | Média | Sim | Depois do MVP |

## As três versões
| | Console da Camila | App do Valdir | Hipótese |
|---|---|---|---|
| **A · Tela dividida** | Fila à esquerda, caso à direita, tudo numa tela | Alerta direto com dados e dois botões | Velocidade: menos cliques por decisão (Hill 1) |
| **B · Agente lateral** | Caso em página, painel "Pergunte ao Watson" ao lado | Alerta em formato de conversa | Confiança: o agente explica e redige junto com a analista |
| **C · Quadro de risco** | Kanban por estado, agente agrupa alertas, painel lateral | Alerta com contexto e mini mapa | Volume: triagem de muitos alertas e rajadas de uma vez |

Ver o canvas, página **01 Wireframe (3 versões)**.
