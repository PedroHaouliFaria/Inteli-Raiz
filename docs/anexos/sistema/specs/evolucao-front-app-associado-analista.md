# Evolução do front e da aplicação: associado e analista

| Campo | Valor |
|---|---|
| Data | 05/11/2026 |
| Estado | proposta para implementação |
| Origem | feedback de interface fornecido pela equipe em 05/11/2026 e revisão do código atual |
| Escopo | front-end, APIs de apoio, persistência e testes dos perfis associado e analista |

## 1. Objetivo

Transformar o feedback recebido em um roteiro implementável, priorizando primeiro os erros que interrompem o fluxo principal e depois as novas capacidades de acompanhamento e gestão.

Esta especificação ainda não altera o contrato oficial da API. Os endpoints e campos novos descritos aqui são propostas e devem ser incorporados ao [contrato da API](contrato-da-api.md) junto com a implementação aprovada.

## 2. Resumo do que precisa mudar

### Associado

1. Manter a compra selecionada quando o chat ou a lista forem atualizados.
2. Mostrar uma linha do tempo com as etapas reais do processo.
3. Melhorar a apresentação das mensagens do assistente.
4. Criar uma tela separada de visão geral do associado.

### Analista

1. Separar revisões pendentes das já encerradas.
2. Permitir abrir uma revisão e consultar seus detalhes antes da decisão.
3. Exigir uma justificativa ao autorizar ou recusar uma compra.
4. Criar uma tela de perfil.
5. Criar uma tela separada de indicadores operacionais.

### Base comum

1. Introduzir navegação interna por perfil e URLs que possam ser abertas diretamente.
2. Cobrir os fluxos críticos com testes de front-end, backend e ponta a ponta.
3. Manter os dados internos do modelo e de outros clientes fora da experiência do associado.

## 3. Diagnóstico do estado atual

| Item | Estado atual | Lacuna |
|---|---|---|
| Seleção da compra | `AssociateApp` recarrega as compras e pode selecionar a primeira novamente | o contexto muda durante uma conversa |
| Linha do tempo | eventos existem no banco, mas não são entregues ao associado | não há visualização das etapas reais |
| Mensagens | o conteúdo do assistente é renderizado em um único parágrafo | quebras, listas e blocos perdem legibilidade |
| Visão geral do associado | inexistente | faltam resumo e ações pendentes |
| Fila do analista | a API lista apenas revisões abertas | revisões encerradas não podem ser consultadas |
| Detalhe da revisão | dados e ações ficam no cartão da fila | não existe consulta detalhada antes da decisão |
| Justificativa | a decisão recebe somente autorizar ou recusar | motivo e responsável não ficam estruturados na revisão |
| Perfil | autenticação usa usuários configurados no ambiente | não há cadastro persistente para edição de perfil ou senha |
| Indicadores do analista | inexistente | não há endpoint de agregação nem tela própria |
| Navegação | cada papel abre uma aplicação única, sem rotas internas | não há menu, URL profunda ou retorno previsível do navegador |

### 3.1 Causa da troca indevida de compra

`loadPurchases`, em `AssociateApp.jsx`, foi criada sem dependências e conserva o valor inicial de `selectedId`. Ao ser chamada novamente depois de uma atualização do chat, ela ainda interpreta que não existe seleção e escolhe a primeira compra da lista.

A correção deve atualizar a seleção de forma funcional:

- preservar o identificador atual enquanto ele ainda existir na lista;
- selecionar a primeira compra somente no primeiro carregamento ou quando a compra atual deixar de existir;
- não alterar a seleção em atualizações do chat, abertura de revisão, polling ou decisão;
- preferir que o identificador da compra também faça parte da URL.

## 4. Arquitetura de navegação proposta

### 4.1 Rotas do associado

| Rota | Finalidade |
|---|---|
| `/associate/purchases` | lista de compras |
| `/associate/purchases/:caseId` | compra e conversa selecionadas |
| `/associate/dashboard` | visão geral do associado |
| `/associate/profile` | perfil e sessão |

### 4.2 Rotas do analista

