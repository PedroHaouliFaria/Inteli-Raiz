# D02 — Mapa de Empatia do Associado

**ID:** D02  
**Versão:** 0.1 · 28/10/2026  
**Responsável:** Pessoa 2  
**Revisor principal:** Pessoa 1  
**Estado:** rascunho para revisão — pesquisa com usuários não executada  
**Origem:** base de Leonardo (`origin/watson` hash `212655c`, `docs/design/00-descoberta/mapas-de-empatia.md` e `personas.md`); revisão por Pessoa 2 conforme plano vigente (`origin/develop` `8942cc5`)

---

## 1. Situação delimitada

**Contexto de uso:** associado recebe uma solicitação de confirmação de compra no aplicativo. A compra foi sinalizada pelo sistema e aguarda sua resposta.  
**Objetivo da pessoa:** entender o que aconteceu, decidir se reconhece ou não a compra e saber o que ocorre depois da sua resposta.  
**Marcação:** todo o conteúdo abaixo é hipótese de trabalho ou interpretação derivada de fontes documentais, salvo identificação explícita de observação. Nenhum participante foi entrevistado nesta versão.

---

## 2. Mapa principal

### O que o associado diz e faz

> _Paráfrases hipotéticas — não são falas de participantes entrevistados (HIP-xx indicado)._

| Bloco | Conteúdo |
|---|---|
| **Diz** (paráfrases hipotéticas) | "Não fui eu que comprei isso!" (HIP-03) · "Por que bloquearam meu cartão?" (HIP-01) · "Minha filha que mexe nisso." (HIP-06) |
| **Faz** | Ignora ligações de número desconhecido (HIP-04) · Abre o app ao receber notificação (HIP-07) · Pede ajuda à família para entender mensagens (HIP-06) |

### O que o associado pensa e sente

| Bloco | Conteúdo |
|---|---|
| **Pensa** (paráfrases hipotéticas) | "Será que essa mensagem é golpe?" (HIP-04) · "Vou ter que ir até a agência resolver." (HIP-08) · "Se eu clicar errado, perco dinheiro." (HIP-05) · "O que acontece se eu responder errado?" (HIP-05) · "Ainda posso responder se pedir ajuda primeiro?" (HIP-02) |
| **Sente** | Medo de golpe (HIP-04) · Vergonha quando o cartão é recusado no balcão (HIP-08) · Alívio quando alguém resolve por ele (HIP-07) · Insegurança diante de termos técnicos (FON-04) |

### Ambiente e informação percebida

| Bloco | Conteúdo |
|---|---|
| **Vê / recebe** (hipótese) | Notificação do app com valor, estabelecimento e data · Pergunta: "Você reconhece esta compra?" · Três botões de resposta · Possivelmente: nome de estabelecimento que não reconhece de imediato (HIP-03) |
| **Canal** (hipótese) | App mobile da cooperativa; recebimento a qualquer hora, inclusive de madrugada ou no campo (FON-04; HIP-06) |

### Necessidades

| Bloco | Conteúdo |
|---|---|
| **Precisa** | Entender claramente o que está sendo confirmado (HIP-03) · Confiar que a mensagem é legítima (HIP-04) · Saber o que cada resposta causa — sem descobrir só depois (HIP-05) · Poder pedir ajuda sem perder a chance de responder (HIP-02) · Ver o status após responder (HIP-09) |

### Dores

| Bloco | Conteúdo |
|---|---|
| **Dores** (hipótese) | Não saber distinguir mensagem legítima de golpe (HIP-04) · Não entender se "não reconheço" bloqueia o cartão inteiro ou só a compra (HIP-01) · Receber o alerta num momento de baixa conectividade ou distração (HIP-06) · Não ter retorno claro do que aconteceu com a compra (HIP-09) |

### Ganhos desejados

| Bloco | Conteúdo |
|---|---|
| **Ganhos** (hipótese) | Responder sem precisar ligar para ninguém (HIP-07) · Sentir que a compra foi resolvida com clareza (HIP-09) · Não ser punido por uma compra legítima ambígua (HIP-03) · Saber que o cartão não foi bloqueado por completo sem necessidade (HIP-01) |

---

## 3. Tabela de notas

