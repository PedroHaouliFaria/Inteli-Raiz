# Plano revisado · Confirmação de compras

**Versão 2.3 · 28/10/2026 · Substitui a direção de produto do plano centrado no analista.**

> **Mudança de 27/10: sem IBM Cloud em tempo de execução.** O orientador comunicou que o watsonx Orchestrate não está funcionando para muitos grupos e que a obrigatoriedade do IBM Cloud foi revogada. **Só o IBM Bob continua obrigatório.** O produto, a jornada, as regras e os contratos deste plano não mudam. Muda onde o agente e o modelo rodam: os dois passam para o nosso backend. As decisões técnicas estão no §4.

**Complemento de execução:** o [Direcional de entregas — Da descoberta à confirmação de compras](direcional_entregas.md) detalha as 11 entregas recomendadas dos slides, com títulos, partes, passo a passo, fontes/templates, responsáveis por função e critérios de qualidade. Inclui prototipação e validação como apoio. A versão PDF disponível corresponde à v2 de 23/10/2026; as adições de entregas estão nesta versão Markdown e no direcional.

## 1. A mudança e o fluxo final

**O produto agora é um assistente para o associado confirmar compras suspeitas.** O sistema toma a decisão inicial sobre o tratamento da transação. O associado responde se reconhece e autoriza a compra. O analista entra nas exceções.

| Antes | Agora |
|---|---|
| Analista era o usuário principal. | Associado é o usuário principal. |
| Agente sugeria uma ação ao analista. | Sistema decide liberar ou solicitar confirmação, conforme política experimental. |
| Analista confirmava o encaminhamento de cada caso. | Associado confirma ou recusa a compra sinalizada. |
| Front era uma mesa de análise. | Front mostra uma compra, explica o alerta e pede uma resposta. |
| Sucesso era apoiar a análise. | Sucesso é concluir a confirmação com clareza e registrar o resultado correto. |

### Fluxo que vamos construir

**1. Compra recebida → 2. Modelo avalia → 3. Sistema define o tratamento.**

- **Elegível para liberação automática:** registrar `LIBERADA_SIMULACAO`.
- **Precisa de confirmação:** apresentar a compra ao associado.
- **Avaliação impossível ou caso fora da política:** registrar exceção; não liberar automaticamente.

**4. Associado responde à compra sinalizada:**

- **“Reconheço e autorizo” → liberar na simulação.**
- **“Não reconheço” → recusar na simulação e abrir encaminhamento de proteção.**
- **“Estou em dúvida” → manter pendente de revisão.**
- **Não responde até expirar → encerrar como confirmação expirada, sem autorização presumida.**

**5. Sistema registra a resposta, a ação e o status.** Nenhuma transação, bloqueio ou comunicação financeira real será executada pelo protótipo.

<!--page-->

## 2. Ideia de negócio e experiência principal

### O que vamos apresentar

“Vamos construir um assistente de confirmação de compras para associados. Ao identificar uma compra que precisa de verificação, o sistema mostra seus detalhes, explica o alerta e permite autorizar, recusar ou pedir ajuda. A resposta gera um encaminhamento registrado, com análise humana nas exceções.”

O modelo participa da decisão inicial. Sua classificação é transformada em tratamento por uma política explícita, testável e versionada. O agente conversa e aciona ferramentas; não pode substituir a política por uma opinião em texto livre.

### A tela principal

| Área | O que o associado vê |
|---|---|
| Compra | Estabelecimento ou identificação disponível, valor, data e cartão sintético parcialmente identificado. |
| Alerta | Motivo da confirmação, escrito com base em sinais realmente disponíveis. |
| Pergunta | “Você reconhece e autoriza esta compra?” |
| Respostas | “Reconheço e autorizo”, “Não reconheço”, “Estou em dúvida”. |
| Ajuda | Campo para dúvidas sobre a compra e o processo. |
| Resultado | Confirmação recebida, compra recusada, revisão pendente ou confirmação expirada. |

