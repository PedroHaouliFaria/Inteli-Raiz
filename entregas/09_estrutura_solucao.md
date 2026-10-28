# D09 — Estrutura da solução e critérios de sucesso

**ID:** D09 · **Versão:** 0.1 · **Data:** 29/10/2026
**Responsável:** Pessoa 3 · **Revisor:** Pessoa 4
**Estado:** rascunho
**Depende de:** D05, D07, D08 (conceito e valor); **Alimenta:** D10, D11, D13

---

## 1. Problema e usuário

**Problema central.** O associado recebe uma compra sinalizada e precisa decidir se a reconhece — mas não tem contexto suficiente para isso: não sabe por que o alerta foi disparado, o que a resposta vai gerar e como seguir se ainda tiver dúvida.

**Usuário principal.** O associado do Sicredi que recebe uma solicitação de confirmação de compra.

**Atores secundários:**
- **Analista de prevenção a fraudes** — recebe os casos que o associado não resolve (dúvida, não reconhecimento, expiração).
- **Sistema/backend** — avalia a compra, aplica a política e persiste estados.
- **Agente conversacional** — esclarece dúvidas com base no contexto disponível; não autoriza compras.

**Jornada prioritária** (ponto de ruptura identificado no D03):

> Associado recebe o alerta → não entende o nome do estabelecimento → não consegue decidir → não responde → confirmação expira sem resultado claro.

---

## 2. Capacidades do agente (saber / decidir / fazer)

| Dimensão | Detalhe |
|---|---|
| **Saber** | Score e sinais da avaliação do modelo (`avaliar_transacao`); contexto da compra: valor, data, estabelecimento, cartão parcial (`consultar_compra`); estado atual da confirmação e próximos passos permitidos (`consultar_status`). |
| **Decidir** | Consultar qual ferramenta usar para responder a dúvida; informar limite quando não houver contexto suficiente; solicitar revisão humana quando a dúvida não puder ser resolvida (`solicitar_revisao`). |
| **Fazer** | Chamar ferramentas via injeção de dependência; retornar explicação fundamentada nos dados; nunca chamar `responder_confirmacao` — essa operação é exclusiva do controle da interface humana. |

---

## 3. Componentes da solução

