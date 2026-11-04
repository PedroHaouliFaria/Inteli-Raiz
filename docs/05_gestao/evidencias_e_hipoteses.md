# Registro único de evidências, hipóteses e decisões

**Revisão:** 04/11/2026. IDs FON/HIP/DEC e FON-P1/HIP-P1/DEC-P1 preservados para rastreabilidade. Fontes com hash descrevem aquele momento histórico. O estado atual é registrado na matriz de aceite e nos artefatos D09–D12. Nenhuma entrevista foi criada nesta revisão.

## Pesquisa e decisões de experiência

### Registro de origem — pesquisa

**ID do registro:** EH-P2-v0.1\
**Versão:** 0.1 · 28/10/2026\
**Responsável:** Pesquisa\
**Estado:** rascunho — sem observações de campo; todo conteúdo é documental ou hipotético.

Este arquivo é o ponto único de rastreabilidade para D02, D03 e D06. Cada entrada usa um ID estável. As entregas referenciam esses IDs em vez de repetir a fonte.

---

## Prefixos de ID

| Prefixo | Tipo |
|---|---|
| `FON-xx` | Fonte documental — caminho/URL, versão e seção |
| `HIP-xx` | Hipótese — comportamento, dor ou contexto ainda não validado |
| `DEC-xx` | Decisão de revisão documental — motivo e fonte que a sustenta |
| `OBS-xx` | Observação real — somente quando houver registro de pesquisa fornecido |
| `TST-xx` | Resultado de teste efetivamente executado, com procedimento e versão |

---

## Fontes documentais

| ID | Origem e localização | Versão / data | Seção relevante | Limite de uso | Entregas relacionadas |
|---|---|---|---|---|---|
| FON-01 | `docs/plano_implementacao.md` em `origin/develop` | Hash `8942cc5` · 28/10/2026 | §§1–3: produto, fluxo, três respostas; §4: arquitetura; §5: estados; §9: testes | Plano governa comportamento futuro; não é evidência de uso do produto | D02, D03, D06 |
| FON-02 | `artefatos/documentacao/direcional_entregas.md` em `origin/develop` | Hash `8942cc5` · 27/10/2026 | §D02, §D03, §D06: estrutura, partes, como produzir, aceite | Guia de produção, não evidência de pesquisa | D02, D03, D06 |
| FON-03 | `artifacts/planejamento/backlog.md` em `origin/develop` | Hash `8942cc5` · 28/10/2026 | C03, C09, C10, C15, C18, C21, C24, C27: consumidores da pesquisa | Planejamento não executado | D02, D03, D06 |
| FON-04 | `docs/design/00-descoberta/personas.md` em `origin/watson` | Hash `212655c` · data não declarada no arquivo | Valdir Bortolini (Persona 2): objetivo, frustração, contexto, estado de sucesso, relação com o Watson | Proto-persona: hipótese do Leonardo, não entrevista executada | D02, D06 |
| FON-05 | `docs/design/00-descoberta/mapas-de-empatia.md` em `origin/watson` | Hash `212655c` | Mapa do Valdir: Diz/Pensa/Faz/Sente; dor central | Hipótese; cada post-it declarado como hipótese pelo próprio autor | D02 |
| FON-06 | `docs/design/00-descoberta/cenario-as-is.md` em `origin/watson` | Hash `212655c` | Jornada do Valdir: 5 etapas (cartão usado → ligação ignorada → bloqueio → central → novo cartão) | Cenário hipotético construído a partir do briefing do case; não confirmado com associados ou Sicredi | D03 |
| FON-07 | `docs/design/00-descoberta/premissas-e-perguntas.md` em `origin/watson` | Hash `212655c` | Premissas com certeza baixa/média; Sponsor Users sugeridos; roteiro de entrevista do associado | Premissas, não evidências; certeza "média" não equivale a fato | D02, D03, D06 |
| FON-08 | `docs/design/00-descoberta/hills-e-pov.md` em `origin/watson` | Hash `212655c` | POV Valdir; HMW; Hills 2 e 3 (metas 30 s e 2 min) | Metas de Hill são aspirações de design, não resultados observados | D03, D06 |
| FON-09 | `contexto/First DT Session deck.pdf` | PDF local | pp.28 (empatia), 47 (jornada 4–6 etapas), 60 (entregas) | Orientação metodológica da aula; não específica ao Sicredi | D02, D03 |
| FON-10 | `contexto/Updated_Second Session DT and AI Agents_BR_Saulo (1) (1).pdf` | PDF local | p.47 (persona funcional); p.63 (entregas) | Orientação metodológica | D06 |
| FON-11 | `contexto/2026 AI Experiential Learning Lab with Bob - Industry Challenges_Portuguese.pdf` | PDF local | p.6: desafio Sicredi — alerta preventivo e confirmação pelo associado | Descrição do desafio; não detalha fluxo interno do Sicredi | D03, D06 |
| FON-12 | `contexto/2H26 GuideBob_IBM SkillsBuild_AI Experiential Learning Lab BR.pdf` | PDF local | pp.13–14 (rubrica); pp.30–31 (evidências do Bob) | Critérios de avaliação, não de produto | Todos |

