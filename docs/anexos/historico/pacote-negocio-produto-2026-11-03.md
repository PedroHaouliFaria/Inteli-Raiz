> **Registro histórico de 03/11/2026, preservado na integração de 05/11.** Origem: develop `9d54d1a`, `docs/entregas/pessoa1/README.md`. Estados, caminhos e divergências abaixo pertencem à versão antiga e não são o estado atual. Consulte a [documentação principal](../../documentacao-do-projeto.md) e as [pendências atuais](../gestao/o-que-falta-concluir.md).

# Pacote Pessoa 1 — Negócios, produto e narrativa

**Versão:** 0.1 · **Data:** 03/11/2026
**Responsável:** Pessoa 1
**Revisores:** Pessoa 2 (D01/D05), Pessoa 3 (D04/D08), Pessoa 4 (D07)
**Branch de trabalho:** `docs/pessoa1-negocio-produto` (criada a partir de `develop`)
**Estado geral:** rascunho — sem pesquisa com usuários executada; D04 aguarda brainstorming do grupo; D07 aguarda teste do pitch; Canvas de Proposta de Valor (D07-canvas) criado em 03/11/2026.

---

## 1. Índice de arquivos

| Arquivo | Entregas | Estado |
|---|---|---|
| `README.md` (este arquivo) | Índice, pendências, rastreabilidade e instruções de exportação | rascunho |
| `evidencias_e_hipoteses_p1.md` | Registro de fontes e hipóteses novas da Pessoa 1 | rascunho |
| `D01_oportunidades.md` | D01 — Oportunidades de segurança e clareza | rascunho |
| `D04_priorizacao.md` | D04 — Alternativas e decisão de prioridade | rascunho |
| `D05_D07_D08_conceito_valor.md` | D05 — Conceito · D07 — Ideia · D08 — Proposta de valor/IA | rascunho |
| `canvas_proposta_de_valor.md` | Canvas de Proposta de Valor (Osterwalder) — encaixe perfil × mapa de valor | rascunho |

---

## 2. Responsabilidades conforme o direcional

