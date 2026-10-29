# D06 — Persona e Cenários: Associado diante de uma compra sinalizada

**ID:** D06  
**Versão:** 0.1 · 28/10/2026  
**Responsável:** Pessoa 2  
**Revisor principal:** Pessoa 1  
**Estado:** rascunho para revisão — protopersona hipotética; cenários construídos a partir do plano vigente; pesquisa com usuários não executada  
**Origem:** personas do Leonardo (`origin/watson` `212655c`, `docs/design/00-descoberta/personas.md`); plano vigente (`origin/develop` `8942cc5`); POV do Leonardo (`hills-e-pov.md`); revisão por Pessoa 2

---

## 1. Persona principal — Valdir (protopersona do associado)

> **Marcação:** Esta é uma **protopersona hipotética** construída a partir do material do Leonardo (FON-04) e ajustada ao foco atual no associado. Idade, profissão e detalhes contextuais são hipóteses que ajudam decisões de design; não representam perfil demográfico confirmado nem associado entrevistado.

| Elemento da persona | Descrição | Fonte / hipótese | Decisão de experiência que influencia |
|---|---|---|---|
| **Nome de referência** | Valdir | FON-04 (Leonardo) | Identificação interna; não representa uma pessoa real |
| **Perfil funcional (hipótese)** | Associado de longa data de uma cooperativa de crédito; usa o cartão com frequência para compras físicas e, eventualmente, online; relação com o app é funcional mas não frequente | FON-04; HIP-06 | Interface precisa ser auto-explicativa; não pode depender de familiaridade com terminologia financeira |
| **Objetivo** | Resolver a compra sinalizada sem precisar ligar para ninguém ou ir à agência | FON-04; HIP-07 | Fluxo completo no app, incluindo pedido de atendimento |
| **Frustração central** | Já teve o cartão bloqueado numa compra legítima sem aviso prévio; não sabe distinguir mensagem legítima de golpe | FON-04; HIP-01; HIP-04 | Texto de resultado deve distinguir "compra recusada" de "cartão bloqueado"; sinal de autenticidade da mensagem |
| **Contexto de decisão** | Recebe o alerta a qualquer hora; pode estar no campo, no balcão ou em baixa conectividade; o momento é inesperado | FON-04; HIP-06 | Interface objetiva; botões grandes; tratamento claro de falha de conexão com orientação para nova tentativa (HIP-06; ver DEC em evidencias_e_hipoteses.md) |
| **Estado de sucesso** | Entende o que está sendo confirmado, dá uma resposta consciente ou pede ajuda, e sabe o que aconteceu depois | FON-01 §9 (perguntas de avaliação); HIP-09 | Tela de resultado com status da compra e próximo passo |
| **Relação com o sistema** | Não usa o console de análise; acessa o produto pelo alerta no app; uso esporádico e baixa familiaridade digital | FON-04 | Sem jargão; sem links para fora do app; texto legível em tela pequena |

**POV (adaptado do Leonardo — FON-08):**  
> Valdir precisa de uma forma de confirmar ou contestar uma compra sinalizada com segurança e sem ligar para ninguém, porque não confia em contatos externos por telefone e só percebe o problema quando já está impactado.

---

## 2. Ator secundário — Camila (analista, exceções)

> Camila aparece neste documento apenas onde a jornada do associado depende da revisão de exceções. O detalhamento da sua experiência pertence às entregas de outras frentes (D09/D10). Nenhum conjunto completo de entregas de analista é produzido aqui.

| Papel neste documento | Descrição |
|---|---|
| **Quando aparece** | Quando o associado pede atendimento, quando a confirmação expira sem resposta, ou quando a avaliação inicial da compra resulta em `REVISAO_PENDENTE` |
| **O que o documento precisa mostrar** | Que existe um caminho humano de revisão nas exceções; que pedir atendimento abre esse caminho sem encerrar a confirmação; que o associado pode ainda responder enquanto a confirmação for válida |
| **O que o documento NÃO faz** | Detalhar a fila de análise, a produtividade da analista, o bloqueio do cartão pela analista ou o atendimento telefônico completo |

---

## 3. Episódio de comparação: compra sinalizada com nome de estabelecimento ambíguo

> Usando o mesmo episódio-base nos dois cenários para permitir comparação honesta.  
> **Situação:** associado recebe alerta sobre uma compra com valor razoável, mas o nome do estabelecimento não é imediatamente reconhecido.