| Rota | Finalidade |
|---|---|
| `/analyst/reviews/open` | revisões pendentes |
| `/analyst/reviews/history` | revisões encerradas |
| `/analyst/reviews/:reviewId` | detalhe da revisão |
| `/analyst/dashboard` | indicadores operacionais |
| `/analyst/profile` | perfil e sessão |

As rotas devem manter a proteção pelo papel retornado na sessão. Um associado não pode acessar dados ou telas de analista, e o analista não deve conseguir assumir a identidade de um associado pela URL.

## 5. Requisitos funcionais e critérios de aceite

### ASSOC-01 — Preservar o contexto da compra — P0

**Comportamento:** a lista pode ser recarregada sem trocar a compra escolhida.

**Critérios de aceite:**

- ao selecionar a compra B e enviar ou receber uma mensagem, a tela continua na compra B;
- ao abrir uma revisão humana, a tela continua na mesma compra;
- uma compra é escolhida automaticamente apenas quando ainda não há seleção válida;
- recarregar uma URL com `caseId` abre a compra indicada, se ela pertencer ao usuário;
- um `caseId` inexistente ou de outro associado produz estado de não encontrado, sem expor dados.

### ASSOC-02 — Linha do tempo do processo — P1

**Comportamento:** o detalhe da compra apresenta eventos reais em ordem cronológica.

Etapas exibidas quando aplicáveis:

1. compra identificada;
2. em análise;
3. aguardando resposta do associado;
4. em revisão humana;
5. concluída.

**Critérios de aceite:**

- cada etapa usa o evento persistido como fonte e mostra data e hora;
- etapas ignoradas pelo fluxo não aparecem como concluídas;
- o estado atual possui texto, ícone ou outro sinal além de cor;
- nomes internos de evento são convertidos para linguagem compreensível;
- identificador de analista, score, atributos brutos do modelo e payload interno não são retornados ao associado.

### ASSOC-03 — Formatação das mensagens — P1

**Comportamento:** mensagens do assistente preservam parágrafos, quebras de linha e listas.

**Critérios de aceite:**

- texto com múltiplos parágrafos continua separado visualmente;
- listas são legíveis e acessíveis;
- mensagens extensas não ultrapassam o cartão ou a tela;
- HTML recebido como texto não é executado;
- links, se habilitados, recebem tratamento seguro.

O primeiro incremento pode preservar espaços com CSS. Se Markdown limitado for adotado, HTML bruto deve permanecer desabilitado.

### ASSOC-04 — Visão geral do associado — P2

**Comportamento:** tela separada resume a situação das compras do usuário autenticado.

Conteúdo inicial recomendado:

- quantidade de confirmações pendentes;
- quantidade de compras por estado;
- compras recentes e sua situação;
- valor total por estado, com rótulo que não sugira saldo bancário;
- atalho para a próxima ação necessária.

**Critérios de aceite:**

- os números consideram apenas o associado autenticado;
- o período usado é informado na tela;
- cada indicador permite chegar à lista filtrada correspondente;
- existem estados de carregamento, vazio e erro;
- score, probabilidade de fraude e dados de outros usuários não aparecem.

### ANALYST-01 — Pendentes e histórico — P0

**Comportamento:** a área do analista tem abas ou páginas para revisões pendentes e encerradas.

**Critérios de aceite:**

- pendentes mostram apenas revisões abertas;
- histórico permite filtrar por decisão e período;
- a listagem é paginada e preserva filtros na navegação;
- um registro encerrado mostra decisão, justificativa, responsável e data;
- revisões encerradas não oferecem uma nova ação de decisão.

### ANALYST-02 — Detalhe antes da decisão — P0

**Comportamento:** selecionar uma revisão abre uma página de detalhe.

Dados previstos:

- protocolo, motivo e data de abertura;
- valor, data, categoria, canal e final do cartão da compra;
- sinais e explicações destinados ao analista;
- análise do modelo identificada como informação interna;
- resposta de confirmação do associado, quando houver;
- linha do tempo de auditoria sem atributos brutos desnecessários.

**Critérios de aceite:**

