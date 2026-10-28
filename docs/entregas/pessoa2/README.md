# Pacote Pessoa 2 — Pesquisa e compreensão do associado

**Versão 0.1 · Rascunho para revisão · 28/10/2026**  
**Responsável:** Pessoa 2  
**Revisor geral:** Pessoa 1 (D02/D06), Pessoa 4 (D03)  
**Estado:** rascunho — pesquisa com usuários ainda não executada; validação pendente.

---

## 1. O que este pacote contém

Este diretório reúne as entregas D02, D03 e D06 sob responsabilidade da Pessoa 2, conforme o [Direcional de Entregas](../../direcional_entregas.md) e a [matriz de quatro pessoas](../../direcional_entregas.md#organização-em-quatro-pessoas-responsáveis-sequência-e-revisão). Inclui também o roteiro de pesquisa para uso posterior e o registro de evidências e hipóteses que sustenta os três documentos.

| Arquivo | Entrega | Estado | Revisor principal |
|---|---|---|---|
| `evidencias_e_hipoteses.md` | Registro de fontes, hipóteses e decisões (todos os artefatos) | Rascunho | Pessoa 1 |
| `D02_mapa_empatia.md` | D02 — Mapa de Empatia do associado | Rascunho | Pessoa 1 |
| `D03_cenario_atual.md` | D03 — Cenário Atual: do alerta à resolução da dúvida | Rascunho | Pessoa 4 |
| `D06_persona_e_cenarios.md` | D06 — Persona funcional e cenários atual/futuro | Rascunho | Pessoa 1 |
| `roteiro_pesquisa.md` | Roteiro de entrevista, compreensão e registro — uso posterior | Pronto para uso | Pessoa 2 |

---

## 2. Origem e aproveitamento do trabalho do Leonardo

O conteúdo de base foi produzido por **Leonardo** na branch `origin/watson` (hash `212655c`), nos arquivos:

- `docs/design/00-descoberta/personas.md`
- `docs/design/00-descoberta/mapas-de-empatia.md`
- `docs/design/00-descoberta/cenario-as-is.md`
- `docs/design/00-descoberta/premissas-e-perguntas.md`
- `docs/design/00-descoberta/hills-e-pov.md`
- `docs/design/00-descoberta/anti-persona.md`

Esses arquivos **permanecem intactos** nesta tarefa. Os documentos aqui produzidos reaproveitam, reconhecem e reveem hipóteses da base, sem sobrescrever os originais.

### Auditoria de ajustes — o que mudou e por quê

| Trecho / arquivo de origem | Aproveitado como | Ajuste necessário | Motivo / fonte | Entrega afetada |
|---|---|---|---|---|
| `personas.md`: Valdir como Persona 2 (associado), Camila como Persona 1 (analista) | Valdir → protagonista; Camila → ator secundário de exceções | Inversão de foco: Camila saiu do centro | Plano §1; Direcional §D06; PR #8 | D02, D03, D06 |
| `mapas-de-empatia.md`: mapa da Camila com 4 quadrantes | Descartado como entrega principal deste pacote | Analista não é o usuário prioritário nesta revisão | Plano §1; Direcional §D02 | D02 |
| `mapas-de-empatia.md`: mapa do Valdir com 4 quadrantes | Aproveitado como ponto de partida do D02 | Ampliado: dúvida sobre consequência das respostas; pedido de atendimento; três respostas distintas; expiração | Plano §3 (AUTHORIZE/DENY/UNSURE/ajuda separada); PR #8 | D02 |
| `personas.md`: dois botões ("Fui eu" / "Não reconheço") | Não transportado | Plano vigente define três respostas + ajuda separada | Plano §§1–3; alinhamento 28/10 (decisão 3) | D02, D06 |
| `personas.md` e `anti-persona.md`: biometria obrigatória em "Fui eu" no alto risco | Registrado como hipótese descartada do MVP | Biometria e aparelho novo saíram do recorte MVP | Plano §4 alinhamento decisão 4 | D06 |
| `personas.md`: "novo cartão", "nada foi cobrado" como estado de sucesso do Valdir | Não transportado | Promessas operacionais fora do escopo do MVP | Plano §5 e §3: "Não bloquear cartão inteiro automaticamente" | D02, D06 |
| `cenario-as-is.md`: jornada do Valdir em 5 etapas (bloqueio → ligação → central → novo cartão) | Aproveitado como cenário hipotético de referência, com marcação de status | Não apresentar como jornada universal; separar do cenário futuro | Plano §9; Direcional §D03 | D03 |
| `hills-e-pov.md`: metas "30 segundos" e "2 minutos" | Registradas como metas propostas, não resultados observados | Proibido tratar meta de Hill como resultado medido | Plano §7; Direcional §D03 | D03, D06 |
| `hills-e-pov.md`: POV para Camila e Valdir | POV do Valdir aproveitado; POV da Camila não transportado | Foco no associado | Direcional §D06 | D06 |
| `premissas-e-perguntas.md`: premissas com certeza "baixa" e "média" | Convertidas para HIP-xx no registro de hipóteses | Certeza "média" não é evidência; preserva o rigor | Direcional: regras comuns; Plano §7 | Todos |
| `anti-persona.md` | Não transportado para este pacote | O impostor não é persona do associado; relevante para segurança, não para empatia | Escopo deste pacote (D02/D03/D06) | — |

---

## 3. Estado de cada entrega

| Entrega | Fontes utilizadas | Pesquisa ainda necessária | Bloqueios |
|---|---|---|---|
| D02 — Mapa de Empatia | Personas e mapa do Leonardo (watson `212655c`); plano vigente §§1–3; direcional D02 | Entrevista com 2–3 associados para validar hipóteses de confiança, reconhecimento e compreensão das respostas | Nenhum para o rascunho |
| D03 — Cenário Atual | Cenário as-is do Leonardo; plano §9; direcional D03 | Entrevista com associado ou especialista do domínio para confirmar canais, tempos e etapas | Cenário hipotético; tempos e canais não confirmados |
| D06 — Persona e Cenários | Personas do Leonardo; plano §§1–5; direcional D06 | Validação do perfil funcional; teste de compreensão dos seis cenários | Nenhum para o rascunho |
| Roteiro de pesquisa | Premissas do Leonardo; perguntas do plano §9; direcional D13 | Execução da pesquisa pela Pessoa 2 | Sem protótipo disponível para bloco de compreensão no momento |

---

## 4. Pendências e responsáveis

| Pendência | Impacto | Responsável sugerido | Prioridade |
|---|---|---|---|
| Validar hipóteses HIP-01 a HIP-09 com entrevistas de descoberta | D02, D03, D06 podem conter premissas falsas que mudariam decisões de experiência | Pessoa 2 (execução da pesquisa) | Alta |
| Confirmar se protótipo ou tela do Leonardo está acessível para bloco de compreensão do roteiro | Sem protótipo, o bloco de compreensão não pode ser executado | Pessoa 4 (D12) + Leonardo | Alta |
| Revisar D02 e D06 com Pessoa 1 após pesquisa | Alinhamento entre necessidades do usuário e proposta de valor | Pessoa 1 (revisão) | Média |
| Verificar alinhamento dos textos de D06 (cenário futuro) com o frontend Watson adaptado (C10/C13) | Incoerência entre experiência descrita e interface implementada | Pessoa 4 + Leonardo | Média |
| Atualizar links para imagens do Leonardo quando branches forem integradas | Imagens estão em `origin/watson` e não nesta branch | Pessoa 2 (após integração) | Baixa |

---

## 5. Hashes e versões consultadas

| Fonte | Branch / local | Hash consultado |
|---|---|---|
| Plano vigente e Direcional | `origin/develop` | `8942cc5` |
| Personas, mapas, cenário as-is do Leonardo | `origin/watson` | `212655c` |
| Backlog e artefatos de contexto | `origin/develop` | `8942cc5` |

Branch de trabalho deste pacote: `docs/pessoa2-pesquisa-associado`, criada a partir de `origin/develop` (`8942cc5`).

---

## 6. Instruções para o revisor

1. Ler `evidencias_e_hipoteses.md` antes dos três documentos principais: ele estabelece os IDs de rastreabilidade.
2. Para cada afirmação em D02/D03/D06, verificar se há um ID (`HIP-xx`, `FON-xx`, `DEC-xx`) referenciado.
3. Sinalizar qualquer afirmação que pareça certeza sem fonte, tempo medido ou resultado inventado.
4. Não marcar como "validado" nenhum item até que a pesquisa com usuários seja executada.
5. Consultar `roteiro_pesquisa.md` para ver quais perguntas ainda precisam de resposta.

---

## 7. Exportação das sessões do Bob

Para exportar capturas desta tarefa: abrir Tasks no Bob IDE, selecionar a tarefa, abrir o resumo no cabeçalho e capturar as sessões relevantes. Salvar em `bob_sessions/<seu_nome>/`. Não criar imagens que simulem evidências de uso do Bob; o resumo da tarefa é a evidência principal.
