# Backlog ÔÇö Confirma├º├úo de compras pelo associado

**Revis├úo de 28/10/2026 ┬À Quatro pessoas ┬À Planejamento ainda n├úo executado.**

O [plano operacional](plano_15_dias.md) define recorte e sequ├¬ncia. O [direcional](../../docs/direcional_entregas.md) detalha D01ÔÇôD13 e sua matriz de respons├íveis/revisores. P1ÔÇôP4 significam Pessoa 1ÔÇô4. Os nomes ser├úo preenchidos pela equipe, sem reaproveitar automaticamente a forma├º├úo antiga de cinco integrantes.

Os IDs C01ÔÇôC32 foram preservados, mas descri├º├Áes, depend├¬ncias e responsabilidades foram revistas para o associado. Os c├│digos A antigos t├¬m correspond├¬ncia no plano operacional. Os **32 cards est├úo ativos e em Backlog**; C10, C13, C18 e C27 foram reativados para adaptar e integrar o frontend Watson j├í produzido por Leonardo no PR #7. Isso n├úo significa que o c├│digo foi integrado ou validado. Datas ser├úo acordadas ap├│s estimar esfor├ºo e disponibilidade; D01ÔÇôD13 s├úo IDs de entregas, n├úo dias do calend├írio.

Respons├ível ├® quem acompanha a conclus├úo e consolida a evid├¬ncia. Nos cards de implementa├º├úo, P3 coordena a escolha dos executores t├®cnicos e revisores habilitados; essa aloca├º├úo ├® requisito para iniciar e n├úo atribui todo o desenvolvimento a P3. Prot├│tipo de design e implementa├º├úo de front-end pr├│prio s├úo trabalhos distintos.

Leonardo ├® o executor t├®cnico definido para adaptar o frontend existente. P4 consolida D12 e as evid├¬ncias da experi├¬ncia; P2 revisa linguagem/usabilidade e P3 apoia contrato/integra├º├úo. Essa atribui├º├úo n├úo redefine os demais nomes de P1ÔÇôP4. Pedir atendimento e registrar `UNSURE` s├úo opera├º├Áes distintas, conforme ┬º3 do plano.

## 1. Descoberta, contratos e primeira integra├º├úo

| Card | Entrega | Atividade e evid├¬ncia para concluir | Respons├ível | Revisor | Depend├¬ncia |
|---|---|---|---|---|---|
| C01 | D01 | Registrar problema, associado priorit├írio, fontes, hip├│teses e perguntas de pesquisa | P1 | P2 | Nenhuma |
| C02 | D01/D04 | Comparar alternativas, reunir achados e publicar decis├úo de prioridade com crit├®rios | P1 | P3 | C01; achados de C03 para fechar |
| C03 | D02/D03/D06 | Produzir empatia, jornada atual e persona; comparar atual/futuro e manter fontes/hip├│teses | P2 | P1 | C01 inicial; C02 para cen├írio futuro final |
| C04 | D09/D10 | Reproduzir contagens da base, alvo, aus├¬ncias e tipos; registrar vers├úo e diverg├¬ncia 900k/160k | P3 | P4, com revis├úo t├®cnica dos n├║meros | Nenhuma; executor t├®cnico definido |
| C05 | D09/D10 | Auditar disponibilidade temporal, features, madrugada, nulos, classes e parti├º├Áes com positivos | P3 | Outro autor t├®cnico a definir | C04 |
| C06 | D10/D11 | Comprovar acesso ao Bob, execu├º├úo do backend/modelo local e configura├º├úo do LLM; conferir viabilidade da interface Watson com sess├úo, compra e resposta expl├¡cita | P3 | P4 | Nenhuma; executor t├®cnico definido |
| C07 | D09/D10 | Publicar arquitetura, contratos, estados e exemplos de compra/an├ílise/confirma├º├úo/resposta/erro | P3 | P4 | C01 inicial, C04 inicial; C06 para fechar viabilidade |
| C08 | D05/D07/D08 | Consolidar conceito, ideia e valor/IA com ado├º├úo, custos e hip├│teses declarados | P1 | P3 | C01, C02 inicial, C03 inicial |
| C09 | D12 | Revisar o prot├│tipo existente: compra, alerta, tr├¬s respostas e ajuda separada; incluir erro e expira├º├úo | P4 | P2 | C03 inicial, C07 inicial |
| C10 | D12/Frontend Watson | Adaptar React + Carbon existente para o associado: tr├¬s respostas, atendimento separado, estados e console de exce├º├Áes; sem promessa de bloqueio do cart├úo ou biometria obrigat├│ria | P4; execu├º├úo: Leonardo | P2 | C09, C07; c├│digo do PR #7 dispon├¡vel |
| C11 | D09/D11 | Executar baseline/candidato inicial com atributos aprovados e avalia├º├úo de valida├º├úo reproduz├¡vel | P3 | Outro autor t├®cnico a definir | C05 |
| C12 | D10/D11 | Implementar ferramentas, pol├¡tica, persist├¬ncia e resposta humana autenticada; demonstrar isolamento de fun├º├Áes | P3 | Outro autor t├®cnico a definir | C06, C07; avalia├º├úo inicial de C11 |
| C13 | D10/D11/D12 | Integrar frontend Watson ├á API: sess├úo, detalhe/status da compra, resposta idempotente, chat e pedido de revis├úo; substituir mocks no fluxo principal e demonstrar estado ap├│s recarga | P4; execu├º├úo: Leonardo, com backend | P3 | C10, C12, C06 |
| C14 | D11 | Reproduzir primeira integra├º├úo: compra ÔåÆ pol├¡tica ÔåÆ confirma├º├úo ÔåÆ resposta ÔåÆ estado persistido | P4 | P3 | C06, C11, C12, C13 |

