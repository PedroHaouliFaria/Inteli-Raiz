# Pacote final IBM — conteúdo e pendências

**Versão:** 0.2 · **Data:** 08/11/2026 · **Estado:** peças prontas para revisão do time; não submetido.\
**Fontes:** guia IBM p.13 e pp.30–31, conforme [mapa de fontes](exigencias-da-ibm.md). Conferir campos/regras vigentes na plataforma antes do envio; não há acesso a ela nesta revisão.

| Peça | Onde está | Situação |
|---|---|---|
| Aplicação publicada (link funcional) | <https://raiz-jq28.onrender.com> | No ar desde 08/11; abre sem login de terceiros |
| Vídeo de demonstração | [demonstracao/](../../../demonstracao/README.md), com arquivo e link do Google Drive | Gravado; o link do Drive abre sem login |
| Declaração de problema e solução | Seção 1 abaixo | Versão para revisão, com 478 palavras (limite: 500) |
| Declaração tecnológica | Seção 2 abaixo | Versão para revisão |
| Relatórios do IBM Bob | [bob_sessions/](../../../bob_sessions/) | Cinco integrantes com relatórios |

## 1. Declaração de problema e solução

**Raiz: confirmação assistida de compras para associados do Sicredi**

**O problema.** Quando o antifraude sinaliza uma compra no cartão, o associado precisa decidir rápido se a reconhece, quase sempre com pouco contexto. O nome do estabelecimento é difícil de reconhecer, não fica claro por que a compra chamou atenção, e há insegurança sobre o efeito de cada botão: recusar a compra bloqueia o cartão? Quem continua em dúvida procura outro canal e repete toda a história. Nossa pergunta: como ajudar o associado a decidir sobre uma compra sinalizada, entendendo o que autoriza e qual é o próximo passo?

**A solução.** O Raiz é uma plataforma web de confirmação assistida de compras. Um modelo de risco (Random Forest treinado com a base sintética do desafio) pontua cada compra: as de baixo risco são liberadas automaticamente, e as suspeitas pedem confirmação do associado ou ficam bloqueadas preventivamente até a resposta.

O associado vê a compra (valor, data, canal, final do cartão) e os motivos do alerta em linguagem simples, e responde por três controles explícitos: "Reconheço e autorizo", "Não reconheço" ou "Estou em dúvida". Um copiloto de IA tira dúvidas consultando só os dados daquele associado, mas nunca decide por ele: apenas os botões registram a resposta. A analista de prevenção a fraudes recebe somente as exceções, já com o score do modelo e a resposta do associado, e registra a decisão com justificativa. O novo status aparece na hora para o associado.

**Por que é diferente.** Alertas antifraude costumam ser um "sim ou não" sem contexto ou uma ligação para a central. O Raiz junta três peças num só fluxo: o modelo prioriza, a IA explica e uma pessoa decide as exceções. A IA tem limites de projeto: não autoriza compras, não vê o score interno e só tem ferramentas de consulta e de pedido de revisão. "Estou em dúvida" é uma resposta válida, que leva o caso a um especialista sem que o associado repita o contexto. Assim, o atendimento humano fica reservado a quem realmente precisa dele.

É um protótipo funcional com dados sintéticos e ações financeiras simuladas. Ainda não medimos o impacto com associados reais; esse é o próximo passo.

**Repositório:** <https://github.com/PedroHaouliFaria/Inteli-Raiz>
- `watson/`: aplicação (frontend React com Carbon, backend FastAPI, infraestrutura Docker)
- `notebooks/` e `outputs/`: análise dos dados e modelo de risco
- `docs/`: documentação completa (problema, decisões, custos e arquitetura)
- `bob_sessions/`: relatórios das sessões no IBM Bob

**Como acessar.** Site: <https://raiz-jq28.onrender.com> (o primeiro acesso pode levar até um minuto)
- Associado: `ana@raiz.demo` / `Ana@123`
- Analista: `carla@raiz.demo` / `Carla@123`

Percurso sugerido: entre como Ana, abra uma compra "Aguardando sua resposta", converse com o copiloto (ícone no topo) e escolha "Estou em dúvida". Depois entre como Carla, abra o caso em "Pendentes" e registre a decisão. De volta à Ana, o status estará atualizado. O link "Restaurar dados da demonstração" reinicia os dados.

## 2. Declaração tecnológica

**IBM Bob.** Os cinco integrantes usaram o Bob como agente de desenvolvimento ao longo de todo o projeto, principalmente no Bob IDE em modo Agent. No backend, também usamos o Bob Shell 2.0.9. Cada sessão tem um relatório em `bob_sessions/<integrante>/`, com o ID da tarefa no Bob, o custo, o número de chamadas de ferramenta, o que foi feito e o que a revisão humana conferiu ou corrigiu. São 18 relatórios de sessão e 2 planos de execução preparados para o Bob.