| Momento | Cenário atual (hipótese — ver D03) | Fonte / hipótese | Experiência futura proposta (MVP) | Capacidade / decisão que muda | Limite do MVP | Como verificar |
|---|---|---|---|---|---|---|
| **1. Perceber o problema** | Recusa no balcão, SMS ou outro canal; o associado pode não saber distinguir mensagem legítima de golpe | FON-06; HIP-04; HIP-08 | Notificação no app autenticado com aviso de que nenhuma resposta é pedida por telefone | Canal confiável disponível no app autenticado; se o app não estiver instalado ou a notificação desabilitada, o canal não muda | O app precisa estar instalado e com notificação habilitada — condição que precisa ser verificada com usuários reais | Pergunta: "Como você ficou sabendo? Pelo app ou por outro canal?" |
| **2. Entender a compra** | Sem contexto; precisa ligar ou ir à agência | FON-06; HIP-03 | App mostra estabelecimento disponível, valor, data, cartão parcial e, quando não há vínculo verificável, informa explicitamente | Informação antes da ação; agente informa o limite em vez de inventar | O agente não pode confirmar identidade de estabelecimento que não está no contexto disponível (DEC-09) | Tarefa: "O que está sendo confirmado?" |
| **3. Decidir** | Não há canal de resposta direta; liga para central (espera) ou ignora | FON-06; HIP-07 | Três opções explícitas com breve descrição de efeito: Autorizo · Não reconheço · Estou em dúvida | Associado responde explicitamente; o agente não decide por ele (DEC-07) | Resposta fora do prazo não libera a compra; o prazo não é prorrogado por pedir atendimento (DEC-05) | Tarefa: "Qual você escolheria? Por quê?" |
| **4. Pedir ajuda se necessário** | Longa espera; risco de não ser atendido; precisa repetir o contexto | FON-06; HIP-07 | Ação separada: "Quero falar com alguém" abre revisão sem registrar uma resposta à confirmação | Confirmação continua aberta e respondível enquanto válida; atendimento não encerra o prazo (DEC-05) | O prazo não é prorrogado; atendimento apenas garante que o caso seja revisado | Pergunta: "Se você pedisse ajuda, ainda poderia responder à pergunta da compra?" |
| **5. Ver o desfecho** | Sem retorno claro; não sabe se a compra foi estornada ou o cartão bloqueado | HIP-09; HIP-01 | Tela de resultado com: o que aconteceu com a compra (não com o cartão), status e próximo passo | Associado sabe o desfecho sem ligar | Resultado é simulado; não há transação financeira real ou bloqueio de cartão real (DEC-08) | Pergunta: "O que aconteceu? O que você faria agora?" |

---

## 4. Seis cenários do produto

> Cada cenário segue o plano vigente (FON-01 §§1, 3 e 9). Ações simuladas são identificadas como tal (DEC-08).

### Cenário 1 — Reconhece e autoriza

**Situação:** o associado identifica a compra antes de responder.  
**O que o sistema faz:** registra `AUTHORIZE`, libera a compra na simulação, mostra resultado com status `LIBERADA_SIMULACAO`.  
**O que o documento precisa mostrar:** a compra foi confirmada pelo associado; a liberação é simulada; o produto não declara ausência de fraude nem garante a legitimidade da compra.  
**Hipótese a verificar:** o associado entende que "autorizo" confirma a compra, não declara que ela foi legítima. (HIP-05)

### Cenário 2 — Não reconhece

**Situação:** o associado não reconhece a compra e responde `DENY`.  
**O que o sistema faz:** registra recusa simulada; abre encaminhamento de proteção/revisão; mostra que a compra foi recusada (não que o cartão foi bloqueado).  
**O que o documento precisa mostrar:** diferença entre "compra recusada" e "cartão bloqueado inteiro" — o protótipo não bloqueia o cartão automaticamente (DEC-04). O encaminhamento de revisão existe; quem o processa é a analista nas exceções.  
**Hipótese a verificar:** o associado compreende que recusar a compra não bloqueia o cartão inteiro. (HIP-01)

### Cenário 3 — Está em dúvida

**Situação:** o associado não tem certeza se reconhece a compra. Responde `UNSURE`.  
**O que o sistema faz:** registra `UNSURE`, leva a compra a `REVISAO_PENDENTE`, mostra status e próximo passo.  
**O que o documento precisa mostrar:** "Estou em dúvida" registra uma resposta explícita e encaminha para revisão; é diferente de pedir atendimento (DEC-05). A compra não é autorizada nem recusada por isso.  
**Hipótese a verificar:** o associado percebe a diferença entre "estou em dúvida" e "quero falar com alguém". (HIP-02)

### Cenário 4 — Pede atendimento antes de responder

**Situação:** o associado usa a opção "Quero falar com alguém" sem ter escolhido uma das três respostas.  
**O que o sistema faz:** abre ou reaproveita uma revisão; a confirmação permanece no estado `AGUARDANDO_ASSOCIADO` enquanto ainda válida; o associado pode responder depois.  
**O que o documento precisa mostrar:** pedir atendimento não registra `UNSURE`, não encerra a confirmação e não prorroga o prazo (DEC-05). O associado pode voltar e responder se o prazo não tiver expirado.  
**Hipótese a verificar:** o associado entende que ainda pode responder após pedir ajuda. (HIP-02)