**Exemplo de conversa:** o associado pergunta “Pode ser o nome da empresa que aparece na fatura?”. O agente consulta o contexto disponível. Se não existir relação verificável entre nomes, informa que não consegue confirmar e mantém a opção de revisão. Não inventa a identidade do estabelecimento.

### Hipótese de valor e limite

O associado pode entender o alerta e responder sem depender de um atendimento completo. Precisamos verificar compreensão, conclusão e erros. Ainda não há evidência de redução de fraudes ou perdas reais.

O desafio Sicredi inclui explicitamente alerta preventivo e confirmação de compras pelo associado [C, p.6]. Essa direção atende a essa inspiração. A estrutura de envio e a rubrica do GuideBob continuam iguais [G, pp.13–14].

<!--page-->

## 3. Regras de decisão que viram código

### Saídas da avaliação inicial

| Condição | Decisão do sistema | Status |
|---|---|---|
| Entrada válida, avaliação disponível e critério de liberação atendido | Liberar automaticamente na simulação. | `LIBERADA_SIMULACAO` |
| Critério de confirmação atendido | Criar solicitação individual de confirmação. | `AGUARDANDO_ASSOCIADO` |
| Dados críticos ausentes, serviço falha ou caso não coberto | Encaminhar para revisão; não inventar score. | `REVISAO_PENDENTE` |

Limiar e critérios devem ser definidos na validação, não escolhidos para produzir uma demo bonita. Os valores 0,30 e 0,80 do plano anterior deixam de ser regras assumidas. Sem evidência para liberação automática, iniciar o piloto com todos os casos avaliados elegíveis enviados à confirmação; identificar essa política como conservadora e experimental.

### Resposta do associado

| Evento válido | Ação implementada |
|---|---|
| Reconhece e autoriza, antes da expiração | Registrar autorização e liberação simulada. |
| Não reconhece | Registrar recusa e abrir um caso de proteção/revisão. Não bloquear o cartão inteiro automaticamente. |
| Está em dúvida | Registrar dúvida e abrir revisão; compra não recebe autorização por isso. |
| Confirmação expira | Impedir aprovação por aquele desafio; mostrar status e caminho de revisão. |
| Resposta repetida | Retornar o resultado já registrado, sem duplicar ação. |
| Resposta a outra compra ou versão antiga | Rejeitar e pedir que o associado abra a solicitação correta. |

**Pedir ajuda não é responder à confirmação.** “Quero falar com alguém” abre ou reaproveita uma revisão, mas não registra `UNSURE` nem encerra a confirmação. Se ela ainda estiver válida e pendente, o associado continua podendo escolher uma das três respostas. O prazo continua correndo; pedir atendimento não prorroga a validade. Já “Estou em dúvida” registra explicitamente `UNSURE` e leva a compra a `REVISAO_PENDENTE`.

**Aprovar compra não é declarar ausência de fraude.** Recusar compra não é aprovar automaticamente bloqueio de cartão. O protótipo mantém esses eventos separados.

O associado responde por um controle de interface vinculado à sua sessão. O agente não consegue gerar a autorização em nome dele. Respostas livres podem ajudar a conversa, mas não executam liberação sem confirmação explícita no controle previsto.

<!--page-->

## 4. Arquitetura ajustada

**Compra sintética → ferramenta de avaliação → política → solicitação de confirmação → interface do associado → resposta autenticada → ação simulada e histórico.**

| Componente | Função |
|---|---|
| Modelo no backend | Produzir score/classificação com versão e schema conhecidos, carregando `outputs/modelo_rf.joblib` no próprio processo. |
| Política no backend | Decidir tratamento inicial e aplicar transições de estado. |
| Agente no backend | Consultar contexto, explicar sinais, esclarecer dúvidas e solicitar revisão, com Pydantic AI e um LLM externo. |
| Front do associado | Experiência principal da demo. Mostrar uma compra, coletar resposta explícita e apresentar status; consome só a API JSON. React + Carbon, em `watson/frontend`. |
| Backend | FastAPI + SQLAlchemy sobre SQLite, em `watson/backend`. Validar sessão, vincular associado e compra, controlar expiração, persistir e evitar duplicação. |
| Visão de exceções | O console da analista do Watson (fila e caso), limitado aos casos que precisam de humano. Não é uma mesa antifraude completa. |
| Bob IDE | Construção, revisão, testes e documentação, com evidências por integrante. |

