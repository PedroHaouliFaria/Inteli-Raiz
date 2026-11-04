# Canvas de Proposta de Valor — Confirmação assistida de compras

**ID:** apoio a D08 · **Versão:** 0.2 · **Data:** 04/11/2026\
**Responsável:** Produto · **Revisor:** Arquitetura · **Estado:** rascunho — nenhuma hipótese validada com usuários reais; todo conteúdo baseia-se em documentação interna e hipóteses registradas\
**Origem:** [D01](D01_oportunidades.md), [D02](../02_ux_design/D02_mapa_empatia.md), [D04](D04_priorizacao.md), [D05](D05_conceito_solucao.md), [D06](../02_ux_design/D06_persona_e_cenarios.md), [D08](D08_proposta_valor_ia.md), [registro de evidências](../05_gestao/evidencias_e_hipoteses.md) e [plano](../05_gestao/plano_implementacao.md)

> Este canvas não é uma entrega própria das aulas: ele organiza, no formato de Osterwalder, o encaixe entre o associado e a solução, e alimenta a proposta de valor de [D08](D08_proposta_valor_ia.md). Se divergirem, vale o D08.

---

## 1. Introdução

Este canvas mapeia o encaixe entre o **perfil do cliente** (dores, ganhos e tarefas do associado diante de uma compra sinalizada) e o **mapa de valor** da solução proposta (aliviadores, criadores de ganho e produtos/serviços). O segmento é restrito ao associado que recebe um alerta e precisa confirmar ou contestar a compra — o analista de fraudes aparece apenas onde a jornada do associado depende de revisão de exceções.

> **Marcação de estado:** as hipóteses listadas não foram verificadas com usuários reais. Cada item cita o ID de evidência ou hipótese que o sustenta.

---

## 2. Diagrama — estrutura do canvas

```
┌─────────────────────────────────┬──────────────────────────────────────────┐
│         MAPA DE VALOR           │           PERFIL DO CLIENTE               │
│                                 │                                           │
│  ┌───────────────────────────┐  │  ┌────────────────────────────────────┐   │
│  │   Produtos e serviços     │  │  │         Tarefas do cliente         │   │
│  │  (o que a solução faz)    │  │  │     (o que o associado quer fazer) │   │
│  └───────────────────────────┘  │  └────────────────────────────────────┘   │
│                                 │                                           │
│  ┌───────────────────────────┐  │  ┌────────────────────────────────────┐   │
│  │   Aliviadores de dor      │  │  │         Dores                      │   │
│  │  (como resolve os bloqueios)│ │  │    (o que bloqueia ou irrita)      │   │
│  └───────────────────────────┘  │  └────────────────────────────────────┘   │
│                                 │                                           │
│  ┌───────────────────────────┐  │  ┌────────────────────────────────────┐   │
│  │   Criadores de ganho      │  │  │         Ganhos esperados           │   │
│  │  (como amplifica o valor) │  │  │    (o que o associado valoriza)    │   │
│  └───────────────────────────┘  │  └────────────────────────────────────┘   │
│                                 │                                           │
└─────────────────────────────────┴──────────────────────────────────────────┘
```

---

## 3. Segmento de clientes

**Quem:** Associado de cooperativa de crédito que recebe, de forma inesperada, um alerta no aplicativo sobre uma compra sinalizada e precisa confirmar, contestar ou pedir ajuda — sem ligar para ninguém.

**Referência:** protopersona Valdir (D06 §1); FON-04; FON-P1-01 p.6.

**Fora do escopo deste canvas:** analista de fraudes, mesa de análise, detecção em tempo real, bloqueio automático de cartão (DEC-P1-01).

---

## 4. Perfil do cliente

### 4.1 Tarefas que o associado quer realizar

| # | Tarefa | Fonte |
|---|---|---|
| T1 | Entender o que está sendo confirmado (valor, estabelecimento, data) antes de responder | FON-04; HIP-03 |
| T2 | Confirmar, contestar ou declarar dúvida sobre a compra, com consciência do efeito de cada resposta | HIP-01; HIP-05 |
| T3 | Pedir ajuda de um atendente sem perder a janela de resposta | HIP-07; DEC-05 |
| T4 | Saber o que aconteceu depois de responder (desfecho) | HIP-09 |

### 4.2 Dores (ordenadas por impacto estimado)

