# D12 — Protótipo da experiência e decisões de interface

**ID:** D12 · **Versão:** 0.3 · **Data:** 04/11/2026\
**Responsável:** Integração e validação; Leonardo na implementação frontend · **Revisor previsto:** Pesquisa\
**Estado:** revisão documental atualizada; aplicação integrada no código; teste de compreensão/acessibilidade pendente.\
**Base:** develop `f741a35`; [D06](D06_persona_e_cenarios.md), [D09](D09_estrutura_solucao.md) e componentes em `watson/frontend/src/features/`.\
**Decisão sustentada:** compra identificada, três respostas e atendimento separado, com resultado sobre a compra.

## 1. Acesso e percurso

Executar [D11](D11_fluxo_mvp.md) e abrir localhost:5173. O fluxo atual começa em SessionGate e escolhe AssociateApp ou AnalystApp pelo papel fictício. A interface antiga MemberPhone/reducer permanece no repositório como legado visual; suas observações de 28/10 não descrevem o fluxo integrado atual.

Percurso: sessão fictícia → lista → detalhe da compra → resposta explícita → resultado. Chat e pedido de atendimento ficam disponíveis como ajuda; revisão não substitui a resposta nem prorroga prazo. Os desenhos anteriores em [docs/design](../docs/design/README.md) são referências visuais, não prova de integração.

## 2. Telas e estados inspecionados no código

| Tela/estado | Implementação | Decisão e ligação com hipótese | O que ainda testar |
|---|---|---|---|
| Sessão/lista | SessionGate, AssociateApp, PurchaseList | Sessões Ana/Bruno/Carla identificadas como fictícias; isolamento R05 | Troca de sessão no navegador |
| Compra e alerta | PurchaseDetail; cartões de compra/alerta | HIP-03/05: contexto antes da pergunta; sinais descritivos, sem score numérico para o associado | Clareza do motivo e identificação da compra |
| Três respostas | Buttons em PurchaseDetail usam allowed_responses da API | HIP-01/05: AUTHORIZE, DENY e UNSURE explícitos, sem etapa de biometria nesse caminho | Entendimento das consequências antes da escolha |
| Envio/erro | Estados de envio, ApiError e chave idempotente no client | R06/R09: feedback e retry consistente | Rede lenta, retry, teclado/foco |
| Chat | PurchaseChat e POST /api/purchases/{case_id}/chat | HIP-03: contexto ou limite; não inventar nome fantasia | Resposta com LLM real e interpretação do limite |
| Pedido de atendimento | HumanReviewRequest e endpoint review | HIP-02: protocolo, confirmação continua válida até o prazo | Compreensão da diferença entre pedir ajuda e UNSURE |
| Resultado | ResultCard/ReviewCard com objetos retornados pelo backend | HIP-09: estado e próximo passo; DENY não significa cartão bloqueado | Recarga, tela pequena e leitura sem explicação |
| Prazo/expiração | ExpiryCountdown, polling e resposta do servidor | R04: contagem visual é apoio; servidor decide validade | Relógio divergente, expiração durante interação |

## 3. Textos e consequências a preservar

- Pergunta: reconhecer **e autorizar esta compra**; não prometer bloquear/desbloquear todo o cartão.

- AUTHORIZE: compra liberada na simulação; nenhuma transação real feita.

- DENY: compra recusada na simulação; revisão de proteção aberta; status da compra continua RECUSADA_SIMULACAO.

- UNSURE: compra em REVISAO_PENDENTE e revisão de dúvida; não é apenas uma pergunta ao chat.

- “Prefiro falar com uma pessoa”: pedido separado, protocolo e confirmação ainda respondível enquanto válida; não estende prazo.

- Expiração: nenhuma autorização presumida; orientar o próximo passo disponível.

- Sem contexto: explicitar a lacuna; sinais são características da compra, não causas comprovadas do score.

A regra do produto e o caminho de revisão estão definidos. O prompt do agente ainda afirma que a tela tem apenas botões e chat, embora HumanReviewRequest exista; registrar esse desalinhamento na pendência TEC-01 antes de encerrar a experiência. Esta revisão documental não alterou o prompt da aplicação.

## 4. Decisões ligadas à pesquisa

| Hipótese | Decisão candidata | Tarefa para testar |
|---|---|---|
| HIP-01 confundir recusa e bloqueio | Texto de resultado sobre a compra e revisão | Não reconhece + pergunta C5 de D13 |
| HIP-02 ajuda encerra resposta | Protocolo e prazo visíveis; separar ação de UNSURE | Pedir ajuda e depois responder |
| HIP-03 nome ambíguo | Categoria/contexto disponível e limite explícito | Comparação A/B com mesmos dados |
| HIP-05 efeito da resposta | Rótulos de ação claros e resultado persistido | Explicar as três consequências sem instrução |
| HIP-09 desfecho incerto | Resultado e próximo passo vindos da API | Recarregar e explicar o estado |

## 5. Aceite e acessibilidade

Código inspecionado não prova que uma pessoa compreendeu o percurso. Pesquisa deve executar as tarefas de [D13](D13_validacao_melhorias.md) e registrar versão, tela observada, interpretação e ajuste. Conferir celular, zoom, navegação por teclado, ordem/foco após erro, nomes acessíveis e status sem depender só da cor. Não há relatório de inspeção visual ou teste com leitor de tela produzido nesta revisão.

Comparar pelo menos duas alternativas de texto/interação se o piloto indicar problema, escolher com justificativa e retestar o cenário afetado. A matriz de aceite central preserva esses itens abertos.
