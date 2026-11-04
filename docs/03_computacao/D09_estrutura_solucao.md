# D09 — Estrutura da solução e critérios de sucesso

**ID:** D09 · **Versão:** 0.2 · **Data:** 04/11/2026\
**Responsável:** Arquitetura · **Revisor previsto:** Integração e validação\
**Estado:** revisado documentalmente; revisão cruzada e ensaio pela interface pendentes\
**Base inspecionada:** develop `f741a35`, após integração dos PRs #15, #16 e #17.\
**Fontes:** [plano](../05_gestao/plano_implementacao.md), [D05](../01_negocios/D05_conceito_solucao.md), [D08](../01_negocios/D08_proposta_valor_ia.md), [contrato JSON](specs/contrato_api.md).\
**Decisão sustentada:** confirmação explícita pelo associado, com agente restrito a contexto e revisão.

## 1. Problema e jornada prioritária

Hipótese de trabalho: ao receber uma compra sinalizada, o associado pode ter dificuldade para reconhecer o contexto e compreender as consequências da resposta (HIP-01/03/05). Isso não comprova ausência de um canal atual da instituição. O associado é o usuário principal; o analista trata exceções.

Jornada proposta: sessão fictícia → compra identificada → detalhes e sinais → resposta explícita ou chat/pedido de revisão → resultado persistido. Modelo avalia sinais; política define tratamento; agente consulta e explica; interface humana registra AUTHORIZE/DENY/UNSURE.

## 2. Componentes e estado verificado