### Cenário 5 — Não responde no prazo

**Situação:** o prazo da confirmação expira sem resposta.  
**O que o sistema faz:** status muda para `CONFIRMACAO_EXPIRADA`; a compra não é liberada; o app mostra o status e o caminho de revisão.  
**O que o documento precisa mostrar:** expiração não significa autorização presumida (DEC-06). Existe um caminho para revisão após a expiração.  
**Hipótese a verificar:** o associado compreende que o prazo expirou e que a compra não foi liberada automaticamente. (HIP-09)

### Cenário 6 — Informação insuficiente ou chat indisponível

**Situação:** o nome do estabelecimento não está disponível ou o chat do agente falha.  
**O que o sistema faz:** apresenta a identificação disponível (categoria ou ID parcial), informa o limite explicitamente, mantém o caminho de resposta e revisão.  
**O que o documento precisa mostrar:** o agente não inventa o nome do estabelecimento; a falha do chat não impede a resposta à confirmação; existe um caminho explícito de revisão (FON-01 §9).  
**Hipótese a verificar:** o associado entende o que o sistema sabe e o que ele não conseguiu confirmar. (HIP-03; HIP-05)

---

## 5. Implicações de design e rastreabilidade

| Necessidade / hipótese | Decisão de design recomendada | Requisito do plano | Teste de compreensão proposto |
|---|---|---|---|
| HIP-01: confundir recusa com bloqueio do cartão inteiro | Texto de resultado explícito: "A compra foi recusada. Seu cartão não foi bloqueado." + próximo passo de revisão | R03, R11 | Tarefa: "não reconheço" + pergunta: "O que aconteceu com o seu cartão?" |
| HIP-02: não saber se pode responder após pedir ajuda | Status da confirmação visível na tela de atendimento: "Sua compra ainda aguarda uma resposta (válida até [horário])." | R02, R03 | Pergunta: "Se você pediu ajuda, ainda poderia responder à pergunta da compra?" |
| HIP-03: nome do estabelecimento irreconhecível | Mostrar o máximo disponível; quando não houver vínculo verificável, comunicar o limite antes de apresentar os botões | R02, R07, R09 | Tarefa: "O que está sendo confirmado aqui? Você reconhece esse nome?" |
| HIP-04: desconfiança do canal | Identificação visual clara da origem (app autenticado); aviso: ninguém pede resposta por telefone | R02, R11 | Pergunta: "Como você sabia que essa mensagem era do seu banco?" |
| HIP-05: não saber o efeito de cada resposta antes de escolher | Breve descrição do efeito junto a cada botão; confirmação de resultado após a escolha | R03, R11 | Tarefa de observação; depois perguntar: "O que você entendeu que aconteceria ao escolher cada opção?" (ver roteiro C2) |
| HIP-09: não saber o desfecho após responder | Tela de resultado com: compra (não cartão), status (`LIBERADA`, `RECUSADA`, `REVISAO_PENDENTE`, `EXPIRADA`) e próximo passo | R02, R03, R11 | Tarefa: verificar tela pós-resposta + pergunta: "O que aconteceu? O que você faria agora?" |
| DEC-05: pedido de atendimento não encerra a confirmação nem prorroga o prazo | Separar visualmente os dois caminhos; mostrar status da confirmação em abas/telas de atendimento | R03, R08 | Pergunta: "Depois de pedir ajuda, sua resposta sobre a compra ainda estava aberta?" |

> Os requisitos R02, R03, R07, R08, R09 e R11 são candidatos; cada associação acima foi justificada pela hipótese correspondente. Nenhum requisito está marcado como implementado nesta versão.

---

## 6. O que precisa de pesquisa antes de fechar a persona e os cenários

- Confirmar se o perfil funcional do Valdir (uso esporádico do app, contexto rural/campo) é representativo ou se existem variações relevantes de perfil.
- Verificar se a distinção entre "recusa da compra" e "bloqueio do cartão" é compreendida sem explicação (HIP-01) — decisão de maior impacto na interface.
- Testar se o associado percebe a diferença entre "Estou em dúvida" e "Quero falar com alguém" (HIP-02) — distinção nova em relação à versão anterior.
- Verificar se o estado de sucesso ("entender a solicitação, dar uma resposta consciente ou pedir ajuda e entender o status/próximo passo") é atingível com o texto e o fluxo propostos.

Ver `roteiro_pesquisa.md` para perguntas e tarefas correspondentes.
