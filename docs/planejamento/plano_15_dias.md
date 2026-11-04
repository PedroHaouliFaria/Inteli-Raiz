# Plano operacional por entregas ÔÇö Inteli-Raiz

**Revis├úo de 28/10/2026 ┬À Quatro pessoas ┬À Confirma├º├úo de compras pelo associado.**

O nome `plano_15_dias.md` foi mantido para preservar os links existentes. A organiza├º├úo vigente ├® por entregas e depend├¬ncias. A janela de 15 dias, a equipe de cinco pessoas e as estimativas de horas da proposta anterior n├úo s├úo compromissos atuais. Datas e disponibilidade precisam ser combinadas pela equipe.

**Objetivo:** entregar uma prova de conceito de IA ag├¬ntica que ajude o associado a entender e responder a uma compra sinalizada, com resultado registrado e revis├úo humana das exce├º├Áes. Dados e a├º├Áes financeiras s├úo simulados.

## 1. Como usar os documentos

| Documento | Papel |
|---|---|
| [Plano de implementa├º├úo](../../docs/plano_implementacao.md) | Define produto, pol├¡tica, estados, contratos, requisitos e testes |
| [Direcional das entregas](../../docs/direcional_entregas.md) | Explica D01ÔÇôD13: conte├║do, produ├º├úo, revis├úo, fontes e crit├®rios de qualidade |
| [Backlog](backlog.md) | Transforma o plano em cards C01ÔÇôC32, com respons├íveis e depend├¬ncias |
| [Cat├ílogo dos materiais](artefatos_materiais_contexto.md) | Identifica entregas recomendadas e pacote obrigat├│rio da IBM |

Este documento organiza a execu├º├úo; n├úo substitui o detalhamento dos requisitos ou das entregas. Os cards s├úo planejamento e n├úo evid├¬ncia de implementa├º├úo conclu├¡da.

## 2. Fluxo e limites do produto

1. Uma compra sint├®tica ├® recebida e avaliada pela ferramenta de risco.
2. Uma pol├¡tica determin├¡stica e versionada decide libera├º├úo simulada, solicita├º├úo de confirma├º├úo ou revis├úo de exce├º├úo.
3. O associado v├¬ a compra, seus detalhes e o motivo verific├ível da solicita├º├úo.
4. O associado pode reconhecer e autorizar, n├úo reconhecer ou informar d├║vida. A conversa ajuda a esclarecer contexto; a resposta expl├¡cita acontece pelo controle humano previsto.
5. O backend valida sess├úo, v├¡nculo da compra, vers├úo, validade e repeti├º├úo; persiste resposta, a├º├úo e status.
6. Sem resposta, a confirma├º├úo expira sem autoriza├º├úo presumida. Falta de contexto ou falha de servi├ºo gera tratamento expl├¡cito e revis├úo quando aplic├ível.

O agente consulta informa├º├Áes e solicita revis├úo. Ele n├úo autoriza em nome do associado. Recusar a compra n├úo equivale a bloquear automaticamente todo o cart├úo. O analista participa das exce├º├Áes; uma mesa completa de an├ílise n├úo faz parte do recorte.

