# Registro de Evidências e Hipóteses — Pacote Pessoa 2

**ID do registro:** EH-P2-v0.1  
**Versão:** 0.1 · 28/10/2026  
**Responsável:** Pessoa 2  
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
| FON-02 | `docs/direcional_entregas.md` em `origin/develop` | Hash `8942cc5` · 27/10/2026 | §D02, §D03, §D06: estrutura, partes, como produzir, aceite | Guia de produção, não evidência de pesquisa | D02, D03, D06 |
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

**Links Box das aulas** (tentativa de acesso em 27/10/2026 registrada no Direcional, sem retorno de conteúdo):  
- Empatia: `https://ibm.box.com/s/bsp0u5ozqqhh69jcpnhsk9kh5bzx9ogd`  
- Cenário atual: `https://ibm.box.com/s/j3b67flksbx0uvjijgl041iqe9njj63p`  
- Persona/cenários: `https://ibm.box.com/s/piv01ht7gm9a4c12vq5w6iv1rowumnaf`  

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

Nenhuma observação de campo disponível nesta versão. A seção será preenchida após execução do `roteiro_pesquisa.md`.

---

## Resultados de teste

Nenhum teste executado até esta versão. A seção será preenchida após validação com protótipo (D12/D13, responsabilidade Pessoa 4 com moderação Pessoa 2).

---

## Como atualizar este registro após a pesquisa

1. Adicionar entradas `OBS-xx` com: participante anonimizado, perfil pertinente, data, contexto/versão, relato ou tarefa, observação literal, interpretação e hipótese relacionada.
2. Atualizar o estado das hipóteses: **sustentada neste recorte**, **contestada** ou **inconclusiva**.
3. Não alterar o conteúdo de `FON-xx` e `DEC-xx` retroativamente; criar novas entradas se a decisão mudar.
4. Limitar a conclusão ao contexto da coleta: uma resposta hipotética ou preferência declarada não equivale a comportamento observado.