**Links Box das aulas** (tentativa de acesso em 27/10/2026 registrada no Direcional, sem retorno de conteúdo):\

- Empatia: `https://ibm.box.com/s/bsp0u5ozqqhh69jcpnhsk9kh5bzx9ogd`\

- Cenário atual: `https://ibm.box.com/s/j3b67flksbx0uvjijgl041iqe9njj63p`\

- Persona/cenários: `https://ibm.box.com/s/piv01ht7gm9a4c12vq5w6iv1rowumnaf`\

Os campos internos dos templates Box não foram verificados nesta tarefa. As estruturas dos artefatos seguem o Direcional (FON-02) e as aulas (FON-09/FON-10), que são verificáveis localmente.

---

## Hipóteses

| ID | Descrição | Origem | Estado / limite | Implicação para o design | Entregas | Como verificar |
|---|---|---|---|---|---|---|
| HIP-01 | O associado pode confundir "não reconheço" com "bloquear o cartão inteiro" | FON-04 (persona Valdir); FON-01 §3 ("Não bloquear o cartão inteiro automaticamente") | Hipótese de comportamento — não confirmada | Exibir explicitamente que a compra é recusada e a revisão é aberta; não dizer "cartão bloqueado" | D02, D06 | Tarefa "não reconheço" no roteiro + pergunta: "O que aconteceu com seu cartão?" |
| HIP-02 | O associado pode não saber se pode ainda responder depois de pedir atendimento | FON-01 §3: "Se ela ainda estiver válida e pendente, o associado continua podendo escolher" | Hipótese derivada da regra; comportamento do usuário não confirmado | Mostrar status da confirmação como "ainda aberta" quando o atendimento é solicitado antes de uma resposta | D02, D06 | Pergunta de compreensão: "Você ainda poderia responder à pergunta sobre a compra depois de pedir ajuda?" |
| HIP-03 | O associado pode não reconhecer o nome do estabelecimento na fatura mesmo em compra legítima | FON-04 (Valdir usa cartão para insumos); FON-05 (Diz: "Não fui eu que comprei isso!") | Hipótese plausível; não confirmada por entrevista | Mostrar estabelecimento/categoria disponível e comunicar quando não há vínculo verificável, sem inventar | D02, D03, D06 | Pergunta: "O nome que aparece aqui faz sentido para você?" |
| HIP-04 | O associado recebe mensagens de golpe imitando o banco e desconfia do canal | FON-04 (Valdir ignora ligações de número desconhecido); FON-05 (Pensa: "Será que essa mensagem é golpe?") | Hipótese proposta por Leonardo a partir da protopersona e do mapa de empatia (FON-04/FON-05), ainda não validada com associados. Frequência, contexto e impacto precisam ser investigados na pesquisa | Mostrar claramente que a mensagem veio do app autenticado; incluir aviso de que ninguém da cooperativa pede resposta por telefone | D02, D03 | Pergunta: "Como você sabia que essa mensagem era legítima?" |
| HIP-05 | O associado não sabe qual consequência cada resposta tem antes de escolher | FON-01 §3 (três respostas com efeitos distintos); FON-05 (Faz: "Abre o app só quando recebe notificação") | Hipótese de lacuna de compreensão — não confirmada | Mostrar breve descrição do que acontece após cada botão antes da escolha | D02, D06 | Pergunta: "O que acontece se você tocar em 'Estou em dúvida'?" |
| HIP-06 | O associado está sob pressão de tempo quando recebe o alerta (campo, sinal fraco, balcão) | FON-04 (contexto: madrugada, campo, sinal fraco) | Hipótese de contexto — não confirmada por entrevista; não sustenta adicionar capacidade offline ao MVP | Tratamento claro de falha de conexão: mostrar erro, orientar tentativa novamente e preservar o status da confirmação verificado pelo servidor; mensagem objetiva sem textos longos | D02, D03 | Pergunta: "Onde você estava quando recebeu a mensagem? Tinha como responder ali?" |
| HIP-07 | O associado prefere resolver pelo app a ligar para a central | FON-07 (premissa com certeza "média") | Hipótese com certeza média do Leonardo; não confirmada | Oferecer resposta completa no app; pedido de atendimento como opção, não obrigação | D02, D06 | Pergunta: "Se você tivesse uma dúvida sobre a compra, o que faria primeiro — responderia no app ou ligaria?" |
| HIP-08 | O bloqueio do cartão descoberto no balcão é a fricção mais frequente na jornada atual | FON-06 (cenário as-is do Valdir: etapa 3); FON-04 (frustração: "passou vergonha no balcão") | Hipótese construída a partir do briefing; não confirmada pela Sicredi ou por entrevista | Demonstrar claramente que o produto atual não bloqueia o cartão inteiro automaticamente | D03 | Pergunta a especialista do domínio: "Qual é o processo atual de bloqueio e em que casos ele ocorre?" |
| HIP-09 | O associado não sabe o que acontece depois que responde — se a compra foi "resolvida" | FON-04 (estado de sucesso desejado: "receber a confirmação"); FON-01 §2 (tela mostra status) | Hipótese sobre necessidade de confirmação pós-resposta | Mostrar status claro (liberada, recusada, em revisão, expirada) e próximo passo após a resposta | D02, D06 | Pergunta: "O que apareceu na tela depois que você respondeu?" / tarefa de pós-ação |