- a decisão só é oferecida após o detalhe estar disponível;
- número completo do cartão, senha, atributos brutos do modelo e dados de outro cliente não aparecem;
- uma revisão inexistente produz estado de não encontrado;
- uma revisão encerrada pode ser consultada, mas não alterada.

O histórico completo do chat não entra no primeiro incremento. Sua exposição ao analista depende de decisão explícita de produto e privacidade.

### ANALYST-03 — Justificativa obrigatória — P0

**Comportamento:** autorizar ou recusar abre uma confirmação com campo de justificativa.

**Critérios de aceite:**

- a justificativa é obrigatória e contém entre 10 e 500 caracteres após remoção de espaços externos;
- a interface não envia a decisão enquanto o campo for inválido;
- o backend repete a validação e rejeita payload inválido;
- decisão, justificativa, analista e instante ficam persistidos na revisão e no evento de auditoria;
- falha no envio mantém o texto digitado e permite nova tentativa;
- a linguagem da interface usa “Autorizar compra” e “Recusar compra”, evitando a ambiguidade de “cancelar”.

A justificativa será inicialmente interna. Exibi-la ao associado exige uma decisão de conteúdo e conformidade.

### COMMON-01 — Perfil e sessão — P2

**Comportamento:** cada papel possui uma página de perfil somente leitura no primeiro incremento.

Conteúdo previsto:

- nome de exibição;
- e-mail;
- papel atual;
- aviso de que o ambiente usa usuários de demonstração;
- ação de sair.

**Critérios de aceite:**

- senhas e hashes nunca são retornados;
- os dados vêm da sessão ou de endpoint autenticado;
- alteração de nome ou senha não é simulada sem persistência e gestão de identidade reais.

Edição de perfil, recuperação e troca de senha ficam fora do MVP até a escolha de um provedor de identidade ou criação de uma base de usuários apropriada.

### ANALYST-04 — Indicadores do analista — P2

**Comportamento:** tela separada apresenta indicadores agregados da operação.

Conteúdo inicial recomendado:

- revisões abertas e encerradas;
- autorizações e recusas;
- tempo mediano de resolução;
- volume de revisões ao longo do tempo;
- valor total por decisão;
- distribuição dos motivos de abertura.

**Critérios de aceite:**

- o período padrão é de 30 dias e pode ser alterado;
- todas as métricas têm definição visível;
- gráficos possuem alternativa textual ou tabela;
- período sem dados não é apresentado como erro;
- os totais são consistentes com a listagem filtrada.

## 6. Mudanças propostas no backend e nos dados

Estas interfaces ainda são propostas, não endpoints existentes.

| Área | Proposta | Observação |
|---|---|---|
| Detalhe da revisão | `GET /api/reviews/{review_id}` | validar papel e retornar apenas dados necessários |
| Listagem | `GET /api/reviews?status=&decision=&from=&to=&page=&page_size=` | substituir a limitação atual a revisões abertas |
| Decisão | `POST /api/reviews/{review_id}/decision` com `decision` e `justification` | validação obrigatória também no servidor |
| Linha do tempo | `GET /api/purchases/{case_id}/timeline` | validar propriedade e sanitizar eventos |
| Visão do associado | `GET /api/associate/dashboard?from=&to=` | agregação limitada ao usuário autenticado |
| Visão do analista | `GET /api/analyst/dashboard?from=&to=` | agregação operacional |
| Perfil | `GET /api/profile` ou ampliação da sessão | somente nome, e-mail e papel |

### 6.1 Migração da revisão

A entidade de revisão precisa de campos estruturados e anuláveis para registros ainda abertos:

| Campo proposto | Finalidade |
|---|---|
| `decision` | decisão final |
| `decision_reason` | justificativa do analista |
| `decided_by` | usuário que decidiu |
| `decided_at` | instante da decisão |

A migração deve preservar as revisões existentes. Registros históricos sem informação suficiente continuam com campos nulos; não se deve inventar responsável, justificativa ou horário.

### 6.2 Paginação e limites

- padrão de 20 registros por página;
- máximo de 100 registros por requisição;
- ordenação padrão: pendentes mais antigas primeiro e histórico mais recente primeiro;
- filtros validados e datas com fuso explícito;
- agregações calculadas no backend, não a partir de uma página parcial no front.

