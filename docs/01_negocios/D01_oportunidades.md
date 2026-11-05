# D01 — Oportunidades de segurança e clareza na confirmação de compras

**ID:** D01 · **Versão:** 0.2 · **Data:** 04/11/2026
**Responsável:** Produto · **Revisor principal:** Pesquisa
**Estado:** rascunho
**Fontes principais:** FON-01 (plano), FON-P1-01 (desafio Sicredi p.6), FON-04 (persona Valdir), FON-06 (cenário as-is), FON-08 (Hills/POV), FON-11 (desafio p.6)
**Decisões que sustenta:** DEC-P1-01 (recorte); alimenta D02–D04 e D08
**Depende de:** nenhuma · **Alimenta:** D02, D03, D04, D05, D08

> **Consolidação de 04/11/2026:** conteúdo documental/hipotético preservado; revisão cruzada pendente. Fontes com hash referem-se àquela versão. Registro comum em [evidências e hipóteses](../05_gestao/evidencias_e_hipoteses.md).

---

## Sumário

- [1. Contexto do desafio e recorte](#1-contexto-do-desafio-e-recorte)
- [2. Usuário prioritário e atores envolvidos](#2-usuário-prioritário-e-atores-envolvidos)
- [3. Evidências do problema](#3-evidências-do-problema)
- [4. Dores e necessidades](#4-dores-e-necessidades)
- [5. Alternativas atuais](#5-alternativas-atuais)
- [6. Oportunidades priorizadas](#6-oportunidades-priorizadas)
- [7. POV](#7-pov)
- [8. HMW — Como poderíamos…](#8-hmw--como-poderíamos)
- [9. Hipóteses mais arriscadas](#9-hipóteses-mais-arriscadas)
- [10. Evidência contrária e o que mudaria](#10-evidência-contrária-e-o-que-mudaria)
- [11. Alinhamento com outros artefatos](#11-alinhamento-com-outros-artefatos)

---

## 1. Contexto do desafio e recorte

<p align="justify">&ensp;&ensp; O desafio Sicredi propõe: "Como podemos utilizar IA Agêntica para prever e intervir em possíveis fraudes relacionadas a compras com cartões, aumentando a segurança dos associados e reduzindo perdas para o Sicredi?" (FON-P1-01, p.6). O desafio menciona explicitamente "alerta preventivo e confirmação de compras pelo associado" como direção a explorar.</p>

<p align="justify">&ensp;&ensp; <strong>Recorte deste produto (DEC-P1-01):</strong> confirmação de compras pelo associado — não prevenção completa de fraudes, não mesa de análise antifraude.</p>

| Elemento | Definição para este projeto |
|---|---|
| **Compra** | Transação sintética sinalizada pelo modelo de risco; dados fictícios |
| **Confirmação** | Ato explícito do associado de autorizar, recusar ou informar dúvida sobre uma compra sinalizada |
| **Exceção** | Caso em que a resposta do associado não resolve — expiração, dúvida irresolvível, recusa com revisão necessária |
| **Simulação** | Todas as ações financeiras são simuladas; nenhuma transação, bloqueio ou estorno real ocorre no MVP |
| **Fora do recorte** | Detecção em tempo real, bloqueio automático de cartão inteiro, estorno, novo cartão, autenticação bancária produtiva |

---

## 2. Usuário prioritário e atores envolvidos

| Ator | Papel | Necessidade central | Possível conflito |
|---|---|---|---|
| **Associado** (usuário principal) | Recebe a solicitação de confirmação; decide sobre a compra | Entender o que está sendo confirmado, confiar no canal, saber a consequência de cada resposta e ver o desfecho | Pode perceber o fluxo como intrusivo se receber muitas solicitações por compras legítimas (falsos positivos do modelo) |
| **Analista de prevenção a fraudes** | Recebe os casos que o associado não resolve | Ter contexto suficiente para revisar sem retrabalho | Pode receber casos ambíguos demais se o associado não tiver informação suficiente para decidir |
| **Atendimento / central** | Canal alternativo quando o associado busca ajuda fora do app | Orientar sem duplicar o processo do app | Canal pode ser usado por golpistas se não houver distinção clara entre o app e contatos externos (HIP-04) |
| **Instituição (Sicredi)** | Responsável pela adoção, custeio e política de uso | Reduzir esforço de atendimento em casos de dúvida; manter confiança do associado | Adoção depende de validação de eficácia que ainda não existe (HIP-P1-01) |

> **Nota:** "associado" e "instituição" têm papéis separados — quem usa o produto é o associado; quem adotaria e pagaria seria a instituição. São necessidades e decisores diferentes. Ver D08 §3.


---

## 3. Evidências do problema

| ID | Fonte | Achado | Alcance | Implicação para o produto |
|---|---|---|---|---|
| FON-06 | Cenário as-is do Leonardo (`origin/watson` `212655c`) | Jornada hipotética de 5 etapas: sinal → entender a compra → tentar contato → descobrir bloqueio → resolução com esforço | Hipótese construída a partir do briefing; não confirmada com associados ou Sicredi | O bloqueio no balcão e a falta de canal direto são candidatos a ponto de ruptura, não fato confirmado |
| FON-04 | Persona Valdir (Leonardo, `212655c`) | Frustração: passou vergonha no balcão; desconfiança de ligações de número desconhecido; usa app ao receber notificação | Protopersona hipotética — não entrevista executada | O app autenticado é o canal mais promissor; sinal de autenticidade importa |
| FON-08 | Hills e POV do Leonardo | POV: Valdir precisa confirmar/contestar compra com segurança sem ligar; Hills: 30 s e 2 min (aspirações) | Metas de Hill são aspirações de design, não resultados medidos | POV sustenta a direção; tempos não são compromisso |
| HIP-01 | Pesquisa, D02 | Associado pode confundir "não reconheço" com "bloquear o cartão inteiro" | Hipótese — não confirmada | Texto de resultado precisa distinguir explicitamente "compra recusada" de "cartão bloqueado" |
| HIP-03 | Pesquisa, D02 | Nome do estabelecimento pode não ser reconhecido mesmo em compra legítima | Hipótese — frequência desconhecida | O agente precisa informar o limite quando não há vínculo verificável; não inventar |
| HIP-04 | Pesquisa, D02 | Associado desconfia de mensagens que imitam o banco | Hipótese — contexto de uso confirmado só em entrevista | Canal precisa ser identificável como app autenticado, com aviso de que nenhuma resposta é pedida por telefone |
| FON-P1-01 | Desafio Sicredi, p.6 | O desafio cita "alerta preventivo" e "confirmação pelo associado" como direção | Definição do desafio acadêmico; não representa contrato com a Sicredi | Confirma que a direção de produto está alinhada ao desafio |
| D03 §4 | Pesquisa, D03 | Ponto de ruptura: associado não tem canal direto confiável para entender e resolver compra ambígua | Hipótese investigável — sustentada por FON-06 e HIP-04; não confirmada por entrevista | A ruptura é no reconhecimento + confiança no canal, não necessariamente no bloqueio no balcão |

---

## 4. Dores e necessidades

> Formato: **resultado buscado** + **obstáculo que impede**. Sem partir de funcionalidades.

| # | Resultado buscado | Obstáculo | Hipótese / fonte |
|---|---|---|---|
| N1 | Entender o que está sendo confirmado antes de responder | O nome do estabelecimento pode não ser reconhecido imediatamente; contexto adicional pode estar indisponível | HIP-03; FON-04 |
| N2 | Confiar que a mensagem é legítima antes de interagir | Canal de alerta é indistinguível, em aparência, de mensagens de golpe | HIP-04; FON-04 |
| N3 | Saber o que cada resposta causa antes de escolher | Consequência das três respostas não é visível antes da escolha; confusão entre "recusar compra" e "bloquear cartão" | HIP-01; HIP-05 |
| N4 | Pedir ajuda sem perder a oportunidade de responder | O associado pode acreditar que pedir atendimento encerra a confirmação | HIP-02; DEC-05 (Pesquisa) |
| N5 | Ver o desfecho claramente após responder | Sem retorno de status, o associado não sabe se a situação foi resolvida | HIP-09; FON-04 |
| N6 | Resolver sem precisar ligar para a central | A central pode ser de difícil acesso; ligação para número desconhecido é ignorada | HIP-07; HIP-08; FON-06 |

---

## 5. Alternativas atuais

<p align="justify">&ensp;&ensp; Como a pessoa tenta resolver hoje e o que continua difícil. Conteúdo hipotético, derivado de D03 e das fontes documentais. Não confirmado com associados ou Sicredi.</p>

| Alternativa atual | O que resolve | O que continua difícil |
|---|---|---|
| Ligar para a central de atendimento | Obtém orientação humana | Tempo de espera; URA burocrática; risco de ser atendido por golpistas em número falso (HIP-04); precisa repetir o contexto |
| Ignorar o alerta | Nenhuma ação imediata necessária | Compra pode ser recusada ou cartão bloqueado sem que o associado entenda o motivo |
| Descobrir o problema no balcão | — | Vergonha; necessidade de resolver presencialmente; cartão bloqueado sem aviso prévio (HIP-08) |
| Ir à agência | Resolução humana completa | Esforço, deslocamento e tempo; desnecessário para casos que poderiam ser resolvidos pelo app |

<p align="justify">&ensp;&ensp; <strong>Lacuna central (hipotética):</strong> não existe hoje um canal direto, identificável como legítimo, que permita ao associado entender a compra, pedir ajuda contextual e registrar sua resposta explícita sem ligar para ninguém. O que existe exige esforço desproporcional ao risco.</p>

---

## 6. Oportunidades priorizadas

| # | Fricção | Resultado desejado pelo associado | Valor esperado | Incerteza |
|---|---|---|---|---|
| O1 | Não reconhecer o nome do estabelecimento na fatura | Entender a compra sem precisar ligar; decidir com segurança | Menos casos sem resposta; menos contatos de atendimento por dúvida (HIP-P1-03) | Com que frequência nomes são ambíguos? (HIP-03) |
| O2 | Não saber se a mensagem é legítima | Responder com confiança de que está no canal certo | Redução de abandono por desconfiança | O sinal de autenticidade do app é percebido? (HIP-04) |
| O3 | Não saber o efeito de cada resposta antes de escolher | Tomar decisão consciente sem medo de consequência indesejada | Menos autorizações equivocadas; menos pedidos de ajuda por confusão | A explicação prévia do efeito muda o comportamento? (HIP-05) |
| O4 | Não ter retorno claro após responder | Saber que o caso foi registrado e o próximo passo | Redução de contatos pós-resposta para confirmar o que aconteceu | O associado lê e entende a tela de resultado? (HIP-09) |

<p align="justify">&ensp;&ensp; <strong>Prioridade:</strong> O3 é a fricção de maior risco de erro no MVP (confundir recusa com bloqueio do cartão). O1 é onde o agente tem o papel mais diferenciado. O2 e O4 são necessárias para que O1 e O3 funcionem.</p>

---

## 7. POV

> Adaptado do POV do Leonardo (FON-08), ajustado ao foco em clareza e consequência.

**Valdir** precisa de **um canal confiável para entender e responder a uma compra sinalizada com clareza sobre o que está autorizando e o que acontece depois**, porque **não consegue distinguir mensagens legítimas de golpe pelo canal atual e não sabe o que cada resposta causa à sua conta e ao seu cartão**.

---

## 8. HMW — Como poderíamos…

<p align="justify">&ensp;&ensp; <strong>HMW principal</strong> (ponto de partida a verificar na pesquisa):</p>

> "Como poderíamos ajudar o associado a decidir sobre uma compra sinalizada com clareza sobre o que está autorizando e sobre o próximo passo quando continua em dúvida?"

<p align="justify">&ensp;&ensp; <strong>HMWs complementares</strong> (derivadas das oportunidades acima):</p>

- Como poderíamos mostrar o contexto da compra de forma que o associado reconheça o estabelecimento — ou entenda quando a informação disponível é insuficiente?
- Como poderíamos distinguir visualmente a mensagem legítima do app de comunicações externas?
- Como poderíamos explicar o efeito de cada resposta sem aumentar o tempo e o esforço de quem já reconhece a compra?
- Como poderíamos confirmar o desfecho de forma que o associado não precise ligar para saber o que aconteceu?

<p align="justify">&ensp;&ensp; Estas perguntas estão abertas a mais de uma solução tecnológica. Ver D04 para a comparação de alternativas.</p>

---

## 9. Hipóteses mais arriscadas

| Hipótese | Como verificar | Consequência se for falsa |
|---|---|---|
| HIP-01: o associado confunde "não reconheço" com "bloquear o cartão inteiro" | Tarefa "não reconheço" + pergunta de compreensão (roteiro D13) | Se falsa: a explicação do efeito não é a decisão de design mais urgente; outra fricção assume prioridade |
| HIP-P1-02: a premissa mais frágil é a compreensão da diferença recusa × bloqueio do cartão | Mesmo teste de HIP-01 | Se confirmada como incompreensível na maioria: toda a proposta de valor do fluxo autônomo precisa incluir instrução antes da tela de confirmação |
| HIP-P1-05: texto fixo é insuficiente para o caso de nome ambíguo | Alternância de fluxo básico × agente no piloto (D13) | Se falsa (texto fixo resolve bem): a justificativa de necessidade de IA agêntica precisa se basear em outro cenário |
| HIP-P1-01: a instituição adotaria o produto se reduzisse esforço de atendimento | Conversa com mentor/orientador; benchmarks de volume de atendimento | Se falsa: a proposta de valor para a instituição precisa ser reformulada ou a pesquisa de adoção precisa ser mais ampla |

---

## 10. Evidência contrária e o que mudaria

<p align="justify">&ensp;&ensp; <strong>Evidência que contraria a ideia inicial:</strong> o cenário as-is do Leonardo (FON-06) aponta o bloqueio no balcão como a ruptura central. Se pesquisa confirmasse que o bloqueio automático é o processo padrão atual do Sicredi para todos os casos suspeitos, o ponto de ruptura mudaria: a intervenção mais importante seria <em>antes</em> do bloqueio, não depois do alerta chegar ao app.</p>

<p align="justify">&ensp;&ensp; <strong>O que mudaria na solução:</strong> a prioridade deixaria de ser "clareza sobre a compra" e passaria a ser "aviso antecipado antes do bloqueio". O produto precisaria atuar mais cedo na cadeia — no momento da transação, não depois — o que mudaria arquitetura, integração e o papel do associado no fluxo.</p>

<p align="justify">&ensp;&ensp; <strong>Por que ainda mantemos a direção atual:</strong> a ruptura da Pesquisa (D03 §4) aponta para a indisponibilidade de canal confiável de entendimento como fricção mais fundamental, independentemente do bloqueio. Essa interpretação continua válida enquanto a pesquisa não confirmar o bloqueio padrão. Ver Lacuna 1 em D03 §5.</p>

---

## 11. Alinhamento com outros artefatos

- **POV/Hills do Leonardo (FON-08):** POV aproveitado; metas de tempo (30 s, 2 min) registradas como aspirações, não resultados.

- **D02/D03 (Pesquisa):** necessidades N1–N6 derivadas das tensões do mapa de empatia e do ponto de ruptura do cenário atual.

- **D06 (Pesquisa):** os seis cenários de D06 cobrem exatamente as hipóteses N1–N6 acima — confirmando que o POV, as necessidades e os cenários estão coerentes.

- **D09 (Arquitetura):** requisitos R01–R12 endereçam N1–N6; R03 (três respostas explícitas) e R02 (confirmação vinculada à compra) são os mais diretamente ligados às necessidades prioritárias.