---

## Decisões documentais

| ID | Descrição | Fonte / regra que motivou | Efeito nos artefatos |
|---|---|---|---|
| DEC-01 | Valdir é o protagonista dos três documentos; Camila aparece apenas nas exceções | FON-01 §1 ("Associado é o usuário principal"); PR #8 | D02 centra-se no associado; D03 é a jornada do associado; D06 tem Valdir como persona principal |
| DEC-02 | O produto prevê três respostas (AUTHORIZE / DENY / UNSURE) e pedido de atendimento separado — não dois botões | FON-01 §§1 e 3; PR #8 decisão 3 | D02 e D06 cobrem as quatro situações; D06 tem seis cenários |
| DEC-03 | Biometria e verificação de aparelho novo foram excluídas do MVP | FON-01 §4 decisão 4 | D06 não inclui biometria no cenário futuro; anti-persona não é transportada para este pacote |
| DEC-04 | Não prometer bloqueio automático do cartão inteiro, estorno, novo cartão ou cartão bloqueado | FON-01 §3 ("Não bloquear o cartão inteiro automaticamente") | D06 cenário "Não reconheço" descreve recusa simulada e revisão, não bloqueio |
| DEC-05 | Pedir atendimento não responde à confirmação nem prorroga o prazo | FON-01 §3 ("Pedir ajuda não é responder à confirmação") | D02 e D06 distinguem ajuda de resposta; D06 cobre o cenário de atendimento |
| DEC-06 | Confirmação expirada não presume autorização | FON-01 §1 (CONFIRMACAO_EXPIRADA) e §3 | D06 cobre o cenário de expiração |
| DEC-07 | O agente não autoriza em nome do associado | FON-01 §3 e §6 ("responder_confirmacao é operação do backend acessível à sessão humana") | D06 cenário futuro deixa explícito que a resposta é do associado |
| DEC-08 | Dados sintéticos e ações simuladas não podem aparecer como efeitos financeiros reais | FON-01 §6 R11 ("Dados fictícios e ações simuladas aparecem no produto e na demo") | D06 identifica ações como simuladas |
| DEC-09 | A jornada atual (D03) é hipótese investigável, não descrição confirmada do Sicredi; o agente informa o limite quando não há vínculo verificável entre nomes em vez de inventar informação | FON-06 (cenário as-is do Leonardo como ponto de partida); FON-11 (desafio Sicredi descreve o problema sem detalhar processo interno); FON-01 §2 ("Se não existir relação verificável entre nomes, informa que não consegue confirmar") | D03 usa status "hipótese"; D06 tabela de comparação usa este ID para justificar comportamento do agente diante de nome de estabelecimento sem vínculo verificável |