## 7. Ordem de implementação

| Ordem | Entrega | Prioridade | Dependências | Tamanho relativo |
|---:|---|---|---|---|
| 1 | ASSOC-01: corrigir seleção e criar teste de regressão | P0 | nenhuma | P |
| 2 | base de rotas, menu por papel e proteção de acesso | P0 | nenhuma | M |
| 3 | migração da revisão e ANALYST-03: justificativa | P0 | banco e contrato | M |
| 4 | ANALYST-02: endpoint e tela de detalhe | P0 | rotas e contrato | M |
| 5 | ANALYST-01: histórico, filtros e paginação | P0 | campos da decisão | M |
| 6 | ASSOC-02: API e componente de linha do tempo | P1 | sanitização de eventos | M |
| 7 | ASSOC-03: formatação segura das mensagens | P1 | nenhuma | P |
| 8 | ASSOC-04: visão geral do associado | P2 | endpoint de agregação | M |
| 9 | ANALYST-04: indicadores do analista | P2 | decisão e datas estruturadas | G |
| 10 | COMMON-01: perfil somente leitura | P2 | sessão expor dados mínimos | P |

Legenda: P = pequeno, M = médio, G = grande. Os tamanhos são relativos e devem ser convertidos em estimativa pela equipe após a definição final dos contratos.

## 8. Estratégia de testes

### Front-end

- manter a compra B selecionada após mensagem, polling e abertura de revisão;
- abrir diretamente as rotas com identificador;
- renderizar mensagens com parágrafos, listas, texto longo e tentativa de injeção;
- validar estados de carregamento, vazio, erro e acesso negado;
- validar campo de justificativa, foco e recuperação após falha;
- testar filtros, paginação e consulta de registro encerrado.

### Backend

- impedir acesso entre papéis e acesso do associado à compra de outro usuário;
- validar tamanho da justificativa e impedir segunda decisão;
- persistir decisão e evento de auditoria na mesma operação;
- testar filtros, ordenação e limites da paginação;
- conferir agregações com conjuntos conhecidos e períodos sem dados;
- garantir que a linha do tempo sanitizada não vaze payload interno.

### Ponta a ponta

1. associado seleciona uma compra, conversa e permanece nela;
2. associado solicita revisão;
3. analista encontra a revisão em pendentes e abre o detalhe;
4. analista recusa ou autoriza com justificativa;
5. revisão aparece no histórico e deixa de aceitar ação;
6. associado vê a situação final na mesma compra e na linha do tempo;
7. totais dos painéis refletem a operação depois da atualização.

## 9. Definição de pronto

Uma entrega deste roteiro só está pronta quando:

- front, backend e migração necessários foram integrados;
- contrato oficial da API foi atualizado;
- critérios de aceite possuem testes proporcionais ao risco;
- estados de carregamento, vazio, erro e acesso negado estão tratados;
- navegação por teclado, foco, rótulos e contraste foram verificados;
- nenhum dado interno ou de outro usuário é exposto;
- documentação de execução e dados de demonstração continuam reproduzíveis.

## 10. Decisões pendentes antes dos painéis e do perfil editável

| Questão | Recomendação inicial |
|---|---|
| Período padrão dos painéis | últimos 30 dias |
| Histórico do chat para analistas | não expor no primeiro incremento |
| Justificativa visível ao associado | manter interna até revisão de conteúdo e conformidade |
| Nome da ação negativa | “Recusar compra” |
| Perfil no MVP | somente leitura |
| Etapas da linha do tempo | derivar apenas de eventos reais |
| Tamanho de página | 20, configurável até 100 |

## 11. Fora de escopo

- ações financeiras reais ou integração com processador de pagamentos;
- cadastro, recuperação e troca de senha de produção;
- exibição do score ou de atributos brutos do modelo ao associado;
- acesso irrestrito do analista ao conteúdo das conversas;
- gráficos decorativos antes da validação dos números;
- reconstrução retroativa de justificativas inexistentes.