| Componente | Papel | Estado |
|---|---|---|
| **Modelo RF** | Produz score de fraude (0–1) e sinais; carregado em `outputs/modelo_rf.joblib` no processo do backend | Treinado e validado (notebooks 02/03); deploy no watsonx.ai testado em 27/10 como evidência |
| **Política de decisão** | Transforma score em tratamento: liberar, confirmar ou encaminhar para revisão; determinística, versionada e testável | Planejada (ver §3 do plano); limiares a definir na validação |
| **Backend FastAPI + SQLAlchemy** | Valida sessão, vincula associado/compra, controla expiração, persiste estados/eventos, expõe API JSON | Planejado; contratos publicados em D10 |
| **Agente Pydantic AI** | Recebe pergunta do associado, escolhe ferramenta, retorna explicação contextualizada | Planejado; provedor LLM a confirmar (Groq/Gemini/Granite) |
| **Interface do associado** (React + Carbon) | Mostra compra, alerta, pergunta e três respostas; campo de dúvida; status final | Em adaptação (Leonardo, Watson PR #7); cards C10/C13 ativos |
| **Console de exceções** | Visão da analista para casos que precisam de revisão humana | Planejado; limitado às exceções |
| **IBM Bob** | Ferramenta de desenvolvimento, revisão, testes e documentação; sessões exportadas em `bob_sessions/` | Obrigatório pelo guia IBM; em uso |

---

## 4. Requisitos ligados a necessidades e testes

| Req. | Necessidade | Como verificar | Evidência a coletar |
|---|---|---|---|
| R01 | Avaliação automática de compra | Política produz tratamento versionado sem decisão prévia do analista | Log com score, política e versão para cada compra de teste |
| R02 | Confirmação vinculada à compra | ID, valor, data e contexto correto aparecem antes da resposta | Inspeção da tela com compra de teste e dado esperado |
| R03 | Três respostas explícitas | Autorizar, recusar e dúvida têm resultados distintos e persistidos | Executar cada resposta; conferir estado e evento no banco |
| R04 | Expiração | Resposta fora do prazo não libera a transação | Forçar expiração e tentar responder; confirmar rejeição |
| R05 | Autorização por usuário | Usuário B não lê nem responde à confirmação de A | Criar sessão de dois associados fictícios e testar acesso cruzado |
| R06 | Idempotência e concorrência | Duas requisições não produzem dois resultados conflitantes | Disparar duas respostas simultâneas; conferir um único estado |
| R07 | Explicação fiel | Números e sinais correspondem aos dados consultados | Comparar output do agente com o retorno bruto de `avaliar_transacao` |
| R08 | Dúvida contextual | Agente consulta o caso, informa limite e permite revisão | Enviar pergunta sem contexto de estabelecimento; registrar resposta do agente |
| R09 | Erro seguro | Falha não gera score inventado ou autorização | Simular falha do modelo/LLM e verificar resposta do sistema |
| R10 | Histórico | Recarregar ou reiniciar preserva resposta e resultado | Recarregar a página após cada resposta; confirmar estado exibido |
| R11 | Transparência | Dados fictícios e ações simuladas aparecem na interface | Inspeção visual da tela principal |
| R12 | Acesso reproduzível | Outra pessoa consegue concluir o fluxo seguindo o guia | P4 reproduz o guia de D11 sem ajuda dos autores técnicos |

**Prioridade P0:** R01–R07 e R09–R12. R08 (dúvida contextual) é essencial para demonstrar o papel agêntico, mas sua falha não pode bloquear o caminho explícito de resposta.

---

## 5. Critérios de sucesso por dimensão

| Dimensão | O que mede | Meta interna | Método de coleta |
|---|---|---|---|
| **Modelo** | PR-AUC no teste com proporção real; comparação com `fraud_score` baseline; versão e schema declarados | PR-AUC ≥ 0,80 sem features de velocidade (ou documentar limitação explicitamente) | Relatório reproduzível do notebook 03 |
| **Sistema** | Todos os cenários do §9 do plano passam; nenhuma falha crítica de autorização | 0 autorizações indevidas; 0 estados corrompidos | Bateria de testes automatizados (C25/C26) |
| **Agente** | Ferramenta correta chamada para cada tipo de dúvida; explicação fiel ao dado retornado; limite declarado quando contexto falta | Rastro de ferramentas coerente com a resposta em todos os casos de teste | Inspeção de logs com ferramentas chamadas vs. resposta exibida |
| **Experiência** | Conclusão da tarefa sem ajuda do moderador; compreensão da consequência da resposta | ≥ 3/5 participantes concluem sem ajuda; ≤ 1 decisão equivocada por sessão | Tarefas e perguntas de compreensão de D13 |
| **Operação** | Fluxo reproduzível por outra pessoa seguindo o guia | P4 conclui todos os cenários de D11 sem intervenção dos autores | D11 executado por P4 antes da entrega final |

---

## 6. Dados disponíveis e limitações

| Dado | Disponibilidade | Limitação |
|---|---|---|
| Base de treino e teste | `data/processed/` — 234 linhas treino, 32.000 teste | Base sintética com 160k (não os 900k descritos nas orientações); todas as fraudes em jan–mar; possível artefato nas features de velocidade |
| Modelo serializado | `outputs/modelo_rf.joblib` (a gerar) | Não calibrado; score ≠ probabilidade real; limiar escolhido por F2, não por custo de negócio |
| Casos de demonstração | `agente/tools/pontuar_transacao.py` — 2 casos fixos (legítima e fraude) | Apenas 2 casos; o estoque de demonstração precisa ser ampliado para cobrir os 13 cenários do §9 do plano |
| Histórico transacional | Disponível no CSV sintético | Não versionado no repositório; notebooks precisam do CSV em `data/` para rodar |
| Contexto de estabelecimento | Apenas `acceptor_risk` e `acceptor_region` no modelo | Nome comercial/nome fantasia não disponível; agente deve informar esse limite explicitamente |

---

## 7. Dependências de acesso

| Item | Responsável | Estado |
|---|---|---|
| LLM para o agente (Groq, Gemini ou Granite) | P3 / equipe | A confirmar; chave em variável de ambiente |
| Deploy watsonx.ai (evidência, não runtime) | P3 | Testado em 27/10; resultado em `docs/specs/teste_integracao_orchestrate_wml.md` |
| Hospedagem (Railway ou equivalente) | A definir | Planejada; `DATABASE_URL` configurável |
| Frontend Watson (PR #7) | Leonardo | Código disponível; integração planejada em C10/C13 |

---

## 8. Limitações e próximos passos

- [ ] Definir limiares da política com base em validação, não no conjunto de teste já usado.
- [ ] Fechar o manifesto de features: código lista 28; documentos anteriores mencionam totais diferentes.
- [ ] Confirmar o provedor LLM e testar a substituição de provedor como configuração.
- [ ] Ampliar os casos de demonstração para cobrir os 13 cenários do §9 do plano.
- [ ] Alinhar definição de `madrugada`, representação de nulos e tipos de categorias entre treino e inferência.
- [ ] Após D13, atualizar métricas de experiência com resultados reais.
