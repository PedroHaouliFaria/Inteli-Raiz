# Registro de Evidências e Hipóteses — Pacote Pessoa 1

**ID do registro:** EH-P1-v0.1
**Versão:** 0.1 · 03/11/2026
**Responsável:** Pessoa 1
**Estado:** rascunho — sem observações de campo; todo conteúdo é documental ou hipotético.

Este arquivo registra **apenas IDs novos** produzidos pela Pessoa 1. Os IDs da Pessoa 2 (`FON-01` a `FON-12`, `HIP-01` a `HIP-09`, `DEC-01` a `DEC-09`) são utilizados por referência em D01, D04, D05, D07 e D08 — consulte `docs/entregas/pessoa2/evidencias_e_hipoteses.md` para o registro completo.

---

## Prefixos de ID

| Prefixo | Tipo |
|---|---|
| `FON-P1-xx` | Fonte documental nova, não registrada pela Pessoa 2 |
| `HIP-P1-xx` | Hipótese nova gerada pela análise de produto/negócios |
| `DEC-P1-xx` | Decisão de produto/narrativa registrada pela Pessoa 1 |

---

## Fontes documentais (novas)

| ID | Origem e localização | Versão / data | Seção relevante | Limite de uso | Entregas relacionadas |
|---|---|---|---|---|---|
| FON-P1-01 | `contexto/2026 AI Experiential Learning Lab with Bob - Industry Challenges_Portuguese.pdf` | PDF local | p.6: desafio Sicredi — "alerta preventivo e confirmação pelo associado"; arquétipos pp.7–10 | Descrição do desafio e arquétipos; não detalha fluxo interno do Sicredi nem confirma demanda de adoção | D01, D08 |
| FON-P1-02 | `docs/entregas/pessoa3/D09_estrutura_solucao.md` | v0.1 · 29/10/2026 | §2 (saber/decidir/fazer), §4 (requisitos R01–R12), §5 (critérios de sucesso) | Rascunho da Pessoa 3; não revisado; PR-AUC documentado = 0,146, meta 0,80 não atingida | D05, D08 |
| FON-P1-03 | `docs/entregas/pessoa3/D10_arquitetura.md` | v0.1 · 29/10/2026 | §4 (ficha do agente), §5 (catálogo de ferramentas), §7 (política e máquina de estados) | Rascunho; componentes em estado "Planejado"; deploy watsonx.ai concluído como evidência, não como runtime | D05, D08 |
| FON-P1-04 | `docs/entregas/pessoa4/D12_prototipo_experiencia.md` | v0.1 · 28/10/2026 | Percurso de confirmação, mapa de telas/estados, textos candidatos | Revisado documentalmente; frontend não integrado à API (PEN-01/PEN-03 da Pessoa 4) | D05, D07 |
| FON-P1-05 | `docs/entregas/pessoa4/D11_fluxo_mvp.md` | v0.1 · 28/10/2026 | Casos P4-T01 a T12, pré-condições e cenários | Rascunho bloqueado por integração; sem execução ponta a ponta verificada | D08 |

---

## Hipóteses (novas — geradas pela análise de produto)