---

## Observações reais

Nenhuma observação de campo disponível nesta versão. A seção será preenchida após execução do [roteiro de pesquisa](../02_ux_design/roteiro_pesquisa.md).

---

## Resultados de teste

Nenhum teste executado até esta versão. A seção será preenchida após validação com protótipo (D12/D13, responsabilidade Integração e validação com moderação Pesquisa).

---

## Como atualizar este registro após a pesquisa

1. Adicionar entradas `OBS-xx` com: participante anonimizado, perfil pertinente, data, contexto/versão, relato ou tarefa, observação literal, interpretação e hipótese relacionada.
2. Atualizar o estado das hipóteses: **sustentada neste recorte**, **contestada** ou **inconclusiva**.
3. Não alterar o conteúdo de `FON-xx` e `DEC-xx` retroativamente; criar novas entradas se a decisão mudar.
4. Limitar a conclusão ao contexto da coleta: uma resposta hipotética ou preferência declarada não equivale a comportamento observado.


## Produto e viabilidade

### Registro de origem — produto

**ID do registro:** EH-P1-v0.1
**Versão:** 0.1 · 03/11/2026
**Responsável:** Produto
**Estado:** rascunho — sem observações de campo; todo conteúdo é documental ou hipotético.

Esta seção preserva os IDs novos do registro original de Produto. Os IDs da Pesquisa (`FON-01` a `FON-12`, `HIP-01` a `HIP-09`, `DEC-01` a `DEC-09`) são utilizados por referência em D01, D04, D05, D07 e D08; as fontes/hipóteses originais estão na seção anterior deste mesmo documento.

---

## Prefixos de ID

| Prefixo | Tipo |
|---|---|
| `FON-P1-xx` | Fonte documental nova, não registrada pela Pesquisa |
| `HIP-P1-xx` | Hipótese nova gerada pela análise de produto/negócios |
| `DEC-P1-xx` | Decisão de produto/narrativa registrada por Produto |

---

## Fontes documentais (novas)