**Interface:** aproveitar o React + Carbon do Watson (`watson/frontend`, PR #7). Leonardo adapta e integra a tela do associado, com apoio do backend no contrato e de produto/pesquisa nos textos e na experi├¬ncia. C10/C13/C18/C27 est├úo ativos. A interface deve comprovar sess├úo, v├¡nculo da compra, resposta humana expl├¡cita e resultado persistido. Um chat de texto livre sozinho n├úo atende a esses requisitos. A exist├¬ncia do prot├│tipo n├úo comprova integra├º├úo.

**Ajuda e resposta:** ÔÇ£Estou em d├║vidaÔÇØ registra `UNSURE` e leva a `REVISAO_PENDENTE`. ÔÇ£Quero falar com algu├®mÔÇØ abre ou reaproveita uma revis├úo sem responder nem encerrar uma confirma├º├úo ainda v├ílida; o prazo original continua correndo. O frontend deve mostrar a├º├Áes distintas e o backend persistir os eventos correspondentes.

**Prioridade:** caminho completo, contexto fiel, persist├¬ncia, testes e experi├¬ncia compreens├¡vel. Segundo modelo, dashboards, telas decorativas, RAG ou m├║ltiplos agentes s├│ entram depois, com necessidade demonstrada. Integra├º├úo banc├íria real, bloqueio efetivo e streaming produtivo permanecem fora do escopo.

## 3. Divis├úo em quatro pessoas

Usar Pessoa 1ÔÇô4 at├® a equipe informar os nomes. Esses r├│tulos n├úo reaproveitam automaticamente os cinco nomes do planejamento anterior.

| Pessoa | Lideran├ºa | Apoio e revis├úo | Pacote final |
|---|---|---|---|
| Pessoa 1 | D01 Oportunidades; D04 Prioriza├º├úo; D05 Conceito; D07 Ideia; D08 Valor/IA | Revisa empatia/persona; mant├®m escopo e narrativa coerentes | Texto de problema/solu├º├úo e roteiro de apresenta├º├úo |
| Pessoa 2 | D02 Empatia; D03 Cen├írio Atual; D06 Persona e Cen├írios | Apoia pesquisa, linguagem, prot├│tipo e modera├º├úo; revisa D12/D13 | Confere narrativa do usu├írio, achados e limites |
| Pessoa 3 | D09 Estrutura; D10 Arquitetura | Consolida contratos, dados/modelo e estado real das integra├º├Áes; revisa D04/D08/D11 | Declara├º├úo tecnol├│gica e instru├º├Áes t├®cnicas |
| Pessoa 4 | D11 Registro do Fluxo; D12 Prot├│tipo; D13 Valida├º├úo | Organiza reprodu├º├úo, evid├¬ncias, testes e corre├º├Áes com os autores | V├¡deo, ├¡ndice, links e confer├¬ncia de acesso |

A [matriz por entrega](../../docs/direcional_entregas.md#organiza├º├úo-em-quatro-pessoas-respons├íveis-sequ├¬ncia-e-revis├úo) define o revisor principal e o resultado para aceite. Liderar o documento n├úo significa desenvolver sozinho os componentes associados. Pessoa 3 coordena a defini├º├úo dos executores t├®cnicos; cada card de implementa├º├úo s├│ fica pronto para iniciar quando executor e revisor com compet├¬ncia t├®cnica estiverem identificados. Pessoa 4 registra e testa o fluxo entregue pelos autores t├®cnicos.

Para o frontend Watson, Leonardo j├í ├® o executor t├®cnico; Pessoa 4 mant├®m a consolida├º├úo de D12/D11/D13, Pessoa 2 revisa usabilidade e Pessoa 3 apoia integra├º├úo. Essa atribui├º├úo espec├¡fica n├úo redefine a identidade das quatro fun├º├Áes.

Cada integrante entrega suas pr├│prias evid├¬ncias do IBM Bob. O l├¡der cadastrado na plataforma realiza o envio, independentemente da fun├º├úo documental acima.

## 4. Sequ├¬ncia por depend├¬ncia

| Etapa | Trabalho | Evid├¬ncia para avan├ºar |
|---|---|---|
| Descoberta | Pessoas 1 e 2 produzem D01ÔÇôD03; Pessoa 3 verifica acessos/contratos; Pessoa 4 prepara esbo├ºo e teste | Problema, contexto, fontes, hip├│teses e depend├¬ncias identificados |
| Escolha e valor | Pessoa 1 facilita D04 e consolida D05/D07/D08; Pessoa 2 fecha D06 | Alternativas comparadas, persona funcional e valor/IA justificados |
| Estrutura e prot├│tipo | Pessoa 3 fecha D09/D10; Pessoa 4 refina D12 com Pessoa 2 | Requisitos, estados, contratos e resposta humana expl├¡cita compat├¡veis |
| Implementa├º├úo e integra├º├úo | Autores t├®cnicos implementam backend/modelo; Leonardo adapta e integra o frontend Watson em C10/C13; Pessoa 4 prepara D11 | Mesma compra rastre├ível pelos componentes, tr├¬s respostas e ajuda separada, inclusive em falha |
| Valida├º├úo e melhoria | Pessoa 4 consolida D13, Pessoa 2 modera e autores corrigem | Observa├º├Áes, m├®tricas, corre├º├Áes e reteste documentados |
| Consolida├º├úo | As quatro pessoas fecham declara├º├Áes, v├¡deo, links e Bob | Evid├¬ncias e acesso conferidos na mesma vers├úo candidata |

Contratos e exemplos sint├®ticos identificados permitem trabalho paralelo. Prot├│tipo de design permite testar compreens├úo antes da aplica├º├úo integrada. O teste final de D11/D13 deve registrar qual vers├úo e qual ambiente foram usados.

## 5. Cuidados de dados e modelo preservados

O planejamento anterior registrou uma c├│pia local com 160.000 linhas, 297 colunas e 146 positivos em `feedback_label`, apesar da refer├¬ncia a 900.000 linhas no nome/orienta├º├Áes. Esses n├║meros s├úo um registro da confer├¬ncia anterior, n├úo uma nova execu├º├úo nesta revis├úo. Reproduzir as contagens e identificar a vers├úo da base antes de publicar m├®tricas.

Verifica├º├Áes necess├írias, relacionadas aos cards C04, C05, C11 e C16:

- Confirmar alvo, per├¡odo, aus├¬ncias, tipos e positivos por parti├º├úo. Auditar disponibilidade temporal de `fraud`, `fraud_score`, `decision`, disputas e feedbacks antes de aprovar preditores.
- Reconciliar o manifesto de 28 features com documentos que mencionam 31; alinhar defini├º├úo de madrugada, nulos, categorias e ordem das classes entre treino e infer├¬ncia.
- Ajustar preparo e limiar na valida├º├úo; preservar avalia├º├úo final independente. O teste j├í consultado para escolha de limiar ├® explorat├│rio.
- Comparar o candidato com uma baseline e com/sem as quatro features de velocidade pr├®-calculadas. M├®tricas perfeitas na base sint├®tica exigem investiga├º├úo.
- Declarar a conven├º├úo de PR-AUC/average precision; registrar precision, recall, falsos positivos, matriz de confus├úo e volume de alertas no limiar escolhido.
- Versionar pr├®-processamento, atributos, modelo, pol├¡tica e contrato. Chamar score de probabilidade calibrada apenas com avalia├º├úo que sustente essa interpreta├º├úo.

O [plano ┬º7](../../docs/plano_implementacao.md) e a [documenta├º├úo do modelo](../../docs/03_modelo.md) orientam esse trabalho. Qualquer alternativa por regras precisa de identifica├º├úo, pol├¡tica pr├│pria e declara├º├úo honesta na demonstra├º├úo.

## 6. Marcos de revis├úo e crit├®rios de corte

| Marco | Crit├®rio de passagem | A├º├úo diante de pend├¬ncia |
|---|---|---|
| Recorte revisado | D01ÔÇôD08 coerentes, com evid├¬ncias ou hip├│teses identificadas | Investigar a hip├│tese que pode mudar a escolha antes de expandir |
| Contratos e interface vi├íveis | Contrato e frontend Watson compat├¡veis com sess├úo, resposta expl├¡cita, ajuda e estados | Priorizar adapta├º├úo/integra├º├úo do c├│digo existente |
| Primeira integra├º├úo | Compra ÔåÆ avalia├º├úo ÔåÆ pol├¡tica ÔåÆ confirma├º├úo ÔåÆ resposta ÔåÆ persist├¬ncia | Concentrar executores no caminho; adiar recursos adicionais |
| Vers├úo candidata | Modelo/pol├¡tica/contrato identificados; cen├írios cr├¡ticos executados | Abrir corre├º├Áes com dono e preservar rastreabilidade |
| Valida├º├úo revisada | D13 com achados, corre├º├Áes e retestes; sem falha cr├¡tica aberta | Corrigir e repetir o cen├írio afetado antes da grava├º├úo final |
| Envio | Outra pessoa reproduz; v├¡deo, declara├º├Áes, links e Bob conferidos | Resolver acesso/vers├úo e guardar confirma├º├úo da plataforma |

N├úo transportar estimativas de horas da equipe de cinco pessoas. Acordar disponibilidade das quatro pessoas e esfor├ºo por card, reservando espa├ºo para integra├º├úo e corre├º├úo. O crit├®rio principal de corte ├® preservar o fluxo seguro e compreens├¡vel e o pacote obrigat├│rio.

## 7. Gest├úo e conclus├úo

- Quadro: **Backlog ÔåÆ Pronto para iniciar ÔåÆ Em andamento ÔåÆ Em revis├úo ÔåÆ Conclu├¡do**. Registrar impedimento, respons├ível por destravar e pr├│ximo passo.
- Um respons├ível e um revisor diferentes por entrega; crit├®rios e evid├¬ncias determinam o aceite.
- Reuni├Áes curtas acompanham resultado, pr├│ximo compromisso e depend├¬ncia. Limitar atividades simult├óneas e ajudar nas revis├Áes quando houver espera.
- Registrar mudan├ºas de contrato e atualizar consumidores, documenta├º├úo e evid├¬ncias na mesma vers├úo.
- Para pesquisa: fonte e implica├º├úo; para design: percurso e estados; para neg├│cio: premissas e evid├¬ncia; para programa├º├úo: execu├º├úo e verifica├º├Áes relevantes.

O [direcional](../../docs/direcional_entregas.md) relaciona as entregas aos quatro crit├®rios IBM. As tarefas recomendadas apoiam a qualidade; checkpoint e envio final continuam sendo as entregas obrigat├│rias, conforme o guia. Conferir situa├º├úo, campos e prazo vigente na plataforma antes da submiss├úo.

## 8. Correspond├¬ncia com a proposta anterior

Os c├│digos A01ÔÇôA12 deixam de orientar o quadro vigente. A correspond├¬ncia abaixo preserva o prop├│sito das atividades ├║teis; n├úo comprova conclus├úo nem migra automaticamente os crit├®rios do recorte antigo.

| Refer├¬ncia anterior | Destino no planejamento vigente |
|---|---|
| A01 Pesquisa/oportunidades | D01, D04 e base de pesquisa de D02/D03 |
| A02 Jornada/hist├│rias | D02, D03, D06 e requisitos do associado em D09 |
| A03 Valor/viabilidade | D08 e seus cen├írios de custo/ado├º├úo |
| A04 Dados e A07 Modelo | Insumos de D09/D10/D11; C04, C05, C11, C16 e C25 |
| A05 Arquitetura/contratos | D09/D10 |
| A06 Prot├│tipo | D12, agora centrado na compra e resposta do associado |
| A08 Agente/backend | Implementa├º├úo necess├íria a D10/D11, com pol├¡tica externa e autoriza├º├úo humana |
| A09 Front-end pr├│prio | Adapta├º├úo e integra├º├úo do frontend Watson por Leonardo; C10/C13/C18/C27 ativos, com consolida├º├úo de Pessoa 4 |
| A10 Valida├º├úo | D13, com teste de compreens├úo e corre├º├Áes |
| A11 Reprodu├º├úo | D11, C28 e declara├º├úo tecnol├│gica |
| A12 Pacote final | C23 e C29ÔÇôC32; divis├úo entre quatro pessoas no direcional |
