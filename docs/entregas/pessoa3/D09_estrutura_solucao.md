# D09 ÔÇö Estrutura da solu├º├úo e crit├®rios de sucesso

**ID:** D09 ┬À **Vers├úo:** 0.1 ┬À **Data:** 29/10/2026
**Respons├ível:** Pessoa 3 ┬À **Revisor:** Pessoa 4
**Estado:** rascunho
**Depende de:** D05, D07, D08 (conceito e valor); **Alimenta:** D10, D11, D13

---

## 1. Problema e usu├írio

**Problema central.** O associado recebe uma compra sinalizada e precisa decidir se a reconhece ÔÇö mas n├úo tem contexto suficiente para isso: n├úo sabe por que o alerta foi disparado, o que a resposta vai gerar e como seguir se ainda tiver d├║vida.

**Usu├írio principal.** O associado do Sicredi que recebe uma solicita├º├úo de confirma├º├úo de compra.

**Atores secund├írios:**
- **Analista de preven├º├úo a fraudes** ÔÇö recebe os casos que o associado n├úo resolve (d├║vida, n├úo reconhecimento, expira├º├úo).
- **Sistema/backend** ÔÇö avalia a compra, aplica a pol├¡tica e persiste estados.
- **Agente conversacional** ÔÇö esclarece d├║vidas com base no contexto dispon├¡vel; n├úo autoriza compras.

**Jornada priorit├íria** (ponto de ruptura identificado no D03):

> Associado recebe o alerta ÔåÆ n├úo entende o nome do estabelecimento ÔåÆ n├úo consegue decidir ÔåÆ n├úo responde ÔåÆ confirma├º├úo expira sem resultado claro.

---

## 2. Capacidades do agente (saber / decidir / fazer)

| Dimens├úo | Detalhe |
|---|---|
| **Saber** | Score do modelo e sinais descritivos dispon├¡veis (`avaliar_transacao`); contexto da compra: valor, data, estabelecimento, cart├úo parcial (`consultar_compra`); estado atual da confirma├º├úo e pr├│ximos passos permitidos (`consultar_status`). |
| **Decidir** | Consultar qual ferramenta usar para responder a d├║vida; informar limite quando n├úo houver contexto suficiente; solicitar revis├úo humana quando a d├║vida n├úo puder ser resolvida (`solicitar_revisao`). |
| **Fazer** | Chamar ferramentas via inje├º├úo de depend├¬ncia; retornar explica├º├úo fundamentada nos dados; nunca chamar `responder_confirmacao` ÔÇö essa opera├º├úo ├® exclusiva do controle da interface humana. |

---

## 3. Componentes da solu├º├úo