| ID | Origem e localização | Versão / data | Seção relevante | Limite de uso | Entregas relacionadas |
|---|---|---|---|---|---|
| FON-P1-01 | `contexto/2026 AI Experiential Learning Lab with Bob - Industry Challenges_Portuguese.pdf` | PDF local | p.6: desafio Sicredi — "alerta preventivo e confirmação pelo associado"; arquétipos pp.7–10 | Descrição do desafio e arquétipos; não detalha fluxo interno do Sicredi nem confirma demanda de adoção | D01, D08 |
| FON-P1-02 | `artefatos/D09_estrutura_solucao.md` | v0.1 · 29/10/2026 | §2 (saber/decidir/fazer), §4 (requisitos R01–R12), §5 (critérios de sucesso) | Rascunho da Arquitetura; não revisado; PR-AUC documentado = 0,146, meta 0,80 não atingida | D05, D08 |
| FON-P1-03 | `artefatos/D10_arquitetura.md` | v0.1 · 29/10/2026 | §4 (ficha do agente), §5 (catálogo de ferramentas), §7 (política e máquina de estados) | Rascunho; componentes em estado "Planejado"; deploy watsonx.ai concluído como evidência, não como runtime | D05, D08 |
| FON-P1-04 | `artefatos/D12_prototipo_experiencia.md` | v0.1 · 28/10/2026 | Percurso de confirmação, mapa de telas/estados, textos candidatos | Revisado documentalmente; frontend não integrado à API naquele registro histórico; atualizado em D12 (PEN-01/PEN-03 da Integração e validação) | D05, D07 |
| FON-P1-05 | `artefatos/D11_fluxo_mvp.md` | v0.1 · 28/10/2026 | Casos P4-T01 a T12, pré-condições e cenários | Rascunho bloqueado por integração; sem execução ponta a ponta verificada | D08 |

---

## Hipóteses (novas — geradas pela análise de produto)

| ID | Descrição | Origem | Estado / limite | Implicação para produto/narrativa | Entregas | Como verificar |
|---|---|---|---|---|---|---|
| HIP-P1-01 | A instituição financeira adotaria o produto se ele reduzisse o esforço de atendimento em casos de dúvida sobre compras | FON-P1-01 (desafio menciona objetivo de reduzir fraudes e melhorar experiência); sem confirmação de interesse da Sicredi | Hipótese de adoção — não confirmada; decisor interno não identificado | Separar "associado usa o produto" de "instituição decide adotar"; não afirmar interesse comercial; registrar como premissa investigável | D08 | Entrevista ou alinhamento com mentor/orientador; benchmarks de volume de chamadas evitadas |
| HIP-P1-02 | A premissa mais frágil da direção escolhida é que o associado compreende a diferença entre recusar a compra e bloquear o cartão inteiro, sem instrução prévia | HIP-01 (Pesquisa); D02 §3 (tensão central de compreensão) | Hipótese de compreensão — ponto mais arriscado do fluxo de confirmação | Se falsa, toda a proposta de valor muda: precisaríamos de um canal de instrução antes da tela, não do fluxo atual | D04, D08 | Tarefa "não reconheço" com pergunta: "O que aconteceu com seu cartão?" (roteiro D13) |
| HIP-P1-03 | O valor principal para a instituição é a redução de contatos de atendimento por dúvida, não a redução direta de perdas por fraude | FON-P1-01 p.6; plano §2 "hipótese de valor e limite" | Hipótese de valor organizacional — não medida | Em D08, separar "hipótese de redução de atendimento" de "redução de perdas financeiras"; a segunda não é verificável neste MVP | D08 | Comparar número de casos com e sem resolução autônoma no piloto; não extrapolar para perdas financeiras |
| HIP-P1-04 | O custo de IA por confirmação é dominado pelo número de mensagens de chat trocadas por caso — casos sem dúvida contextual (autorização direta) geram custo mínimo | FON-P1-03 §7 (agente só é chamado quando há dúvida contextual); plano §4 (agente com LLM externo) | Hipótese de viabilidade — não calculada; custo por chamada de API não levantado | Construir tabela de premissas com cenário conservador (todas as confirmações geram chat) e base (x% geram chat) | D08 | Instrumentar o piloto para contar mensagens de chat por caso |
| HIP-P1-05 | Uma alternativa sem agente (confirmação com texto fixo) seria suficiente para casos onde o associado reconhece imediatamente a compra, mas insuficiente para o caso de nome de estabelecimento ambíguo | D02 §3 (tensão de reconhecimento); D03 §4 (ruptura: canal incerto + informação insuficiente); D10 §4 (ficha do agente) | Hipótese comparativa — sustenta a justificativa de necessidade de IA em D04/D08 | O agente deve demonstrar valor exatamente no caso ambíguo; se o piloto mostrar que o texto fixo resolve bem, essa hipótese cai e a justificativa de IA precisa ser revisada | D04, D08 | Alternância de fluxo básico × agente no piloto (D13) |