| ID | Descrição | Origem | Estado / limite | Implicação para produto/narrativa | Entregas | Como verificar |
|---|---|---|---|---|---|---|
| HIP-P1-01 | A instituição financeira adotaria o produto se ele reduzisse o esforço de atendimento em casos de dúvida sobre compras | FON-P1-01 (desafio menciona objetivo de reduzir fraudes e melhorar experiência); sem confirmação de interesse da Sicredi | Hipótese de adoção — não confirmada; decisor interno não identificado | Separar "associado usa o produto" de "instituição decide adotar"; não afirmar interesse comercial; registrar como premissa investigável | D08 | Entrevista ou alinhamento com mentor/orientador; benchmarks de volume de chamadas evitadas |
| HIP-P1-02 | A premissa mais frágil da direção escolhida é que o associado compreende a diferença entre recusar a compra e bloquear o cartão inteiro, sem instrução prévia | HIP-01 (Pessoa 2); D02 §3 (tensão central de compreensão) | Hipótese de compreensão — ponto mais arriscado do fluxo de confirmação | Se falsa, toda a proposta de valor muda: precisaríamos de um canal de instrução antes da tela, não do fluxo atual | D04, D08 | Tarefa "não reconheço" com pergunta: "O que aconteceu com seu cartão?" (roteiro D13) |
| HIP-P1-03 | O valor principal para a instituição é a redução de contatos de atendimento por dúvida, não a redução direta de perdas por fraude | FON-P1-01 p.6; plano §2 "hipótese de valor e limite" | Hipótese de valor organizacional — não medida | Em D08, separar "hipótese de redução de atendimento" de "redução de perdas financeiras"; a segunda não é verificável neste MVP | D08 | Comparar número de casos com e sem resolução autônoma no piloto; não extrapolar para perdas financeiras |
| HIP-P1-04 | O custo de IA por confirmação é dominado pelo número de mensagens de chat trocadas por caso — casos sem dúvida contextual (autorização direta) geram custo mínimo | FON-P1-03 §7 (agente só é chamado quando há dúvida contextual); plano §4 (agente com LLM externo) | Hipótese de viabilidade — não calculada; custo por chamada de API não levantado | Construir tabela de premissas com cenário conservador (todas as confirmações geram chat) e base (x% geram chat) | D08 | Instrumentar o piloto para contar mensagens de chat por caso |
| HIP-P1-05 | Uma alternativa sem agente (confirmação com texto fixo) seria suficiente para casos onde o associado reconhece imediatamente a compra, mas insuficiente para o caso de nome de estabelecimento ambíguo | D02 §3 (tensão de reconhecimento); D03 §4 (ruptura: canal incerto + informação insuficiente); D10 §4 (ficha do agente) | Hipótese comparativa — sustenta a justificativa de necessidade de IA em D04/D08 | O agente deve demonstrar valor exatamente no caso ambíguo; se o piloto mostrar que o texto fixo resolve bem, essa hipótese cai e a justificativa de IA precisa ser revisada | D04, D08 | Alternância de fluxo básico × agente no piloto (D13) |

---

## Decisões de produto (Pessoa 1)

| ID | Descrição | Fonte / regra que motivou | Efeito nos artefatos |
|---|---|---|---|
| DEC-P1-01 | O recorte de D01 é confirmação de compras pelo associado — não prevenção completa de fraudes, não mesa de análise | FON-01 §1 (mudança de produto); FON-P1-01 p.6 (desafio Sicredi) | D01 não inclui detecção em tempo real nem bloqueio automático como entregáveis do MVP |
| DEC-P1-02 | A direção vencedora em D04 é Alternativa B (ajuda contextual com agente), como revisão da decisão já tomada no plano; registrada com a mesma base de critérios que avalia as alternativas A e C | FON-01 §2 e §8.1 (escolha já no plano); direcional §D04 ("registrar como revisão da decisão se a discussão ocorrer depois") | D04 registra a decisão como revisão, não como resultado de brainstorming executado; a seção de discussão em grupo fica como roteiro pendente |
| DEC-P1-03 | Em D08, o valor das transações sinalizadas não é tratado como perda evitada; os números de premissas ficam marcados como `[a definir]` até que haja fonte verificável | Plano §9 ("valor das transações sinalizadas não equivale a perdas evitadas"); direcional §D08 | D08 não afirma redução de perdas; usa hipóteses mensuráveis com fonte explícita ou marcação `[a definir]` |
| DEC-P1-04 | Os arquétipos do desafio (especialista sensível ao contexto; gestor da fronteira humano–IA) são tratados como interpretação candidata, não como classificação definitiva | FON-P1-01 pp.7–10 (arquétipos); direcional §D08 ("marcar como interpretação a confirmar pelo comportamento executado") | D08 apresenta os arquétipos com explicitação de que são interpretações a confirmar |