**Revis├úo da primeira integra├º├úo:** verificar estados, v├¡nculo da compra, resposta expl├¡cita e chamadas reais. Enquanto C06 n├úo comprovar uma interface compat├¡vel, registrar a depend├¬ncia; um chat sem controle humano seguro n├úo conclui C14.

## 2. Avalia├º├úo e vers├úo candidata

| Card | Entrega | Atividade e evid├¬ncia para concluir | Respons├ível | Revisor | Depend├¬ncia |
|---|---|---|---|---|---|
| C15 | D13 | Conduzir primeira rodada no prot├│tipo ou MVP; registrar perfil, vers├úo, tarefas e dificuldades | P4, com P2 na modera├º├úo | P2 | C09; C14 quando avaliar a aplica├º├úo integrada |
| C16 | D09/D11 | Avaliar candidato/limiar na valida├º├úo, comparar baseline e features de velocidade; registrar avalia├º├úo final independente e limites | P3 | Outro autor t├®cnico a definir | C11 |
| C17 | D10/D11 | Tratar dados ausentes, falhas, expira├º├úo e resposta duplicada/concorrente; comprovar explica├º├úo fiel | P3 | Outro autor t├®cnico a definir | C12, C14 |
| C18 | D12/D13/Frontend Watson | Corrigir textos, navega├º├úo, teclado/foco e estados a partir do teste; comprovar que atendimento n├úo responde ├á compra nem prorroga o prazo | P4; execu├º├úo: Leonardo | P2 | C13, C15 |
| C19 | D08 | Atualizar custos e valor com cen├írios conservador/base e resultados dispon├¡veis; separar hip├│tese de medi├º├úo | P1 | P3 | C08; C15/C16 para incorporar resultados |
| C20 | D10/D11 | Integrar pacote versionado de modelo/preparo/pol├¡tica e conferir respostas humanas, estados e persist├¬ncia | P3 | Outro autor t├®cnico a definir | C16, C17 |
| C21 | D06/D12 | Revisar prot├│tipo e experi├¬ncia implementada contra a jornada; registrar textos e pend├¬ncias | P4 | P2 | C09, C18, C20 |
| C22 | D09/D10/D11 | Identificar vers├úo candidata: dados, features, modelo, pol├¡tica, contratos e interface | P3 | P4 | C20, C21 |
| C23 | Pacote final | Criar ├¡ndice e roteiro de tr├¬s minutos, distribuindo trechos e evid├¬ncias pelas quatro pessoas | P1 | P4 | C19 inicial, C21 |