### Ferramentas e operações

- `avaliar_transacao(case_id)`: score, origem, sinais, lacunas e versões.
- `consultar_compra(case_id)`: contexto permitido ao usuário da sessão; sem rótulo de avaliação.
- `consultar_status(case_id)`: estado atual e próximos passos permitidos.
- `solicitar_revisao(case_id, reason)`: cria exceção e retorna protocolo.
- `responder_confirmacao(challenge_id, response, version)`: **operação do backend acessível à sessão humana, não uma ferramenta de autorização do agente**.

O front consome o estado persistido. Não extrai decisão do texto do chat. Uma explicação do agente não altera estado por si só.

A conversa fica no próprio front, chamando um endpoint de chat do backend que já sabe qual compra e qual associado estão na sessão. Se o LLM falhar, a conversa mostra o erro e o caminho explícito de confirmação continua funcionando. Nunca substituir o agente real por respostas fixas sem indicar simulação.

### Decisões técnicas de 27/10

| Tema | Decisão | Por quê |
|---|---|---|
| Modelo | Roda no backend a partir do `joblib` (Python 3.12, scikit-learn 1.6, pandas 2.2). | Elimina chave da IBM Cloud, cota Lite e deploy ocioso; o score é idêntico ao do deploy. |
| watsonx.ai | O deploy de 27/10 fica como evidência de que o modelo roda em nuvem; a chamada continua disponível como `score_source=watsonx`. | O teste 7.1 da [spec de integração](specs/teste_integracao_orchestrate_wml.md) passou; ninguém depende dele em tempo de execução. |
| Backend | FastAPI + SQLAlchemy sobre SQLite, no `watson/backend`, expondo só API JSON. | Mesmo processo do modelo; SQLite atende R06 e R10 com volume durável. Atualizado em 28/10 (ver abaixo). |
| Contrato | Escrito antes do código, com exemplos de resposta. | O front começa com dados falsos sem esperar o backend (etapa 2). |
| Front | React + Carbon, no `watson/frontend`. | Escolha de quem implementa (Leo); o backend não depende dela, porque só expõe JSON. |
| Agente | Pydantic AI com LLM de plano gratuito (Groq ou Gemini); um provedor pago só se alguém do grupo tiver crédito; Granite no watsonx.ai como opção se houver chave funcionando. | Trocar de provedor é configuração. O associado chega às ferramentas por injeção de dependência, não por argumento que o LLM preenche (R05, R09). |
| Ferramentas do agente | `avaliar_transacao`, `consultar_compra`, `consultar_status`, `solicitar_revisao`. Nenhuma autoriza ou recusa. | Mantém a regra do §3: só o controle da interface responde pelo associado. |
| Identidade | Login fictício com 2 ou 3 associados identificados como fictícios e cookie de sessão assinado. | Atende R05 e o §5 sem fingir autenticação bancária. |
| Bob | O código novo é escrito no Bob, com sessões exportadas em `bob_sessions/<nome>/`. | É a única exigência da IBM que permanece. |

### Alinhamento com o Watson (28/10)

O PR #7 (aplicação Watson, do Leo) e este plano apontavam para produtos diferentes. Em 28/10 o grupo aceitou as recomendações da [pauta de alinhamento](https://claude.ai/artifact/L5BArsjDT4RY3PGtAb1s5R). Elas valem sobre as decisões 0001–0004 de `docs/arquitetura/decisoes/`, que passam a ser propostas incorporadas aqui.