Para manter o Bob alinhado ao projeto, criamos regras em `.bob/rules/`. O arquivo `backend.md` define o contrato da API como fonte da verdade e manda o Bob parar e perguntar quando a especificação for ambígua. O arquivo `docs.md` limita as tarefas de documentação à pasta `docs/`.

Onde o Bob atuou:
- **Modelo de risco:** construção do notebook 03, com o pipeline e o Random Forest, do gráfico de distribuição de scores e de uma análise comparando o modelo com e sem as features de velocidade.
- **Backend (FastAPI):** expiração da confirmação; resposta do associado com idempotência e controle de concorrência; registro do score; fila de revisão da analista; agente de chat com Pydantic AI; modo de demonstração com reset. Também correções de segurança: o score fica fora do contexto do agente, o modelo é carregado uma única vez e o chat não trava o banco enquanto o LLM responde.
- **Frontend (React e Carbon):** integração das telas de associado e analista com a API; justificativa obrigatória e histórico de revisões; proteção de rotas por perfil; triagem automática de risco e contestações; reorganização do fluxo da analista; correções de usabilidade.
- **Documentação:** plano de implementação, estrutura e arquitetura da solução, protocolo de validação, guia da demonstração, Canvas de Proposta de Valor e consolidação dos artefatos D01–D13.

Todo trabalho do Bob passou por branch, revisão humana e pull request. Os relatórios registram também os limites, por exemplo uma tarefa que parou no teto de custo e foi concluída numa segunda rodada, e um teste intermitente que a revisão identificou e o Bob corrigiu.

**IBM watsonx.ai.** O modelo de risco foi publicado no watsonx.ai Runtime. O Random Forest, retreinado em Python 3.12 com scikit-learn 1.6.1, foi enviado pelo script `scripts/deploy_watsonx.py` como deploy online no space "Inteli Raiz Space" (Dallas). O script também resolve dois problemas que encontramos: o timeout de upload da biblioteca `ibm-watsonx-ai` e a exigência de task credential.

No teste de 27/10, chamando o endpoint `/predictions`, o caso de fraude recebeu score 0,9917 e o caso legítimo 0,0089. Os resultados foram idênticos aos do modelo local, com latência entre 1,1 e 2,9 segundos. O backend aceita os dois modos pela variável `RISK_MODEL_PROVIDER`: `watsonx` chama o deployment, e `local` lê o mesmo arquivo do modelo. A demonstração publicada usa o modo local, para não depender da disponibilidade do serviço durante a avaliação. O copiloto de chat usa Pydantic AI com o modelo `gpt-oss-120b` via Groq.

**IBM watsonx Orchestrate.** Construímos um agente com o ADK do Orchestrate (`agente/agents/agente_teste.yaml`), com uma ferramenta Python (`agente/tools/pontuar_transacao.py`) que chama o deployment do watsonx.ai para pontuar transações. Não conseguimos validar o agente dentro do Orchestrate: o trial expirou e a opção "Extend Trial" retornou erro. Levamos o caso ao orientador e decidimos tirar o Orchestrate da dependência de execução. O código do agente continua no repositório.

Fontes: [relatórios do Bob](../../../bob_sessions/), [regras do Bob](../../../.bob/rules/), [teste do watsonx.ai](../sistema/specs/teste-historico-watsonx.md), [script de publicação](../../../scripts/deploy_watsonx.py) e [agente do Orchestrate](../../../agente/).

## 3. Roteiro de vídeo — 3 minutos

O vídeo foi gravado e está em [demonstracao/](../../../demonstracao/README.md). O roteiro abaixo é o planejamento original.

| Tempo | Conteúdo | Evidência a exibir |
|---|---|---|
| 0:00–0:25 | Problema, associado e hipótese de valor | Fricção de D01, com limite da pesquisa |
| 0:25–0:45 | Solução, simulação e limites | Login fictício e compra identificada |
| 0:45–1:40 | Percurso integrado e resposta explícita | UI, resultado, protocolo e recarga |
| 1:40–2:15 | Dúvida contextual e limite do agente | Ferramentas e resposta real sem inventar estabelecimento |
| 2:15–2:40 | Exceção/falha e persistência | Revisão/expiração, sem autorização presumida |
| 2:40–3:00 | Tecnologia, validação disponível e próximos limites | Log/teste e resultado de piloto somente se executado |

## 4. Checklist de submissão

- [x] Vídeo de três minutos gravado e acessível sem login.
- [ ] Vídeo conferido por outra pessoa contra a versão publicada.
- [x] Link funcional publicado e aberto sem login em 08/11.
- [ ] Declaração problema/solução revisada pelo time.
- [ ] Declaração tecnológica revisada pelo time.
- [x] Sessões reais do IBM Bob dos cinco integrantes em `bob_sessions/`.
- [ ] Revisão cruzada e limites de pesquisa/teste declarados.
- [ ] Regras/campos de checkpoint e envio conferidos pelo líder cadastrado na plataforma.
- [ ] Comprovante de submissão preservado após o envio.

Este documento consolida conteúdo disponível, sem inventar requisitos de plataforma, participantes, resultado financeiro ou evidências do Bob.