| # | Dor | Fonte | Notas |
|---|---|---|---|
| ⭐ D1 | Não consegue distinguir se o canal de alerta é legítimo ou golpe | HIP-04; FON-06 | Mais alta: paralisa qualquer ação antes mesmo de começar |
| ⭐ D2 | Não sabe o que cada resposta faz ao cartão — teme bloquear o cartão inteiro ao contestar | HIP-01; HIP-P1-02 | Segunda mais crítica: risco de resposta errada por medo de consequência |
| D3 | Nome do estabelecimento é ambíguo ou desconhecido; sem contexto extra para reconhecer | HIP-03; HIP-P1-05 | Comum em compras online e franquias com nome técnico |
| D4 | Não sabe se pode responder à compra depois de pedir ajuda — teme perder a janela | HIP-02; DEC-05 | Risco de abandono do fluxo ao perceber que o prazo corre |
| D5 | Não recebe retorno claro do desfecho — não sabe se a compra foi liberada ou o cartão bloqueado | HIP-09; HIP-01 | Incerteza pós-resposta gera nova ligação para a central |

### 4.3 Ganhos esperados (ordenados por importância)

| # | Ganho | Fonte | Notas |
|---|---|---|---|
| ⭐ G1 | Resolver a confirmação completamente dentro do app, sem precisar ligar | HIP-07; FON-04 | Mais valorizado: evitar espera na central |
| ⭐ G2 | Saber, antes de escolher, o que cada resposta faz — sem surpresas depois | HIP-01; HIP-05 | Segundo mais crítico: decisão informada |
| G3 | Não ser prejudicado por uma compra legítima que apenas parecia suspeita | HIP-05; DEC-04 | Não ter o cartão bloqueado por compra ambígua |
| G4 | Confiar que o alerta veio do app do banco, não de golpista | HIP-04; FON-06 | Confiança no canal como pré-condição de uso |

---

## 5. Mapa de valor

### 5.1 Produtos e serviços

| # | O que a solução entrega | Tipo | Fonte |
|---|---|---|---|
| S1 | Tela de confirmação no app autenticado com dados da compra (estabelecimento disponível, valor, data, cartão parcial) | Texto fixo | FON-P1-03 §4; R02 |
| S2 | Três opções de resposta com descrição breve do efeito: Autorizo · Não reconheço · Estou em dúvida | Texto fixo | DEC-07; R03 |
| S3 | Agente de IA conversacional para dúvidas contextuais sobre o estabelecimento ou as opções | **IA (agente)** | FON-P1-03 §4; HIP-P1-05 |
| S4 | Tela de desfecho com status da compra (não do cartão), estado e próximo passo | Texto fixo | HIP-09; R02 |
| S5 | Ação separada "Quero falar com alguém" que abre revisão sem registrar resposta e sem encerrar o prazo | Texto fixo | DEC-05; R08 |

> **Distinção importante:** S1, S2, S4 e S5 são fluxo de texto fixo e funcionam sem o agente. S3 é o diferencial de IA — ativado apenas quando o associado tem dúvida contextual sobre o estabelecimento (HIP-P1-05).

### 5.2 Aliviadores de dor

| Dor aliviada | Aliviador | Como | Fonte |
|---|---|---|---|
| D1 — canal suspeito | A1: Tela aparece no app autenticado; aviso explícito: nenhuma resposta é pedida por telefone | Confiança do canal é estabelecida antes da pergunta | HIP-04; R11 |
| D2 — medo de bloquear o cartão | A2: Cada botão de resposta tem breve descrição do efeito; tela de resultado diz "A compra foi recusada. Seu cartão não foi bloqueado." | Texto específico de desfecho (DEC-04) | HIP-01; HIP-P1-02; R11 |
| D3 — estabelecimento ambíguo | A3: Agente mostra o contexto disponível; quando não há vínculo verificável, declara o limite explicitamente antes de qualquer botão | O agente informa o que sabe e o que não sabe; não inventa | HIP-03; HIP-P1-05; DEC-09 |
| D4 — perder a janela ao pedir ajuda | A4: Status da confirmação permanece visível ao pedir atendimento: "Sua compra ainda aguarda uma resposta (válida até [horário])" | Separação visual de dois caminhos (DEC-05) | HIP-02; R08 |
| D5 — desfecho invisível | A5: Tela de resultado com status e próximo passo após qualquer resposta | Retorno imediato pós-interação | HIP-09; R02 |

### 5.3 Criadores de ganho

| Ganho criado | Criador | Como | Fonte |
|---|---|---|---|
| G1 — resolver sem ligar | C1: Fluxo completo no app — confirmar, contestar, declarar dúvida e pedir atendimento sem sair do app | Jornada fechada no canal digital | HIP-07; R02 |
| G2 — decisão informada | C2: Descrição do efeito junto a cada botão + confirmação de resultado | Transparência antes e depois da ação | HIP-01; HIP-05; R03 |
| G3 — cartão não bloqueado sem necessidade | C3: Recusa da compra não bloqueia o cartão; bloqueio só ocorre por ação do analista (fora do MVP) | DEC-04: protótipo não bloqueia automaticamente | DEC-04; R11 |
| G4 — confiança no canal | C4: Identificação visual do app autenticado + aviso anti-golpe | Canal verificável antes da resposta | HIP-04; R11 |