**Revis├úo da candidata:** evid├¬ncias devem corresponder ao mesmo fluxo e ├ás mesmas vers├Áes. Priorizar corre├º├Áes; recursos adicionais n├úo entram automaticamente.

## 3. Valida├º├úo final, reprodu├º├úo e envio

| Card | Entrega | Atividade e evid├¬ncia para concluir | Respons├ível | Revisor | Depend├¬ncia |
|---|---|---|---|---|---|
| C24 | D13 | Completar teste de compreens├úo e matriz requisito/teste/evid├¬ncia; comparar fluxo b├ísico/agente e retestar ajustes | P4, com P2 na modera├º├úo | P2 | C22, C15 |
| C25 | D09/D11 | Executar verifica├º├Áes cr├¡ticas de dados/modelo na candidata e anexar resultados reproduz├¡veis | P3 | Outro autor t├®cnico a definir | C22 |
| C26 | D10/D11/D13 | Corrigir/revalidar integra├º├úo, acesso cruzado, autoriza├º├úo, expira├º├úo, duplica├º├úo, falhas e persist├¬ncia | P3; autores corrigem suas partes | P4; revis├úo t├®cnica quando necess├íria | C22; achados de C24 |
| C27 | D11/D12/D13/Frontend Watson | Corrigir e retestar a interface na candidata: tr├¬s respostas, ajuda separada, expira├º├úo, conflitos, falha do chat e recarga; guardar resultados da vers├úo corrigida | P4; execu├º├úo: Leonardo | P2, com P3 na integra├º├úo | C22; achados de C24 |
| C28 | D11/Pacote final | Documentar execu├º├úo, tecnologias e limites; P4 reproduz o guia produzido por P3 | P3 | P4 | C22, C25, C26, C27 para aceite |
| C29 | Pacote final | Conferir evid├¬ncias do Bob das quatro pessoas e consolidar ├¡ndice/links; cada uma fornece suas capturas | P4 | P3 | Capturas de cada integrante ao longo do trabalho |
| C30 | D07/D08/Pacote final | Fechar declara├º├Áes de problema/solu├º├úo e narrativa com resultados, fontes e limites | P1 | P2 | C19, C23, C24 |
| C31 | Pacote final | Gravar/editar v├¡deo de tr├¬s minutos na candidata; todos fornecem os trechos acordados | P4 | P1 | C24ÔÇôC30 |
| C32 | Pacote final | Conferir acesso, links, v├¡deo e vers├Áes; entregar ao l├¡der formal e guardar confirma├º├úo de envio | P4; envio pelo l├¡der cadastrado | P1 | C28ÔÇôC31 |

**Revis├úo de envio:** reproduzir a demonstra├º├úo, verificar permiss├Áes e conferir a plataforma. C32 conclui com confirma├º├úo do envio, n├úo com a exist├¬ncia de um rascunho.

## Regras de uso do quadro

1. Manter IDs C01ÔÇôC32; associar cada card ├ás entregas D correspondentes e aos requisitos do plano.
2. Registrar executor t├®cnico e revisor habilitado antes de iniciar cards de implementa├º├úo; distribuir trabalho conforme compet├¬ncia e disponibilidade.
3. Vers├Áes iniciais permitem preparar trabalho dependente; registrar o que precisa estar fechado para o aceite.
4. Anexar resultado, evid├¬ncia, vers├úo e revis├úo. N├úo marcar integra├º├úo como conclu├¡da por existir apenas um mock ou diagrama.
5. Corrigir o documento afetado junto da mudan├ºa de decis├úo/contrato. Reabrir testes atingidos.
6. Usar C10/C13/C18/C27 para adaptar, integrar e validar o frontend Watson existente. N├úo declarar o fluxo integrado com mocks; C14 depende de C13 e o aceite final inclui C27.

## Modelo para copiar ao criar um card

```text
ID / t├¡tulo:
Entregas Dxx / requisitos Rxx:
Respons├ível pela entrega:
Executor(es), quando houver implementa├º├úo:
Revisor:
Prazo acordado:
Objetivo:
Entradas e depend├¬ncias:
Resultado esperado:
Crit├®rios de aceite:
Evid├¬ncia / link / vers├úo / commit:
Impedimento e a├º├úo:
Estado:
```