Conforme [guia de entregas atual](../gestao/guia-das-entregas.md#responsáveis-sequência-e-revisão):

| Entrega | Responsável | Apoio necessário | Revisor principal | Saída para aceite |
|---|---|---|---|---|
| D01 Oportunidades | Pessoa 1 | Pessoa 2: pesquisa e fontes | Pessoa 2 | Fricção, evidências, lacunas e HMW/POV |
| D04 Priorização | Pessoa 1 | As quatro pessoas: alternativas; Pessoa 3: viabilidade | Pessoa 3 | Matriz comparável e justificativa da direção escolhida |
| D05 Conceito | Pessoa 1 | Pessoa 3: capacidades e limites | Pessoa 2 | Conceito compreensível e cenário de uso |
| D07 Ideia e Descrição | Pessoa 1 | Pessoa 2: linguagem do usuário | Pessoa 4 | Descrição curta coerente com conceito e fluxo |
| D08 Valor e IA | Pessoa 1 | Pessoa 3: inteligência/custos; Pessoa 2: dor/evidência | Pessoa 3 | Uma página com valor, adoção, justificativa de IA e premissas |

---

## 3. Estado de cada entrega

| Entrega | Estado | Justificativa |
|---|---|---|
| **D01** Oportunidades | rascunho | Contexto, atores, 8 evidências/hipóteses, 6 necessidades, 4 oportunidades, POV, 4 HMWs e 4 hipóteses mais arriscadas documentados. Sem pesquisa com usuários executada; toda afirmação de dor ou comportamento aponta para FON/HIP. |
| **D04** Priorização | rascunho | Três alternativas comparadas com matriz de 5 critérios; direção B (agente) selecionada como revisão da decisão já no plano. Brainstorming em grupo não executado — seção 3 é roteiro pendente. |
| **D05** Conceito | rascunho | Solução em uma frase, experiência em 3 momentos (incluindo caso sem resposta do agente), papel do agente, limites e dependências documentados. Aguarda revisão da Pessoa 2 para alinhar com D06. |
| **D07** Ideia | rascunho | Ficha completa, pitch de 30 s e mini-roteiro de teste da explicação prontos. Teste do pitch não executado. |
| **D08** Proposta de valor | rascunho | Tabela completa, comparação A×B, decomposição saber/decidir/fazer, premissas com `[a definir]` explícitos e separação de métricas do protótipo × efeitos operacionais. Será atualizado após D13. |

---

## 4. Pendências e responsáveis

### Pendências internas (Pessoa 1)

| ID | Descrição | Prioridade | Estado |
|---|---|---|---|
| PEN-P1-01 | Executar teste do pitch de D07 com alguém de fora do grupo (mini-roteiro em D07 §3) | P1 | Pendente |
| PEN-P1-02 | Facilitar discussão em grupo para D04 (roteiro em D04 §3) após a equipe ter tempo | P1 | Pendente |
| PEN-P1-03 | Atualizar D08 após D13: substituir hipóteses por resultados reais; atualizar justificativa de IA se piloto inverter HIP-P1-05 | P2 — depende de D13 | Pendente |
| PEN-P1-04 | Preencher campos `[a definir]` das premissas de viabilidade (D08 §4) com dados reais da instituição quando disponíveis | P2 | Pendente |

### Pendências para outras pessoas

| ID | Para quem | Descrição | Por que importa para P1 | Prioridade |
|---|---|---|---|---|
| PEN-P1-05 | **Pessoa 2** | Revisar D01 para confirmar se as necessidades N1–N6 estão alinhadas com D02/D03; sinalizar qualquer dor prioritária não coberta | D01 alimenta D04 e D08; discrepância muda a prioridade das oportunidades | P1 |
| PEN-P1-06 | **Pessoa 2** | Revisar D05 para confirmar coerência com D06 (cenários e textos de resposta); sinalizar divergência de linguagem ou de consequência das respostas | D05 e D06 precisam descrever a mesma experiência | P1 |
| PEN-P1-07 | **Pessoa 3** | Revisar D04 §4 (viabilidade técnica de B); confirmar se a avaliação de "Média viabilidade" para o agente está correta dado o estado atual do PEN-04/PEN-05 da Pessoa 4 | D04 registra premissas que a Pessoa 3 tem mais contexto para avaliar | P1 |
| PEN-P1-08 | **Pessoa 3** | Revisar D08 §2 (por que IA) e §4 (premissas); confirmar se decomposição saber/decidir/fazer está coerente com D09/D10 | D08 deve refletir a arquitetura real, não uma versão idealizada | P1 |
| PEN-P1-09 | **Pessoa 4** | Revisar D07 para confirmar coerência com D11/D12; sinalizar se o pitch descreve capacidades não implementadas ou omite o que está implementado | D07 não pode descrever um produto diferente do que está em D11/D12 | P1 |
| PEN-P1-10 | **Pessoa 3** | Após revisão de D05/D08, atualizar D09 para fechar a **PEN-P3-01** (escopo e proposta de valor bloqueada por D05/D07/D08 da Pessoa 1) | D09 declarava dependência de D05/D07/D08; agora esses documentos existem | P2 |
| PEN-D07-01 | **Leonardo / Pessoa 4** | Frontend atual tem dois botões + biometria (PEN-01 da Pessoa 4); D07 descreve três respostas + sem biometria. Alinhar a UI com o que D07 descreve | D07 e D12 precisam descrever a mesma interface | P0 |

---

## 5. Versões consultadas

| Fonte | Local | Hash / versão | Observação |
|---|---|---|---|
| Plano de implementação | `docs/plano_implementacao.md` | v2.3 · 28/10/2026 | Fonte principal de produto |
| Direcional das entregas | `docs/direcional_entregas.md` | v1 · 27/10/2026 | Governa estrutura e critérios |
| Backlog | `artifacts/planejamento/backlog.md` | 28/10/2026 | Cards C01/C02/C08/C19/C23/C30 |
| Plano operacional | `artifacts/planejamento/plano_15_dias.md` | 28/10/2026 | Sequência e critérios de passagem |
| Pessoa 2 — evidências e hipóteses | `docs/entregas/pessoa2/evidencias_e_hipoteses.md` | v0.1 · 28/10/2026 | FON-01 a 12, HIP-01 a 09, DEC-01 a 09 |
| Pessoa 2 — D02/D03/D06 | `docs/entregas/pessoa2/` | v0.1 · 28/10/2026 | Necessidades, cenário de ruptura e persona |
| Pessoa 3 — D09/D10 | `docs/entregas/pessoa3/` | v0.1 · 29/10/2026 | Capacidades do agente, requisitos, arquitetura |
| Pessoa 4 — D11/D12 | `docs/entregas/pessoa4/` | v0.1 · 28/10/2026 | Fluxo do MVP e protótipo; PEN-01/03/04 |
| Desafio Sicredi | `contexto/2026 AI Experiential...pdf` | PDF local | p.6 e arquétipos pp.7–10 |

---

## 6. Matriz de rastreabilidade (Pessoa 1)

| Evidência / hipótese | Necessidade (D01) | Decisão | Requisito do plano | Como verificar | Resultado / versão |
|---|---|---|---|---|---|
| HIP-P1-05: texto fixo insuficiente para nome ambíguo | N1 — entender a compra com nome ambíguo | DEC-P1-02: B (agente) sobre A (texto fixo) | R08 — dúvida contextual | Alternância fluxo básico × agente no piloto D13 | Pendente |
| HIP-P1-02: compreensão de recusa × bloqueio do cartão é a premissa mais frágil | N3 — saber o efeito de cada resposta | DEC: texto de resultado explícito obrigatório | R03, R11 | Tarefa "não reconheço" + pergunta de compreensão (roteiro D13) | Pendente |
| HIP-01 (P2): confundir recusa com bloqueio | N3 | DEC (P2 DEC-04): não prometer bloqueio automático | R03, R11 | Mesma tarefa acima | Pendente |
| HIP-03 (P2): nome do estabelecimento irreconhecível | N1 | DEC-09 (P2): informar limite; não inventar | R07, R08 | Caso com nome ambíguo no piloto: "O que o sistema sabe e o que não sabe?" | Pendente |
| HIP-P1-01: adoção pela instituição depende de redução de atendimento | — | DEC-P1-03: não afirmar interesse comercial; marcar como premissa investigável | — | Conversa com mentor/orientador; benchmarks operacionais | Pendente |

---

## 7. Divergências encontradas (não corrigi arquivos de outras pessoas)

| # | Divergência | Arquivos envolvidos | Como registrei |
|---|---|---|---|
| 1 | D09 §3 sugere modelo "treinado e avaliado"; plano §7 lista pendências críticas antes de apresentar resultados; D10 §11 marca modelo como "A serializar" | `docs/entregas/pessoa3/D09_estrutura_solucao.md`, `docs/plano_implementacao.md` §7, `docs/entregas/pessoa3/D10_arquitetura.md` §11 | Registrado em D05 §7 (limites) e D08 §5; PEN-P1-10 orienta revisão de D09 pela Pessoa 3 |
| 2 | Frontend atual (PEN-01 da Pessoa 4): dois botões + biometria vs. três respostas + sem biometria descrito em D07 | `docs/entregas/pessoa4/README.md` PEN-01, `docs/entregas/pessoa1/D05_D07_D08_conceito_valor.md` D07 §4 | PEN-D07-01 acima; Pessoa 4 e Leonardo são responsáveis |
| 3 | PR-AUC 0,146 documentado em D09 §5 como resultado real; D08 não pode usar essa métrica como argumento de valor | `docs/entregas/pessoa3/D09_estrutura_solucao.md` §5 | D08 §5 separa explicitamente métricas do protótipo de efeitos operacionais; DEC-P1-03 |

---

## 8. Checklist final

- [x] Seis arquivos criados com cabeçalho completo e estado "rascunho"
- [x] Nenhuma fala, número ou resultado inventado; toda afirmação relevante tem ID (FON/HIP/DEC)
- [x] D04 compara ≥3 alternativas, incluindo uma sem agente (A: texto fixo), com os mesmos critérios
- [x] D05 inclui caso em que o agente não sabe responder e encaminha para revisão (D05 §5 Cenário C)
- [x] D07 tem versão de 30 segundos coerente com D05 e com o fluxo; nota sobre "30s = pitch, não meta de uso"
- [x] D08 responde "por que um agente?" e "por que alguém adotaria?", com premissas e `[a definir]` explícitos
- [x] Pendências para Pessoas 2, 3 e 4 registradas (PEN-P1-05 a PEN-D07-01)
- [x] Nenhum arquivo de outra pessoa foi alterado

---

## 9. Próximos passos

1. **Pessoa 2 revisa D01 e D05** (PEN-P1-05 e PEN-P1-06) — confirma coerência com D02/D03/D06.
2. **Pessoa 3 revisa D04 e D08** (PEN-P1-07 e PEN-P1-08) — fecha a PEN-P3-01.
3. **Pessoa 4 revisa D07** (PEN-P1-09) — confirma coerência com D11/D12.
4. **Pessoa 1 facilita discussão de D04 em grupo** (PEN-P1-02) — com as quatro pessoas; atualiza seção 3.
5. **Pessoa 1 testa o pitch de D07** (PEN-P1-01) — mini-roteiro em D07 §3.
6. **Após D13:** Pessoa 1 atualiza D08 com resultados reais (PEN-P1-03) e fecha a narrativa (C30).

---

## 10. Exportação das sessões do Bob

Para exportar capturas desta tarefa: abrir Tasks no Bob IDE → selecionar a tarefa → abrir o resumo no cabeçalho → capturar as sessões relevantes. Salvar em `bob_sessions/<seu_nome>/`. Não criar imagens que simulem evidências de uso do Bob; o resumo da tarefa é a evidência principal, conforme Guia IBM pp.30–31 (FON-12).