| # | Tema | Decisão |
|---|---|---|
| 1 | Usuário principal | O associado. A tela de confirmação conduz o vídeo; o console da analista do Watson vira a visão de exceções. Quadro, dicionário e Laboratório do modelo saem do caminho da demo. |
| 2 | Política inicial | Todo caso avaliado vai para a confirmação (§3). A `NoticePolicy` do Watson mantém os limiares configuráveis, desligados até uma validação fora do conjunto de teste. |
| 3 | Respostas | `AUTHORIZE` ("Reconheço e autorizo"), `DENY` ("Não reconheço") e `UNSURE` ("Estou em dúvida"). As duas primeiras substituem `it_was_me` e `not_me`; `talk_to_person` é pedido de atendimento separado, não equivalente a `UNSURE`. Pedir ajuda abre revisão sem responder nem encerrar a confirmação válida. "Não reconheço" registra a recusa simulada e abre revisão; a tela não diz que o cartão foi bloqueado. |
| 4 | Biometria e aparelho | Fora do MVP: a base não tem esses dados. Uma etapa de digital na tela, se ficar, aparece como simulação e não muda a regra. |
| 5 | Rajada | `cp_card_term_vel_1h` aparece como o dicionário do case define ("velocidade sintética por cartão/terminal em 1 hora"). O MVP não gera tentativas simuladas. |
| 6 | LLM | Pydantic AI (ver tabela acima). O provedor "simulado" fica só nos testes. |
| 7 | Banco | SQLAlchemy do Watson com SQLite na demo. PostgreSQL segue possível pela `DATABASE_URL`; sem obrigação de testar no Db2. |
| 8 | Processo | Este plano é a fonte única; decisão nova entra por PR revisado por mais uma pessoa. Código novo, inclusive no `watson/`, sai do Bob. |

**Recomendações, ainda não decididas pelo grupo:**

- **Backend e modelo:** Lucas no backend e no agente; Pedro R. no score local, nos sinais por regra e nos casos de demonstração. A alocação restante segue a matriz de quatro pessoas do direcional.
- **Hospedagem:** Railway, com um serviço e volume persistente para o SQLite e as chaves do LLM como variáveis de ambiente. Responsável a definir. Hospedar atende R12 e permite gravar o vídeo sobre uma execução real.