---

## 6. Encaixe

| Elemento do perfil | Elemento do mapa de valor | Tipo de encaixe |
|---|---|---|
| T1 — entender a compra | S1 (dados) + A3 (agente para ambiguidade) | Informação antes da ação |
| T2 — responder com consciência | S2 (3 opções + efeito) + A2 (texto de desfecho) + C2 (descrição prévia) | Decisão informada |
| T3 — pedir ajuda sem perder janela | S5 (ação separada) + A4 (status visível) | Caminho paralelo ao fluxo |
| T4 — saber o desfecho | S4 (tela de resultado) + A5 (status e próximo passo) | Retorno pós-interação |
| D1 — canal suspeito | A1 (app autenticado + aviso) + C4 (identificação visual) | Confiança do canal |
| D2 — medo de bloquear cartão | A2 (texto explícito) + C3 (recusa ≠ bloqueio) | Clareza de consequência |
| D3 — estabelecimento ambíguo | A3 (agente) — único aliviador que exige IA | Diferencial do agente |

> **Hipótese de encaixe central (HIP-P1-02):** o encaixe mais frágil é D2 × A2: se o associado não compreender a distinção entre recusa da compra e bloqueio do cartão apenas pelo texto, a proposta de valor muda radicalmente. Esta é a hipótese prioritária a testar (D13).

---

## 7. Proposta de valor em uma frase

> O aplicativo do Sicredi permite que o associado **confirme, conteste ou declare dúvida** sobre uma compra sinalizada **diretamente no app, com informações suficientes para uma decisão consciente**, sabendo desde o início que nenhuma resposta bloqueia o cartão automaticamente.

---

## 8. Valor para a instituição

**Hipótese de valor organizacional (HIP-P1-03):** redução de contatos de atendimento gerados por dúvidas sobre compras sinalizadas — o associado resolve no app sem ligar.

**O que não se afirma aqui:** redução direta de perdas por fraude, eliminação de casos para a analista ou melhoria de detecção. O canal de confirmação não é equivalente a um sistema de antifraude (DEC-P1-03).

**Como verificar:** comparar volume de contatos de atendimento em casos com e sem resolução autônoma no piloto; não extrapolar para perdas financeiras (HIP-P1-03).

---

## 9. Boas práticas já incorporadas

1. **Separação de caminhos:** "responder à compra" e "pedir atendimento" são ações distintas e paralelas — o segundo não encerra o primeiro (DEC-05).
2. **Declaração de limite do agente:** quando o nome do estabelecimento não é verificável, o agente diz explicitamente o que não sabe antes de apresentar os botões — não inventa (DEC-09).
3. **Desfecho diferenciado:** a tela de resultado descreve o estado da compra, não do cartão — evita a confusão mais crítica (HIP-01).
4. **Aviso anti-golpe:** o app comunica que nenhuma resposta é solicitada por telefone — estabelecimento de confiança do canal (HIP-04).

---

## 10. Hipóteses prioritárias a validar

| Prioridade | Hipótese | ID | Como testar |
|---|---|---|---|
| ⭐ 1 | O associado entende que recusar a compra não bloqueia o cartão inteiro, apenas com o texto da tela | HIP-01; HIP-P1-02 | Tarefa "não reconheço" + pergunta: "O que aconteceu com seu cartão?" (roteiro D13) |
| ⭐ 2 | O agente de IA agrega valor no caso de nome ambíguo; texto fixo seria insuficiente neste caso | HIP-P1-05 | Teste A/B: texto fixo × agente no caso de estabelecimento ambíguo |
| 3 | O associado consegue distinguir "Estou em dúvida" de "Quero falar com alguém" | HIP-02 | Pergunta: "Se você pediu ajuda, ainda poderia responder à pergunta da compra?" |
| 4 | O associado identifica o canal como legítimo pelo app autenticado + aviso | HIP-04 | Pergunta: "Como você sabia que essa mensagem era do seu banco?" |

---

## Rastreabilidade de fontes

| ID usado | Onde está |
|---|---|
| FON, HIP e DEC (incluindo os prefixos P1) | [Registro único de evidências e hipóteses](../05_gestao/evidencias_e_hipoteses.md) |
| R02, R03, R08, R11 | [D09 — Estrutura da solução](../03_computacao/D09_estrutura_solucao.md) e [matriz de cenários](../03_computacao/matriz_cenarios_e_evidencias.md) |
