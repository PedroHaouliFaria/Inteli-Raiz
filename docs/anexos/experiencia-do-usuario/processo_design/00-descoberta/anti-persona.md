# Anti-persona · "O Impostor"

> **O que é.** Para o NN/g, antipersonas são "pessoas que podem usar mal o produto de um jeito que prejudica os usuários-alvo e o negócio". É diferente de uma *persona negativa* (alguém para quem só não desenhamos). No Watson, a anti-persona é quem **ataca o fluxo** que as personas usam. Por isso o objetivo do design é **frustrá-la sem punir a Camila e o Valdir**.
>
> **Método.** Usamos o mesmo modelo das personas (objetivo, frustração, contexto, sucesso, relação com o sistema), como recomenda a UserTesting. A ele juntamos o formato das *fraudster personas* do Serious Fraud Office da Nova Zelândia e do Counter Fraud Centre da Austrália: **definição em uma linha, ações típicas e sinais de alerta**, todos descritos pelo **método** e não pela aparência ou pela origem da pessoa. Os sinais vêm do próprio case do Sicredi: rajadas, alta velocidade, horários concentrados, divergência geográfica, valores anômalos e cartão não presente.
>
> **Status.** É uma proto-anti-persona e precisa ser validada com alguém de prevenção a fraudes (Sponsor User).

---

## Anti-persona · O Impostor

> Mesmo template das personas (`personas.md`): quem, objetivo, frustração, contexto de decisão, estado de sucesso, relação com o sistema, frase e implicações de design.

| | |
|---|---|
| **Quem** | Quadrilha que opera com dados de cartão vazados, online e por telefone. Sem nome próprio nem rosto, de propósito: descrevemos o comportamento, não uma pessoa. Combina os perfis *Impersonator*, *Exploiter* e *Organised* (SFO/NZ). |
| **Objetivo** | Converter o máximo de cartões vazados em dinheiro antes do bloqueio. |
| **Frustração** | Bloqueio rápido do cartão; associado que não confia em ligação; confirmação que só o associado consegue dar; alerta que não pode ser imitado. |
| **Contexto de decisão** | Madrugada, rajadas de minutos, lojas online (cartão não presente), longe da região do associado, aparelhos novos. Conhece e imita a linguagem dos alertas dos bancos. |
| **Estado de sucesso** | O associado toca "Fui eu" achando que está se protegendo, ou passa um código por telefone, e a compra é liberada. |
| **Relação com o Watson** | Nunca vê o console. Ataca o **modelo** (testes de limite), o **canal de alerta** (imitação e pressão) e a **analista** (volume para causar fadiga). |
| **Frase** | "Só preciso que ele toque em 'Fui eu'." |

**Implicações de design (contramedidas)**
- Atrito assimétrico: "Não reconheço" bloqueia na hora; "Fui eu" no alto risco pede biometria.
- Alerta sem link, só dentro do app, avisando que ninguém pede resposta por telefone.
- O app não revela os sinais que dispararam o alerta; aparelho trocado recentemente manda o caso para a analista.

## Ações típicas
1. **Teste de cartão**: compras de valor baixo em sequência para saber se o cartão está ativo e onde fica o limite de bloqueio.
2. **Rajada**: várias compras em poucos minutos, de madrugada, em lojas online de revenda fácil.
3. **Ligação falsa**: liga para o associado "da central de segurança" logo depois do alerta e pede que ele toque em "Fui eu" ou informe um código.
4. **Mensagem clonada**: SMS ou WhatsApp com link imitando o alerta do app.
5. **Fadiga de alerta**: dispara muitas tentativas para gerar alertas em série, até o associado aprovar por cansaço ou a fila da analista lotar.
6. **Troca de chip (SIM swap)**: quando consegue, assume o número do associado para receber o alerta ele mesmo.

## Sinais de alerta (o que o Watson procura)
- Várias transações em minutos com o mesmo cartão (rajada / velocidade)
- Compra longe de onde o associado costuma comprar (divergência geográfica)
- Horário fora do padrão do associado
- Valor muito acima da média ou sequência de valores pequenos (teste)
- Cartão não presente, dispositivo ou e-mail novos
- Associado que responde "Fui eu" logo depois de uma ligação, ou de um aparelho trocado recentemente

## Contramedidas de design (o que muda nas telas)
| Ataque | Contramedida no Watson | Onde aparece |
|---|---|---|
| Ligação falsa pedindo para tocar "Fui eu" | O alerta diz claramente que **ninguém da cooperativa vai pedir para você responder por telefone** e que a resposta só existe dentro do app | App do associado |
| Mensagem clonada com link | O alerta **nunca tem link** e só aparece dentro do app autenticado. Nas comunicações fora do app, nenhuma ação é possível | App do associado |
| Aprovação por pressão ou cansaço | **Atrito assimétrico**: "Não reconheço" bloqueia na hora, sem atrito. "Fui eu" em caso de alto risco pede biometria do aparelho | App do associado |
| Troca de chip | Aparelho ou número trocado recentemente é sinal de risco: o agente **não aceita "Fui eu" sozinho** e manda o caso para a analista | Caso (console) |
| Teste de limite do modelo | O app **não explica ao associado** quais sinais dispararam o alerta (o detalhe fica no console). O agente agrupa testes de valor baixo do mesmo cartão | App e Quadro |
| Fadiga da analista | Agrupamento de rajadas em um só caso, fila por risco × valor e resumo do agente | Fila e Quadro |

## Tensão com as personas (o que não podemos piorar)
- **Valdir**: cada atrito extra contra o Impostor pesa em quem tem pouca familiaridade digital. Regra: atrito só em "Fui eu" e só no alto risco; "Não reconheço" é sempre um toque.
- **Camila**: o agente não pode empurrar para ela todo "Fui eu" suspeito. Só sobe para a analista o que tem sinal de engenharia social ou de troca de aparelho.

## Métricas de sucesso contra a anti-persona
- Taxa de "Fui eu" em casos depois confirmados como fraude (deve cair)
- Tempo entre a primeira transação da rajada e o bloqueio
- Falsos positivos por associado (não deve subir para o Valdir)

## Candidata considerada e deixada para depois
**Autofraude** (o próprio associado nega uma compra que fez para pedir estorno). É um risco real, mas atinge mais o fluxo de contestação do que o de alerta preventivo. Fica para quando o MVP tratar a contestação.

## Referências
- NN/g, Antipersonas in UX: https://www.nngroup.com/videos/antipersonas/
- UserTesting, What are anti-personas: https://usertesting.com/blog/anti-personas
- Serious Fraud Office (NZ), Fraudster personas: https://sfo.govt.nz/counter-fraud/guidance/fraudster-personas
- Commonwealth Fraud Prevention Centre (AU), Guide to the practical use of fraudster personas: https://www.counterfraud.gov.au/library/guide-practical-use-fraudster-personas
- Case Sicredi: `data/Orientacoes_case_prevencao_sicredi.txt` no repositório Inteli-Raiz