| Componente | Papel e localização | Estado e limite |
|---|---|---|
| Modelo RF | `outputs/modelo_rf.joblib`; `app/risk/`; intake calcula análise | Arquivo e carregamento implementados. Validade do modelo exige corte, versão, schema e limitações do relatório; score não é probabilidade calibrada. |
| Política | `app/domain/cases/intake.py` | Política conservadora `confirmacao-v2`: avaliação disponível → confirmação; falha → revisão. Limiar `risk_decision_threshold=0.817` é configuração do modelo, não autorização automática. |
| Backend | `watson/backend/app/`, FastAPI/SQLAlchemy | Rotas, sessões, persistência, estados e revisões implementados; evidência de teste em D11. SQLite é padrão; outros bancos não foram executados nesta revisão. |
| Agente de chat | `app/domain/agent/__init__.py` | Pydantic AI implementado; `pydantic-ai-slim[groq]==2.63.0` é dependência principal. Modelo padrão `groq:openai/gpt-oss-120b`; requer configuração de chave para execução real. |
| Interface | `SessionGate`, `AssociateApp`, `PurchaseDetail`, `PurchaseChat`, `HumanReviewRequest`, `AnalystApp` | Fluxo por papel e cliente HTTP implementados (#14/#18). Código legado de apresentação continua no repositório; não é o fluxo integrado de aceite. |
| IBM Bob / watsonx.ai | Bob no desenvolvimento; teste de deploy documentado na spec | A spec relata teste em 27/10. Não foi reexecutado nesta revisão; não presumir watsonx.ai no runtime do chat atual. |

Os caminhos `app/` acima são relativos a `watson/backend/`. Implementado significa código presente; execução real com credenciais e teste humano têm registros próprios.

## 3. Saber, decidir e fazer

- **Saber:** contexto da compra autorizada pela sessão, sinais, disponibilidade da avaliação, política e estado. A ferramenta de avaliação atual não devolve o valor numérico do score ao agente; a interface do associado também não o recebe.

- **Decidir:** qual ferramenta consultar, quando declarar falta de contexto e quando solicitar revisão.

- **Fazer:** consultar compra/status/avaliação e criar revisão permitida. Nunca registrar AUTHORIZE/DENY/UNSURE pelo texto do chat. Identidade e compra são injetadas pelo backend, não aceitas do LLM.

## 4. Requisitos e coleta

| Req. | Necessidade / verificação | Responsável pela coleta | Registro |
|---|---|---|---|
| R01 | Avaliação e política com origem/versão ou falha explícita | Arquitetura/dados | Testes intake/seed/análise + relatório do modelo |
| R02 | Compra correta exibida antes da resposta | Integração | Testes purchases + ensaio UI |
| R03 | Três respostas com estados distintos | Integração | Testes confirmations + ensaio UI |
| R04 | Expiração não autoriza e não é estendida pela ajuda | Integração | Testes TTL + ensaio UI |
| R05 | Sessão de B não lê nem responde compra de A | Arquitetura | Testes acesso cruzado e sessão |
| R06 | Repetição/concorrência não sobrescreve resposta | Arquitetura | Testes chaves, versão e simultaneidade |
| R07 | Explicação corresponde aos sinais, sem causalidade inventada | Arquitetura/pesquisa | Ferramentas, prompt e comparação de resposta real |
| R08 | Ajuda contextual é útil e informa limites | Pesquisa | D13 + rastro real de ferramentas |
| R09 | Falha não inventa score nem impede resposta humana válida | Arquitetura | Testes de falha/lock + ensaio UI |
| R10 | Status e histórico sobrevivem à recarga/reinício | Integração | Teste com segunda instância + ensaio UI |
| R11 | Compra/ação fictícias e simulação explícitas | Pesquisa | API + inspeção da tela |
| R12 | Outra pessoa reproduz o roteiro | Integração | Registro de execução independente de D11 |

## 5. Critérios de sucesso

| Dimensão | Definição / meta a levar ao piloto | Método e responsável |
|---|---|---|
| Modelo | PR-AUC, recall/precision no limiar e baseline, declarando positivos/corte. Resultado exploratório documentado sem velocidade: 0,146; a antiga ambição 0,80 não foi atingida nem constitui eficácia real. | Dados: [relatório](../04_dados_e_modelo/03_modelo.md), notebooks e hash do modelo. Não houve novo treino nesta revisão. |
| Sistema | Zero autorizações indevidas e zero estados corrompidos nos casos executados. | Arquitetura: pytest e evidências de D11. Passar testes finitos não prova ausência total de falhas. |
| Agente | Consultar a compra correta, explicar fielmente e declarar limite nos casos controlados. | Arquitetura: rastro e resposta; separar modelo de teste de LLM real. |
| Experiência | Meta candidata herdada: ≥3/5 tarefas/participantes definidos no protocolo concluídos sem ajuda; registrar numerador e denominador por condição. Decisões equivocadas são contadas e analisadas; autorização de compra explicitamente desconhecida é achado crítico, nunca tolerância automática de uma por sessão. | Pesquisa: acordar meta e unidade antes da coleta em D13; responder compreensão por chave. |
| Operação | Outro integrante conclui o roteiro sem ajuda dos autores; medir início até resultado, interrupções e erros. | Integração: ensaio UI e relatório com versão. |

## 6. Dados e limitações

Base local sintética: 160.000 registros, 146 fraudes; treino balanceado 234 registros/117 fraudes; teste 32.000/29. Não equivale à base nominal de 900 mil. Positivos concentrados em jan–mar limitam avaliação temporal. O teste já foi explorado, portanto não é holdout intocado.

O manifesto atual de `app/risk/features.py` lista 28 atributos. A relação entre features de velocidade, vazamento temporal e comportamento nacional/real não foi validada nesta revisão. A regra `madrugada` do notebook inclui 0h até 4h (`between(0,4)`); conferir treino/inferência antes de afirmar equivalência. Nome fantasia verificável não está disponível na base; não inventar.

## 7. Aceite e próximas ações

A estrutura está organizada e alinhada ao código inspecionado. Para encerrar: revisão cruzada, evidência de LLM real, ensaio de D11 por outra pessoa e resultados de D13. A matriz central [critérios e pendências](../05_gestao/criterios_e_pendencias.md) distingue esses itens da revisão documental concluída.
