# Personas (proto-personas)

> Tipo: **proto-personas** (Nielsen Norman Group), feitas a partir do briefing da Trilha 4 (Sicredi), do dicionário de dados do case e do que sabemos do domínio. São **hipóteses**: precisam ser validadas com Sponsor Users (ver `premissas-e-perguntas.md`).
> Formato do curso (sessão de DT do Saulo): objetivo, frustração, contexto de decisão, estado de sucesso e relação com o sistema. Nada de detalhe decorativo.

---

## Persona 1 · Camila Rocha, analista de prevenção a fraudes

| | |
|---|---|
| **Quem** | 31 anos, analista pleno na central de prevenção a fraudes de uma cooperativa de crédito. 4 anos na área. Trabalha em turnos, em duas telas. |
| **Objetivo** | Decidir rápido e com segurança se um cartão sob suspeita deve ser bloqueado, sem travar o associado que está comprando de verdade. |
| **Frustração** | A fila tem centenas de alertas por turno e quase todos são legítimos (no case, só 0,1% das transações é fraude). O score do motor de regras não diz *por quê*. Para entender um caso ela abre 4 ou 5 sistemas (transações, cadastro, dispositivo, geolocalização, histórico de contato) e escreve a justificativa à mão. |
| **Contexto de decisão** | Tem minutos por alerta, SLA de atendimento e meta de perda evitada. A fraude se concentra em **crédito com cartão não presente**, em rajadas rápidas, de madrugada, longe de onde o associado costuma estar e com valores fora do padrão. |
| **Estado de sucesso** | Abre a fila já ordenada por risco × valor, vê em uma tela os fatores que explicam o risco e a recomendação do agente, aciona o associado com um clique e registra a decisão com justificativa gerada. |
| **Relação com o Watson** | Usuária diária e intensa (*power user*). Quer atalhos, densidade de informação e controle final da decisão: o agente recomenda, ela decide. |
| **Frase** | "Não me dá só um número. Me mostra o que está estranho nessa compra." |

**Implicações de design**
- Fila densa e ordenável (tabela de dados Carbon), com nível de risco por cor **e** texto.
- Explicabilidade: lista de fatores com peso, linguagem de negócio, sem jargão de modelo.
- Ações principais visíveis no topo do caso; decisão sempre humana (*human-in-the-loop*).
- Justificativa da decisão pré-preenchida pelo agente e editável (trilha de auditoria).

---

## Persona 2 · Valdir Bortolini, associado

| | |
|---|---|
| **Quem** | 58 anos, produtor rural no oeste de Santa Catarina, associado da cooperativa há 20 anos. Usa o cartão de crédito para insumos e, de vez em quando, compra pela internet. Usa o celular para WhatsApp e o app do banco, com ajuda da filha. |
| **Objetivo** | Comprar sem susto e saber na hora se algo estranho aconteceu com o cartão dele, sem precisar ligar para ninguém. |
| **Frustração** | Já teve o cartão bloqueado numa compra grande e legítima de insumos e passou vergonha no balcão. Recebe ligações dizendo ser "do banco" e não sabe em quem confiar. Mensagens com termos técnicos o deixam inseguro. |
| **Contexto de decisão** | Recebe o alerta a qualquer hora, inclusive de madrugada, muitas vezes no campo e com sinal fraco. Precisa entender em segundos o que aconteceu. |
| **Estado de sucesso** | Vê no app uma mensagem clara (valor, loja, cidade, horário), responde "Fui eu" ou "Não reconheço" com um toque, e recebe a confirmação de que o cartão está protegido e de que nada foi cobrado. |
| **Relação com o Watson** | Não usa o console; vive o Watson pelo **alerta preventivo** no app. Uso esporádico, baixa familiaridade digital, precisa de texto grande e linguagem simples. |
| **Frase** | "Se for golpe, me avisa direito. E se fui eu, não me trava." |

**Implicações de design**
- Mensagem com valor, estabelecimento, cidade e horário antes de qualquer pergunta.
- Dois botões grandes e explícitos; nada de links para clicar fora do app.
- Sinal de confiança: lembrar que a cooperativa nunca pede senha ou código por telefone.
- Estado final tranquilizador e com o próximo passo (novo cartão, contestação).

---

### Por que duas personas
Elas são as duas pontas do mesmo fluxo: a **Camila** decide no console e o **Valdir** confirma no app. O agente Watson coordena as duas (arquétipos *guardião de tomada de decisão*, *redutor de carga cognitiva* e *gestor de fronteiras entre humanos e IA*, do guia da IBM).