| Bloco | Conteúdo | Natureza | ID fonte / hipótese | Pergunta para investigar |
|---|---|---|---|---|
| Diz | "Não fui eu que comprei isso!" | Hipótese / paráfrase | HIP-03; FON-05 | Esta é a reação mais comum? Ou o associado costuma reconhecer a compra mas ainda assim hesita? |
| Pensa | "Será que essa mensagem é golpe?" | Hipótese | HIP-04; FON-05 | Em que condições o associado confia na mensagem? O que o convence? |
| Faz | Ignora ligações desconhecidas | Hipótese de comportamento | HIP-04; FON-04 | Quantas vezes isso ocorreu? Qual o impacto no caso não resolvido? |
| Pensa | "Se eu clicar errado, perco dinheiro" | Hipótese | HIP-05 | Qual das três respostas gera mais medo de consequência negativa? |
| Pensa | "Ainda posso responder se pedir ajuda primeiro?" | Hipótese derivada de regra do produto | HIP-02; DEC-05 | O associado entende que pedir atendimento não encerra a confirmação? |
| Sente | Vergonha no balcão | Hipótese | HIP-08; FON-04 | Qual é a sequência de eventos que leva ao bloqueio no balcão? Isso ainda ocorre no modelo atual? |
| Vê | Nome de estabelecimento irreconhecível | Hipótese | HIP-03 | Com qual frequência o nome na fatura difere do nome percebido pelo associado? |
| Precisa | Saber o que cada resposta causa | Hipótese de necessidade | HIP-05 | O associado lê ou ignora a descrição do efeito de cada opção ao usar o produto? |
| Precisa | Ver status após responder | Hipótese de necessidade | HIP-09 | O que o associado procura ver na tela após tocar em qualquer resposta? |
| Dor | Baixa conectividade no campo | Hipótese de contexto | HIP-06; FON-04 | Qual proporção de associados está em áreas rurais? O que o app mostra quando não há conexão no momento da resposta? |

---

## 4. Síntese: necessidades e tensões

Com base nas hipóteses acima (não em pesquisa executada):

1. **Confiança no canal** — o associado precisa reconhecer a mensagem como legítima antes de interagir. A desconfiança em comunicações financeiras é a tensão mais estrutural.
2. **Reconhecimento da compra** — mesmo compras legítimas podem ter nomes ambíguos. O sistema precisa apresentar o máximo de contexto disponível e comunicar quando não há informação verificável, sem inventar.
3. **Compreensão das consequências** — o associado pode não saber que "não reconheço" registra uma recusa simulada (não bloqueia o cartão inteiro) e que "estou em dúvida" abre uma revisão. Essa diferença importa para a decisão.
4. **Independência de canal** — a necessidade de pedir ajuda não deve encerrar a possibilidade de resposta. O produto prevê isso (DEC-05), mas o associado precisa entender o status claramente.
5. **Desfecho visível** — a ausência de retorno após a resposta pode criar sensação de que nada aconteceu.

Estas tensões são hipóteses de projeto. A pesquisa pode invalidá-las, ordená-las de forma diferente ou revelar tensões não previstas.

---

## 5. Implicações para o design

| Implicação | Hipótese que origina | Como verificar compreensão |
|---|---|---|
| **Mostrar antes de perguntar:** exibir valor, estabelecimento ou categoria disponível, data e cartão parcialmente identificado antes de mostrar os botões de resposta | HIP-03: nome da fatura pode não ser reconhecido; HIP-05: escolha consciente requer contexto | Tarefa: "O que está sendo confirmado nessa tela? Quanto custa e onde foi feita?" |
| **Descrever brevemente o efeito de cada resposta** antes da escolha: "Reconheço → confirma a compra", "Não reconheço → recusa e abre revisão da compra", "Estou em dúvida → mantém em revisão" | HIP-01: confundir "não reconheço" com bloqueio do cartão; HIP-05: medo de clicar errado | Tarefa de observação; depois perguntar: "O que você entendeu que aconteceria ao escolher cada opção?" (ver roteiro C2) |
| **Sinal de autenticidade da mensagem:** texto simples informando que a mensagem veio do app autenticado e que ninguém pede resposta por telefone | HIP-04: desconfiança em comunicações financeiras | Pergunta: "Como você sabia que essa mensagem era do seu banco?" |
| **Tela de resultado clara:** após qualquer resposta, mostrar o que aconteceu com a compra (não com o cartão), o que vem a seguir e como entrar em contato se necessário | HIP-09: associado não sabe se o caso foi resolvido | Tarefa: "O que apareceu depois que você respondeu? O que você faria agora?" |

> **Decisão de design pendente:** verificar se apresentar os efeitos antes da escolha aumenta a compreensão sem prolongar o tempo de resposta quando o contexto de uso é adverso (HIP-06). O produto deve mostrar erro de conexão claro e orientar tentativa novamente, sem presumir funcionamento offline; a confirmação e o prazo de validade são verificados pelo servidor. Isso exige teste com protótipo.

---

## 6. O que ainda precisa de pesquisa

- Frequência e contexto de recebimento do alerta (campo, madrugada, balcão).
- O que o associado faz primeiro quando não reconhece uma compra (liga, ignora, responde no app, pede ajuda a alguém).
- Qual resposta gera mais dúvida ou medo de consequência negativa.
- Se a distinção entre "recusa da compra" e "bloqueio do cartão" é compreendida sem explicação.
- Se o associado entende que pode ainda responder à confirmação após pedir atendimento.

Ver `roteiro_pesquisa.md` para as perguntas correspondentes.