---

## Decisões de produto (Produto)

| ID | Descrição | Fonte / regra que motivou | Efeito nos artefatos |
|---|---|---|---|
| DEC-P1-01 | O recorte de D01 é confirmação de compras pelo associado — não prevenção completa de fraudes, não mesa de análise | FON-01 §1 (mudança de produto); FON-P1-01 p.6 (desafio Sicredi) | D01 não inclui detecção em tempo real nem bloqueio automático como entregáveis do MVP |
| DEC-P1-02 | A direção vencedora em D04 é Alternativa B (ajuda contextual com agente), como revisão da decisão já tomada no plano; registrada com a mesma base de critérios que avalia as alternativas A e C | FON-01 §2 e §8.1 (escolha já no plano); direcional §D04 ("registrar como revisão da decisão se a discussão ocorrer depois") | D04 registra a decisão como revisão, não como resultado de brainstorming executado; a seção de discussão em grupo fica como roteiro pendente |
| DEC-P1-03 | Em D08, o valor das transações sinalizadas não é tratado como perda evitada; os números de premissas ficam marcados como `[a definir]` até que haja fonte verificável | Plano §9 ("valor das transações sinalizadas não equivale a perdas evitadas"); direcional §D08 | D08 não afirma redução de perdas; usa hipóteses mensuráveis com fonte explícita ou marcação `[a definir]` |
| DEC-P1-04 | Os arquétipos do desafio (especialista sensível ao contexto; gestor da fronteira humano–IA) são tratados como interpretação candidata, não como classificação definitiva | FON-P1-01 pp.7–10 (arquétipos); direcional §D08 ("marcar como interpretação a confirmar pelo comportamento executado") | D08 apresenta os arquétipos com explicitação de que são interpretações a confirmar |


## Registro desta consolidação — 04/11/2026

| ID | Tipo | Origem | Achado / decisão | Limite | Entregas |
|---|---|---|---|---|---|
| FON-REV-01 | Código | develop f741a35; API, client.js, PurchaseDetail e agente | Sessão, três respostas, revisão e chat implementados | Presença de código não é validação com usuários | D05, D07, D09–D12 |
| DEC-REV-01 | Organização | Solicitação de consolidação | Fonte única em artefatos/, por D01–D13, responsáveis por função | Sem alteração dos IDs históricos | Todas |
| DEC-REV-02 | Comparação | Direcional D04/D08 e protocolo D13 | A/B usam mesmos dados; IA não recebe vantagem por existir | Vantagem depende do piloto | D04, D08, D13 |
| HIP-REV-01 | Viabilidade | D08 §4 | Volumes/tokens/tempo ilustrativos para cálculo base/conservador | Sem preços ou volumes reais da instituição | D08 |
| TST-REV-01 | Teste executado | Log pytest no índice de evidências | 207 passed, 1 warning; código f741a35 | Não usa LLM externo real nem testa interface por humano | D09–D11 |

HIP-P1-02 permanece compreensão de recusa versus bloqueio; a hipótese de vantagem do agente é HIP-P1-05. IDs não são intercambiáveis. Fontes datadas de 28/10 são históricas e não diagnosticam o frontend atual.