| Componente | Papel | Estado |
|---|---|---|
| **Modelo RF** | Produz score de fraude (0ÔÇô1); sinais descritivos s├úo apurados separadamente; modelo a carregar de `outputs/modelo_rf.joblib` no processo do backend | Treinado e avaliado em dados sint├®ticos (notebooks 02/03); deploy no watsonx.ai testado em 27/10 como evid├¬ncia |
| **Pol├¡tica de decis├úo** | Transforma score em tratamento: liberar, confirmar ou encaminhar para revis├úo; determin├¡stica, versionada e test├ível | Planejada (ver ┬º3 do plano); limiares a definir na valida├º├úo |
| **Backend FastAPI + SQLAlchemy** | Valida sess├úo, vincula associado/compra, controla expira├º├úo, persiste estados/eventos, exp├Áe API JSON | Planejado; contratos publicados em D10 |
| **Agente Pydantic AI** | Recebe pergunta do associado, escolhe ferramenta, retorna explica├º├úo contextualizada | Planejado; provedor LLM a confirmar (Groq/Gemini/Granite) |
| **Interface do associado** (React + Carbon) | Mostra compra, alerta, pergunta e tr├¬s respostas; campo de d├║vida; status final | Em adapta├º├úo (Leonardo, Watson PR #7); cards C10/C13 ativos |
| **Console de exce├º├Áes** | Vis├úo da analista para casos que precisam de revis├úo humana | Planejado; limitado ├ás exce├º├Áes |
| **IBM Bob** | Ferramenta de desenvolvimento, revis├úo, testes e documenta├º├úo; sess├Áes exportadas em `bob_sessions/` | Obrigat├│rio pelo guia IBM; em uso |

---

## 4. Requisitos ligados a necessidades e testes

| Req. | Necessidade | Como verificar | Evid├¬ncia a coletar |
|---|---|---|---|
| R01 | Avalia├º├úo autom├ítica de compra | Pol├¡tica produz tratamento versionado sem decis├úo pr├®via do analista | Log com score, pol├¡tica e vers├úo para cada compra de teste |
| R02 | Confirma├º├úo vinculada ├á compra | ID, valor, data e contexto correto aparecem antes da resposta | Inspe├º├úo da tela com compra de teste e dado esperado |
| R03 | Tr├¬s respostas expl├¡citas | Autorizar, recusar e d├║vida t├¬m resultados distintos e persistidos | Executar cada resposta; conferir estado e evento no banco |
| R04 | Expira├º├úo | Resposta fora do prazo n├úo libera a transa├º├úo | For├ºar expira├º├úo e tentar responder; confirmar rejei├º├úo |
| R05 | Autoriza├º├úo por usu├írio | Usu├írio B n├úo l├¬ nem responde ├á confirma├º├úo de A | Criar sess├úo de dois associados fict├¡cios e testar acesso cruzado |
| R06 | Idempot├¬ncia e concorr├¬ncia | Duas requisi├º├Áes n├úo produzem dois resultados conflitantes | Disparar duas respostas simult├óneas; conferir um ├║nico estado |
| R07 | Explica├º├úo fiel | N├║meros e sinais correspondem aos dados consultados | Comparar output do agente com o retorno bruto de `avaliar_transacao` |
| R08 | D├║vida contextual | Agente consulta o caso, informa limite e permite revis├úo | Enviar pergunta sem contexto de estabelecimento; registrar resposta do agente |
| R09 | Erro seguro | Falha n├úo gera score inventado ou autoriza├º├úo | Simular falha do modelo/LLM e verificar resposta do sistema |
| R10 | Hist├│rico | Recarregar ou reiniciar preserva resposta e resultado | Recarregar a p├ígina ap├│s cada resposta; confirmar estado exibido |
| R11 | Transpar├¬ncia | Dados fict├¡cios e a├º├Áes simuladas aparecem na interface | Inspe├º├úo visual da tela principal |
| R12 | Acesso reproduz├¡vel | Outra pessoa consegue concluir o fluxo seguindo o guia | P4 reproduz o guia de D11 sem ajuda dos autores t├®cnicos |

**Prioridade P0:** R01ÔÇôR07 e R09ÔÇôR12. R08 (d├║vida contextual) ├® essencial para demonstrar o papel ag├¬ntico, mas sua falha n├úo pode bloquear o caminho expl├¡cito de resposta.

---

## 5. Crit├®rios de sucesso por dimens├úo

| Dimens├úo | O que mede | Meta interna | M├®todo de coleta |
|---|---|---|---|
| **Modelo** | PR-AUC no teste com a propor├º├úo de fraudes da base sint├®tica; compara├º├úo com `fraud_score` baseline; vers├úo e schema declarados | Meta aspiracional: PR-AUC ÔëÑ 0,80 sem features de velocidade. Resultado documentado: 0,146; meta n├úo atingida | Relat├│rio reproduz├¡vel do notebook 03; resultado explorat├│rio, n├úo valida├º├úo em dados reais nem holdout intocado |
| **Sistema** | Todos os cen├írios do ┬º9 do plano passam; nenhuma falha cr├¡tica de autoriza├º├úo | 0 autoriza├º├Áes indevidas; 0 estados corrompidos | Bateria de testes automatizados (C25/C26) |
| **Agente** | Ferramenta correta chamada para cada tipo de d├║vida; explica├º├úo fiel ao dado retornado; limite declarado quando contexto falta | Rastro de ferramentas coerente com a resposta em todos os casos de teste | Inspe├º├úo de logs com ferramentas chamadas vs. resposta exibida |
| **Experi├¬ncia** | Conclus├úo da tarefa sem ajuda do moderador; compreens├úo da consequ├¬ncia da resposta | ÔëÑ 3/5 participantes concluem sem ajuda; Ôëñ 1 decis├úo equivocada por sess├úo | Tarefas e perguntas de compreens├úo de D13 |
| **Opera├º├úo** | Fluxo reproduz├¡vel por outra pessoa seguindo o guia | P4 conclui todos os cen├írios de D11 sem interven├º├úo dos autores | D11 executado por P4 antes da entrega final |

---

## 6. Dados dispon├¡veis e limita├º├Áes

| Dado | Disponibilidade | Limita├º├úo |
|---|---|---|
| Base de treino e teste | `data/processed/` ÔÇö 234 linhas treino, 32.000 teste | Base sint├®tica com 160k (n├úo os 900k descritos nas orienta├º├Áes); todas as fraudes em janÔÇômar; poss├¡vel artefato nas features de velocidade |
| Modelo serializado | `outputs/modelo_rf.joblib` (a gerar) | N├úo calibrado; score Ôëá probabilidade real; limiar escolhido por F2, n├úo por custo de neg├│cio |
| Casos de demonstra├º├úo | `agente/tools/pontuar_transacao.py` ÔÇö 2 casos fixos (leg├¡tima e fraude) | Apenas 2 casos; o estoque de demonstra├º├úo precisa ser ampliado para cobrir os 13 cen├írios do ┬º9 do plano |
| Hist├│rico transacional | Dispon├¡vel no CSV sint├®tico | N├úo versionado no reposit├│rio; notebooks precisam do CSV em `data/` para rodar |
| Contexto de estabelecimento | Apenas `acceptor_risk` e `acceptor_region` no modelo | Nome comercial/nome fantasia n├úo dispon├¡vel; agente deve informar esse limite explicitamente |

---

## 7. Depend├¬ncias de acesso

| Item | Respons├ível | Estado |
|---|---|---|
| LLM para o agente (Groq, Gemini ou Granite) | P3 / equipe | A confirmar; chave em vari├ível de ambiente |
| Deploy watsonx.ai (evid├¬ncia, n├úo runtime) | P3 | Testado em 27/10; resultado em `docs/specs/teste_integracao_orchestrate_wml.md` |
| Hospedagem (Railway ou equivalente) | A definir | Planejada; `DATABASE_URL` configur├ível |
| Frontend Watson (PR #7) | Leonardo | C├│digo dispon├¡vel; integra├º├úo planejada em C10/C13 |

---

## 8. Limita├º├Áes e pr├│ximos passos

- [ ] Definir limiares da pol├¡tica com base em valida├º├úo, n├úo no conjunto de teste j├í usado.
- [ ] Fechar o manifesto de features: c├│digo lista 28; documentos anteriores mencionam totais diferentes.
- [ ] Confirmar o provedor LLM e testar a substitui├º├úo de provedor como configura├º├úo.
- [ ] Ampliar os casos de demonstra├º├úo para cobrir os 13 cen├írios do ┬º9 do plano.
- [ ] Alinhar defini├º├úo de `madrugada`, representa├º├úo de nulos e tipos de categorias entre treino e infer├¬ncia.
- [ ] Ap├│s D13, atualizar m├®tricas de experi├¬ncia com resultados reais.
