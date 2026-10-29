# Backlog — Confirmação de compras pelo associado

**Revisão de 28/10/2026 · Quatro pessoas · Planejamento ainda não executado.**

O [plano operacional](plano_15_dias.md) define recorte e sequência. O [direcional](../../docs/direcional_entregas.md) detalha D01–D13 e sua matriz de responsáveis/revisores. P1–P4 significam Pessoa 1–4. Os nomes serão preenchidos pela equipe, sem reaproveitar automaticamente a formação antiga de cinco integrantes.

Os IDs C01–C32 foram preservados, mas descrições, dependências e responsabilidades foram revistas para o associado. Os códigos A antigos têm correspondência no plano operacional. Os **32 cards estão ativos e em Backlog**; C10, C13, C18 e C27 foram reativados para adaptar e integrar o frontend Watson já produzido por Leonardo no PR #7. Isso não significa que o código foi integrado ou validado. Datas serão acordadas após estimar esforço e disponibilidade; D01–D13 são IDs de entregas, não dias do calendário.

Responsável é quem acompanha a conclusão e consolida a evidência. Nos cards de implementação, P3 coordena a escolha dos executores técnicos e revisores habilitados; essa alocação é requisito para iniciar e não atribui todo o desenvolvimento a P3. Protótipo de design e implementação de front-end próprio são trabalhos distintos.

Leonardo é o executor técnico definido para adaptar o frontend existente. P4 consolida D12 e as evidências da experiência; P2 revisa linguagem/usabilidade e P3 apoia contrato/integração. Essa atribuição não redefine os demais nomes de P1–P4. Pedir atendimento e registrar `UNSURE` são operações distintas, conforme §3 do plano.

## 1. Descoberta, contratos e primeira integração

| Card | Entrega | Atividade e evidência para concluir | Responsável | Revisor | Dependência |
|---|---|---|---|---|---|
| C01 | D01 | Registrar problema, associado prioritário, fontes, hipóteses e perguntas de pesquisa | P1 | P2 | Nenhuma |
| C02 | D01/D04 | Comparar alternativas, reunir achados e publicar decisão de prioridade com critérios | P1 | P3 | C01; achados de C03 para fechar |
| C03 | D02/D03/D06 | Produzir empatia, jornada atual e persona; comparar atual/futuro e manter fontes/hipóteses | P2 | P1 | C01 inicial; C02 para cenário futuro final |
| C04 | D09/D10 | Reproduzir contagens da base, alvo, ausências e tipos; registrar versão e divergência 900k/160k | P3 | P4, com revisão técnica dos números | Nenhuma; executor técnico definido |
| C05 | D09/D10 | Auditar disponibilidade temporal, features, madrugada, nulos, classes e partições com positivos | P3 | Outro autor técnico a definir | C04 |
| C06 | D10/D11 | Comprovar acesso ao Bob, execução do backend/modelo local e configuração do LLM; conferir viabilidade da interface Watson com sessão, compra e resposta explícita | P3 | P4 | Nenhuma; executor técnico definido |
| C07 | D09/D10 | Publicar arquitetura, contratos, estados e exemplos de compra/análise/confirmação/resposta/erro | P3 | P4 | C01 inicial, C04 inicial; C06 para fechar viabilidade |
| C08 | D05/D07/D08 | Consolidar conceito, ideia e valor/IA com adoção, custos e hipóteses declarados | P1 | P3 | C01, C02 inicial, C03 inicial |
| C09 | D12 | Revisar o protótipo existente: compra, alerta, três respostas e ajuda separada; incluir erro e expiração | P4 | P2 | C03 inicial, C07 inicial |
| C10 | D12/Frontend Watson | Adaptar React + Carbon existente para o associado: três respostas, atendimento separado, estados e console de exceções; sem promessa de bloqueio do cartão ou biometria obrigatória | P4; execução: Leonardo | P2 | C09, C07; código do PR #7 disponível |
| C11 | D09/D11 | Executar baseline/candidato inicial com atributos aprovados e avaliação de validação reproduzível | P3 | Outro autor técnico a definir | C05 |
| C12 | D10/D11 | Implementar ferramentas, política, persistência e resposta humana autenticada; demonstrar isolamento de funções | P3 | Outro autor técnico a definir | C06, C07; avaliação inicial de C11 |
| C13 | D10/D11/D12 | Integrar frontend Watson à API: sessão, detalhe/status da compra, resposta idempotente, chat e pedido de revisão; substituir mocks no fluxo principal e demonstrar estado após recarga | P4; execução: Leonardo, com backend | P3 | C10, C12, C06 |
| C14 | D11 | Reproduzir primeira integração: compra → política → confirmação → resposta → estado persistido | P4 | P3 | C06, C11, C12, C13 |

**Revisão da primeira integração:** verificar estados, vínculo da compra, resposta explícita e chamadas reais. Enquanto C06 não comprovar uma interface compatível, registrar a dependência; um chat sem controle humano seguro não conclui C14.

## 2. Avaliação e versão candidata