**Frontend já definido:** Leonardo adapta e integra o React + Carbon existente do Watson (`watson/frontend`, PR #7), com apoio do responsável de backend no contrato e de produto/pesquisa na experiência. Os cards C10, C13, C18 e C27 passam a ativos: adaptação, integração, correções de usabilidade e reteste. D12 continua sob consolidação de Pessoa 4; a autoria técnica do frontend não atribui automaticamente a Leonardo outro papel na matriz de quatro pessoas. O trabalho é planejado, não concluído; a disponibilidade do código do #7 e a implementação dos endpoints precisam ser conferidas.

<!--page-->

## 5. Contratos, identidade e estados

### Solicitação de confirmação

```json
{
  "challenge_id": "CH-007",
  "case_id": "T-007",
  "analysis_id": "A-007-v1",
  "version": 1,
  "status": "AGUARDANDO_ASSOCIADO",
  "allowed_responses": ["AUTHORIZE", "DENY", "UNSURE"],
  "expires_at": "2026-10-23T15:02:00Z",
  "policy_version": "confirmacao-v2",
  "simulation": true
}
```

Valores ilustrativos. O tempo de validade é um parâmetro experimental; não representa prática ou exigência oficial do Sicredi.

### Resposta e persistência

`POST /confirmations/{challenge_id}/response` recebe resposta, versão esperada e chave de idempotência. O servidor deriva o usuário da sessão e verifica propriedade da compra, status pendente, validade e política. Não aceitar um `customer_id` enviado pelo cliente como prova de identidade.

Guardar compra, análise, solicitação, resposta, estado final e eventos. Registrar estado e evento na mesma transação. A requisição duplicada retorna a decisão existente; uma segunda resposta conflitante retorna conflito e não sobrescreve silenciosamente o resultado.

### Estados principais

`RECEBIDA → EM_AVALIACAO → LIBERADA_SIMULACAO` ou `AGUARDANDO_ASSOCIADO` ou `REVISAO_PENDENTE`.

De `AGUARDANDO_ASSOCIADO`: `LIBERADA_SIMULACAO`, `RECUSADA_SIMULACAO`, `REVISAO_PENDENTE` ou `CONFIRMACAO_EXPIRADA`.

O backend verifica a expiração em cada leitura/resposta; um processo de atualização pode materializar estados expirados. O relógio do browser é apenas apresentação. Reiniciar a aplicação não apaga respostas. SQLite exige volume durável; em hospedagem efêmera, usar armazenamento persistente disponível.

**Demonstração:** sessão de um associado fictício, identificada como tal, e separação de dois usuários para testar acesso cruzado. Isso não comprova autenticação bancária produtiva.

<!--page-->

## 6. Requisitos de implementação

| ID | Requisito | Aceite |
|---|---|---|
| R01 | Avaliação automática de compra | Política produz um tratamento versionado sem decisão prévia do analista. |
| R02 | Confirmação vinculada à compra | ID, valor, data e contexto correto aparecem antes da resposta. |
| R03 | Três respostas explícitas | Autorizar, recusar e dúvida têm resultados distintos e persistidos. |
| R04 | Expiração | Resposta fora do prazo não libera a transação. |
| R05 | Autorização por usuário | Usuário B não lê nem responde à solicitação de A. |
| R06 | Idempotência e concorrência | Duas requisições não produzem duas ações ou resultados conflitantes. |
| R07 | Explicação fiel | Números e sinais correspondem aos dados consultados. |
| R08 | Dúvida contextual | Agente consulta o caso, informa limite e permite revisão. |
| R09 | Erro seguro | Falha não gera score inventado, autorização ou troca silenciosa por regras. |
| R10 | Histórico | Recarregar ou reiniciar preserva resposta e resultado. |
| R11 | Transparência | Dados fictícios e ações simuladas aparecem no produto e na demo. |
| R12 | Acesso reproduzível | Outra pessoa autorizada consegue concluir o fluxo de teste. |

### Requisitos de experiência e operação

Uma tela legível no celular; botões com rótulos claros; uso por teclado; status não depende só de cor; estado de carregamento e erro visíveis. Após responder, apresentar confirmação com compra e status, sem ambiguidade.

Segredos ficam em connections ou no servidor. Não registrar credenciais ou dados desnecessários. Os logs incluem IDs, versões, status, etapa de erro e latência. A decisão sobre o tratamento inicial usa código determinístico e política; instruções em prompt não substituem controle de autorização.

**P0:** R01–R07 e R09–R12. A conversa contextual R08 é essencial para demonstrar o papel agêntico, mas sua falha não pode impedir um caminho explícito e seguro de resposta e revisão. Não entregar apenas um formulário fixo e chamá-lo de agente.

<!--page-->

## 7. Modelo e agente: o que manter e corrigir

### Mantemos

O trabalho de EDA e o Random Forest como candidato inicial; o deploy validado no watsonx.ai, como evidência; ferramenta de avaliação; dados sintéticos; sessões do Bob; explicação ligada a evidências. A mudança é no usuário, no fluxo e em quem responde à compra.

### Corrigimos antes de apresentar resultados

- Fechar o manifesto de features: o código conferido anteriormente lista 28; documentos mencionam outro total.
- Alinhar a definição de madrugada, representação de nulos e tipos de categorias entre treino e inferência.
- Confirmar a ordem das classes antes de extrair a probabilidade da classe fraude.
- Auditar disponibilidade temporal das features e sinais históricos.
- Não escolher o limiar no teste final. O teste já consultado para seleção de limiar é exploratório, não um holdout intocado.
- Comparar com e sem as quatro features de velocidade; métricas perfeitas em dados sintéticos não comprovam eficácia real.

Os CSVs conferidos no plano anterior tinham 234 linhas/117 positivos no treino e 32.000 linhas/29 positivos no teste. Os números devem acompanhar a versão executada. Não tratar score como probabilidade calibrada sem avaliação apropriada.

### Comportamento esperado do agente

Explicar por que o sistema pediu confirmação com base nos sinais retornados. Se não houver explicação local do modelo implementada, distinguir score de sinais por regras. Não afirmar que uma regra explica causalmente a predição.

Não pressionar o associado a autorizar. Não pedir senha, PIN ou dados completos de cartão. Não inventar nomes alternativos de estabelecimentos, políticas da instituição ou resultados de bloqueio. Dados e documentos consultados não podem mudar suas instruções.

**Plano alternativo:** se a avaliação pelo modelo falhar, decidir explicitamente usar índice por regras, com `score_source=regras`, política própria e identificação na demonstração. O aplicativo preserva o fluxo de confirmação; a declaração técnica muda. Não esconder essa substituição.

<!--page-->

## 8. Backlog revisado e ordem de execução

**Primeiro:** grupo confirma este fluxo e nomeia responsáveis para dados/modelo, agente/integração, backend, front e validação. A divisão nominal anterior não implica atribuição automática das novas tarefas.

**Divisão das entregas em quatro pessoas:** Pessoa 1 lidera negócios/produto (D01, D04, D05, D07, D08); Pessoa 2 lidera pesquisa/usuário (D02, D03, D06); Pessoa 3 lidera estrutura/arquitetura (D09, D10); Pessoa 4 lidera protótipo, registro do fluxo e validação (D11, D12, D13). A [matriz no direcional](direcional_entregas.md#organização-em-quatro-pessoas-responsáveis-sequência-e-revisão) define apoio, revisor e passagem de trabalho por entrega. Os nomes e a alocação da implementação são definidos pela equipe; liderar um artefato não significa implementar sozinho todos os componentes associados.

### 8.1. Entregas de negócio, design e estruturação

As entregas recomendadas pelas aulas passam a integrar explicitamente o planejamento. O [direcional completo](direcional_entregas.md) contém instruções para produzir e revisar cada uma. IDs D01–D11 correspondem às entregas nomeadas nos slides; D12–D13 organizam atividades de prototipação e validação. Criar o direcional não significa que pesquisa, protótipo ou testes foram executados.

| Bloco | Entregas a produzir | Critério de passagem | Responsabilidade sugerida |
|---|---|---|---|
| Descoberta | D01 Mapeamento de Oportunidades; D02 Mapa de Empatia; D03 Cenário Atual | Fricção, contexto, fontes e hipóteses identificados; pergunta de projeto definida | Produto/negócios + pesquisa/design |
| Escolha e experiência | D04 Agrupamento/Priorização; D05 Conceito; D06 Persona e Cenários | Alternativas comparadas e escolha justificada; persona funcional; atual/futuro comparáveis | Produto + pesquisa/design, com revisão técnica |
| Valor | D07 Ideia e Descrição; D08 Proposta de Valor e Justificativa de IA | Dor, adoção/custeio, valor, necessidade do agente e “por que agora” explícitos | Produto/negócios, com revisão do grupo |
| Estrutura técnica | D09 Estrutura da Solução; D10 Arquitetura Técnica | Necessidades ligadas a requisitos/testes; papéis, ferramentas, política e limites documentados | Produto + backend/agente + dados/modelo |
| Experiência testável | D12 Protótipo da Experiência | Estados, três respostas e ajuda separada testáveis | Pessoa 4 consolida; Leonardo adapta o frontend Watson; produto/pesquisa revisam |
| Fluxo e melhoria | D11 Fluxo Principal do MVP; D13 Validação | Execução reproduzível, observações, correções e reteste na versão identificada | Autores técnicos + integração/testes + pesquisa/validação |

Revisar D01–D03 antes de fechar a experiência; revisar D04–D08 antes de consolidar a proposta de valor; usar D09–D10 para orientar contratos e implementação. D12 permite testar cedo; D11 comprova o caminho integrado; D13 realimenta as decisões. Contratos e exemplos sintéticos podem avançar em paralelo à pesquisa. As entregas semanais são recomendadas, conforme o guia; o checkpoint e o envio final permanecem obrigatórios.

### 8.2. Implementação e integração das entregas

| Etapa | Entrega concreta | Dono sugerido por função | Critério de passagem |
|---|---|---|---|
| 1 | Descoberta, escolha, valor e jornada do associado; política inicial (D01–D09) | Produto + pesquisa/design + grupo | Fontes/hipóteses, alternativas, persona, atual/futuro e valor registrados; liberação, confirmação, dúvida, recusa e expiração definidos. |
| 2 | Contratos da API JSON e fixtures neutras | Backend + dados | Compra, análise, confirmação e chat com IDs, versões e exemplos de resposta; rótulos fora do agente; o front consegue trabalhar só com o contrato. |
| 3 | Modelo local no backend | Modelo + backend | Mesmos scores do notebook para os casos fixos; falha tratada. A prova no watsonx.ai já foi feita em 27/10. |
| 4 | Motor de decisão e persistência | Backend | Política testada; estados e eventos duráveis. |
| 5 | Resposta humana por endpoint | Backend | Propriedade, expiração, repetição e concorrência testadas. |
| 6 | Adaptar e integrar a tela do associado do Watson (D06, D12; C10/C13) | Leonardo no React + Carbon; Pessoa 4 consolida D12; backend apoia API | Três respostas e ajuda separada; sessão, compra, estados e erros lidos da API; console limitado às exceções. |
| 7 | Conversa contextual real | Agente + front | Dúvida usa contexto correto e não altera autorização. |
| 8 | Exceções e status | Backend + agente | Caso sem resposta ou informação chega à revisão com protocolo. |
| 9 | Bateria ponta a ponta e registro do fluxo (D10–D11) | Todos, revisão cruzada | Cenários da seção 9 passam, falhas críticas corrigidas; versão, arquitetura e evidências coerentes. |
| 10 | Teste de compreensão e relatório de melhorias (D13) | Pesquisa/validação + produto/design | Achados, limites, ajustes e retestes registrados; proposta de valor atualizada com resultados. |
| 11 | Documentação, Bob e vídeo | Todos; uma pessoa consolida | Mesma versão, evidências e links revisados. |

### O que sai do backlog anterior

Mesa completa do analista, confirmação obrigatória pelo analista em todo caso, chat do analista como experiência principal e dashboard como prioridade. Não precisamos migrar essas funções para a interface do associado.

### O que entra

Tela de confirmação, vínculo entre usuário e compra, controle de expiração, respostas autorizar/recusar/dúvida, status ao associado e revisão de exceções.

Reestimar o esforço depois das etapas 2 e 3. A estimativa de 69–114 horas do plano anterior não deve ser transportada automaticamente para este novo escopo. Primeiro fechar o caminho de resposta e o agente; cortar elementos decorativos e integrações extras se ameaçarem a conclusão.

<!--page-->

## 9. Testes e medida de melhoria

| Cenário | Resultado esperado |
|---|---|
| Compra elegível à liberação automática | Estado liberado na simulação, com análise e política identificadas. |
| Compra sinalizada; associado autoriza | Uma confirmação e uma liberação simulada registradas. |
| Associado não reconhece | Recusa simulada e encaminhamento de proteção; sem liberação. |
| Associado está em dúvida | Revisão pendente, com status e próximo passo compreensíveis. |
| Associado pede atendimento sem responder à compra | Revisão aberta, sem resposta registrada; confirmação permanece pendente se válida e expira no prazo original. |
| Associado não responde | Expiração sem aprovação presumida. |
| Resposta duplicada ou concorrente | Um resultado consistente; conflito não sobrescreve autorização. |
| Outro usuário tenta responder | Acesso negado. |
| Modelo ou ferramenta falha | Nenhuma conclusão inventada; revisão ou erro explícito. |
| Contexto de estabelecimento ausente | Agente informa limite; não adivinha o estabelecimento. |
| Agente recebe pedido para autorizar sozinho | Não consegue executar resposta em nome do associado. |
| Atualização de página / reinício | Estado preservado. |
| Troca de compra | Dados, conversa e confirmação isolados. |

### Como demonstrar melhoria da experiência

Comparar uma confirmação com dados básicos e texto fixo com o mesmo fluxo apoiado pelo agente. Usar casos equivalentes, alternar a ordem e registrar compreensão, conclusão, erros e tempo. Um piloto de 3 a 5 pessoas pode revelar problemas; identificar se são colegas ou pessoas do domínio e não generalizar para todos os associados.

Perguntas de avaliação: “Qual compra está sendo verificada?”, “O que acontece se você não reconhecer?”, “O que o sistema sabe e o que não sabe?”, “Seu cartão inteiro foi bloqueado ou apenas houve encaminhamento?”.

**Melhoria observável:** menos dúvida sobre o alerta e o próximo passo, sem aumento de autorizações equivocadas no exercício. Registrar resultados, não prometer essa melhoria antes do teste. Separar desempenho do classificador, funcionamento do sistema e compreensão do usuário.

<!--page-->

## 10. Avaliação, demonstração e fontes

### Como sustentar uma entrega forte

| Rubrica do guia | Evidência desta versão |
|---|---|
| Completude e Viabilidade | Compra avaliada, confirmação respondida e resultado persistido; acesso e reprodução. |
| Criatividade e Inovação | Agente resolve dúvidas contextuais e coordena revisão, além de pedir sim/não. |
| Design e Usabilidade | Tela compreensível, estados claros e teste de entendimento com pessoas. |
| Eficácia e Eficiência | Avaliação honesta do modelo, bateria funcional e resultados do piloto. |

Esses quatro critérios valem até 5 pontos cada [G, pp.13–14]. O recorte pode sustentar nota alta, mas não garante 20/20.

### Vídeo de 3 minutos

**0:00–0:25:** problema do associado e produto. **0:25–1:10:** compra sinalizada e autorização explícita, com resultado registrado. **1:10–1:50:** segunda compra, dúvida contextual e recusa/revisão. **1:50–2:20:** demonstrar limite: sem resposta não há autorização; agente não autoriza sozinho. **2:20–3:00:** arquitetura, Bob, evidência e limitações.

As ações são simuladas. O vídeo mostra uma execução real do protótipo, sem simular integração concluída por meio de telas desconectadas.

### Entrega obrigatória permanece

Checkpoint, conforme plataforma; vídeo de 3 minutos; declaração do problema e solução com link funcional; declaração de tecnologia; evidências das sessões do Bob no repositório. As atividades das sessões são recomendadas e devem ser adaptadas à nova persona [G, p.13 e pp.30–31].

### Fontes e relação com a versão anterior

- **G:** [Guia IBM](../contexto/2H26%20GuideBob_IBM%20SkillsBuild_AI%20Experiential%20Learning%20Lab%20BR.pdf), pp.5, 13–14 e 30–31.
- **C:** [Desafio Sicredi](../contexto/2026%20AI%20Experiential%20Learning%20Lab%20with%20Bob%20-%20Industry%20Challenges_Portuguese.pdf), p.6.
- **Base técnica local:** [Preparação dos dados](02_base_balanceada.md), [Modelo](03_modelo.md) e notebooks 02/03. As regras e requisitos desta proposta revisam a direção anterior centrada no analista.
- **Referências técnicas:** [Pydantic AI](https://ai.pydantic.dev/), [FastAPI](https://fastapi.tiangolo.com/), [limiares de classificação](https://scikit-learn.org/stable/modules/classification_threshold.html) e [calibração](https://scikit-learn.org/stable/modules/calibration.html).
- **Integração IBM testada:** [spec do teste Orchestrate → watsonx.ai](specs/teste_integracao_orchestrate_wml.md), com o resultado de 27/10. O Orchestrate saiu do escopo antes do teste completo.

**Resultado desta revisão:** produto, jornada, regras, interface, contratos, testes e backlog foram atualizados no planejamento. Código de aplicação e serviços IBM ainda não foram implementados ou modificados nesta revisão.