| Card | Entrega | Atividade e evidência para concluir | Responsável | Revisor | Dependência |
|---|---|---|---|---|---|
| C15 | D13 | Conduzir primeira rodada no protótipo ou MVP; registrar perfil, versão, tarefas e dificuldades | P4, com P2 na moderação | P2 | C09; C14 quando avaliar a aplicação integrada |
| C16 | D09/D11 | Avaliar candidato/limiar na validação, comparar baseline e features de velocidade; registrar avaliação final independente e limites | P3 | Outro autor técnico a definir | C11 |
| C17 | D10/D11 | Tratar dados ausentes, falhas, expiração e resposta duplicada/concorrente; comprovar explicação fiel | P3 | Outro autor técnico a definir | C12, C14 |
| C18 | D12/D13/Frontend Watson | Corrigir textos, navegação, teclado/foco e estados a partir do teste; comprovar que atendimento não responde à compra nem prorroga o prazo | P4; execução: Leonardo | P2 | C13, C15 |
| C19 | D08 | Atualizar custos e valor com cenários conservador/base e resultados disponíveis; separar hipótese de medição | P1 | P3 | C08; C15/C16 para incorporar resultados |
| C20 | D10/D11 | Integrar pacote versionado de modelo/preparo/política e conferir respostas humanas, estados e persistência | P3 | Outro autor técnico a definir | C16, C17 |
| C21 | D06/D12 | Revisar protótipo e experiência implementada contra a jornada; registrar textos e pendências | P4 | P2 | C09, C18, C20 |
| C22 | D09/D10/D11 | Identificar versão candidata: dados, features, modelo, política, contratos e interface | P3 | P4 | C20, C21 |
| C23 | Pacote final | Criar índice e roteiro de três minutos, distribuindo trechos e evidências pelas quatro pessoas | P1 | P4 | C19 inicial, C21 |

**Revisão da candidata:** evidências devem corresponder ao mesmo fluxo e às mesmas versões. Priorizar correções; recursos adicionais não entram automaticamente.

## 3. Validação final, reprodução e envio

| Card | Entrega | Atividade e evidência para concluir | Responsável | Revisor | Dependência |
|---|---|---|---|---|---|
| C24 | D13 | Completar teste de compreensão e matriz requisito/teste/evidência; comparar fluxo básico/agente e retestar ajustes | P4, com P2 na moderação | P2 | C22, C15 |
| C25 | D09/D11 | Executar verificações críticas de dados/modelo na candidata e anexar resultados reproduzíveis | P3 | Outro autor técnico a definir | C22 |
| C26 | D10/D11/D13 | Corrigir/revalidar integração, acesso cruzado, autorização, expiração, duplicação, falhas e persistência | P3; autores corrigem suas partes | P4; revisão técnica quando necessária | C22; achados de C24 |
| C27 | D11/D12/D13/Frontend Watson | Corrigir e retestar a interface na candidata: três respostas, ajuda separada, expiração, conflitos, falha do chat e recarga; guardar resultados da versão corrigida | P4; execução: Leonardo | P2, com P3 na integração | C22; achados de C24 |
| C28 | D11/Pacote final | Documentar execução, tecnologias e limites; P4 reproduz o guia produzido por P3 | P3 | P4 | C22, C25, C26, C27 para aceite |
| C29 | Pacote final | Conferir evidências do Bob das quatro pessoas e consolidar índice/links; cada uma fornece suas capturas | P4 | P3 | Capturas de cada integrante ao longo do trabalho |
| C30 | D07/D08/Pacote final | Fechar declarações de problema/solução e narrativa com resultados, fontes e limites | P1 | P2 | C19, C23, C24 |
| C31 | Pacote final | Gravar/editar vídeo de três minutos na candidata; todos fornecem os trechos acordados | P4 | P1 | C24–C30 |
| C32 | Pacote final | Conferir acesso, links, vídeo e versões; entregar ao líder formal e guardar confirmação de envio | P4; envio pelo líder cadastrado | P1 | C28–C31 |

**Revisão de envio:** reproduzir a demonstração, verificar permissões e conferir a plataforma. C32 conclui com confirmação do envio, não com a existência de um rascunho.

## Regras de uso do quadro

1. Manter IDs C01–C32; associar cada card às entregas D correspondentes e aos requisitos do plano.
2. Registrar executor técnico e revisor habilitado antes de iniciar cards de implementação; distribuir trabalho conforme competência e disponibilidade.
3. Versões iniciais permitem preparar trabalho dependente; registrar o que precisa estar fechado para o aceite.
4. Anexar resultado, evidência, versão e revisão. Não marcar integração como concluída por existir apenas um mock ou diagrama.
5. Corrigir o documento afetado junto da mudança de decisão/contrato. Reabrir testes atingidos.
6. Usar C10/C13/C18/C27 para adaptar, integrar e validar o frontend Watson existente. Não declarar o fluxo integrado com mocks; C14 depende de C13 e o aceite final inclui C27.

## Modelo para copiar ao criar um card

```text
ID / título:
Entregas Dxx / requisitos Rxx:
Responsável pela entrega:
Executor(es), quando houver implementação:
Revisor:
Prazo acordado:
Objetivo:
Entradas e dependências:
Resultado esperado:
Critérios de aceite:
Evidência / link / versão / commit:
Impedimento e ação:
Estado:
```
