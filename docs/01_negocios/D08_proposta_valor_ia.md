# D08 — Proposta de valor e necessidade de IA agêntica

**ID:** D08 · **Versão:** 0.2 · **Data:** 04/11/2026
**Responsável:** Produto · **Estado:** rascunho revisado documentalmente; revisão cruzada pendente
**Fontes:** registro de evidências, plano de implementação e direcional.

**Revisor:** Arquitetura · **Estado:** rascunho — será atualizado após D13.

---

## 1. Tabela da proposta de valor

| Parte | Conteúdo |
|---|---|
| **Dor e público** | Hipótese: contexto ambíguo ou canal percebido como suspeito podem impedir decisão autônoma e gerar busca de atendimento. A frequência e os canais atuais ainda precisam ser pesquisados. (D01 N1–N4; HIP-03; HIP-04) |
| **Solução em uma frase** | Um assistente de confirmação no app que apresenta a compra, responde dúvidas contextuais e registra a resposta explícita do associado — com revisão humana das exceções. |
| **Quem usa** | **Associado:** usa diretamente o app de confirmação. **Analista:** recebe os casos de exceção (não reconhecimento, dúvida, expiração). |
| **Quem adota e quem paga** | Decisor: a instituição financeira (Sicredi ou equivalente). Hipótese de adoção: a instituição adotaria se o produto reduzisse contatos de atendimento por dúvida e melhorasse a experiência do associado. **Interesse comercial não confirmado** — trata-se de projeto acadêmico sem compromisso da instituição. (HIP-P1-01) |
| **Posicionamento** | Solução vertical de serviços financeiros cooperativos. Benefício ao associado (clareza e autonomia) e adoção pela instituição (redução de atendimento) são papéis diferentes. |
| **Valor para o associado** | Resolver a confirmação sem ligar; entender o que autorizou; saber o desfecho imediatamente. Hipóteses mensuráveis: meta candidata ≥ 3/5 participantes concluem sem ajuda, a acordar antes do piloto; contar todos os erros e tratar autorização de compra explicitamente desconhecida como achado crítico (D09 §5). |
| **Valor para a organização** | Hipótese: redução de contatos de atendimento para dúvidas sobre compras sinalizadas. **Não equivale a redução de perdas financeiras.** Valor das transações sinalizadas ≠ perdas evitadas. (DEC-P1-03) |
| **Por que IA e qual arquétipo** | Ver seção 2 abaixo. |
| **Por que agora** | O desafio Sicredi propõe "alerta preventivo e confirmação pelo associado" (FON-P1-01 p.6). O modelo RF treinado na base sintética fornece scores como ponto de partida. O projeto dispõe de código integrado e ferramentas de desenvolvimento; o chat atual usa configuração Groq e requer chave. Disponibilidade técnica torna o piloto viável, mas não comprova demanda nem gratuidade de operação. |
| **Evidência, custo e limites** | PR-AUC 0,146 no teste com dados sintéticos; meta 0,80 não atingida; modelo não calibrado (FON-P1-02 §5). Nenhuma evidência de redução de fraudes reais. Nenhum teste com usuários executado até esta versão. Ver seção 4 (premissas) e seção 5 (limites). |

---

## 2. Por que IA agêntica e qual arquétipo

### Comparação: mesma interface sem chat × com chat

| Capacidade | A — Sem conversa | B — Com agente |
|---|---|---|
| Apresentar compra e sinais específicos | Sim; dados calculados pelo backend e texto determinístico | Sim; mesmos dados e sinais |
| Informar que o nome fantasia não é verificável | Sim; aviso explícito | Sim; ferramenta e explicação na conversa |
| Identificar estabelecimento sem fonte | Não | Não |
| Responder perguntas livres sobre os dados disponíveis | Sem conversa; textos e FAQ podem cobrir dúvidas previstas | Conversa e escolha de ferramentas; utilidade a testar |
| Encaminhar para revisão | Ação separada | Ação separada ou ferramenta do agente |

**Justificativa como hipótese (HIP-P1-05):** a conversa pode ajudar a interpretar contexto e limites melhor que a mesma interface sem chat. Isso precisa ser observado em D13; não é capacidade comprovadamente superior por ter LLM. Se A funcionar tão bem, manter A como baseline e rever a necessidade da camada conversacional. Sinais são características descritivas, não causas comprovadas do score.

### Arquétipos candidatos (DEC-P1-04)

> Interpretações candidatas dos arquétipos do desafio (FON-P1-01 pp.7–10), a confirmar pelo comportamento executado:

- **Especialista sensível ao contexto:** o agente responde dúvidas sobre a compra específica — não dá respostas genéricas. Consulta ferramentas (`avaliar_transacao`, `consultar_compra`) para basear a explicação nos dados reais.

- **Gestor da fronteira humano–IA:** o agente sabe o que pode resolver (explicar, informar limite, solicitar revisão) e o que não pode (autorizar, recusar, inventar informação). A fronteira é explícita e testável.

### Decomposição saber / decidir / fazer

| Dimensão | Conteúdo |
|---|---|
| **Saber** | Disponibilidade da análise e sinais descritivos da compra (`avaliar_transacao`), sem expor valor numérico de score ao agente; contexto da compra — estabelecimento disponível, valor, data, cartão parcial, MCC, região (`consultar_compra`); estado atual da confirmação e próximos passos (`consultar_status`) |
| **Decidir** | Qual ferramenta consultar para a dúvida específica; quando informar o limite (contexto insuficiente); quando solicitar revisão (dúvida irresolvível) |
| **Fazer** | Chamar ferramentas autorizadas; retornar explicação baseada nos dados; nunca chamar `responder_confirmacao` — essa operação é exclusiva do controle da interface humana |

**Dúvida fora do contexto:** se o associado fizer uma pergunta que nenhuma ferramenta resolve, o agente declara o limite explicitamente e mantém o caminho de revisão. Nunca inventa.

**RAG e múltiplos agentes:** não entram nesta versão — sem necessidade demonstrada para o escopo atual.

---

## 3. Posicionamento nos eixos (interpretação candidata)

| Eixo | Posição candidata | Fonte |
|---|---|---|
| Vertical / Horizontal | Vertical — serviços financeiros cooperativos | FON-P1-01 p.6 (desafio Sicredi específico) |
| Interno / Externo | Interno ao processo da cooperativa (experiência do associado) | Fluxo de confirmação é operação interna |

---

## 4. Premissas de viabilidade

**HIP-REV-01 — cenários ilustrativos, não medições ou previsão da Sicredi.** São escolhas de planejamento para tornar a conta reproduzível sem inventar dados operacionais. Substituir pelos volumes observados e cotações antes de decidir adoção.

| Premissa | Base ilustrativa | Conservador ilustrativo | Fonte / como substituir |
|---|---|---|---|
| Confirmações/mês | 1.000 | 1.000 | Hipótese de escala escolhida nesta revisão |
| Fração que usa chat | 30% | 100% | Hipótese; medir sessões com chat / confirmações |
| Chamadas de LLM por sessão | 2 | 4 | Hipótese; medir chamadas reais, incluindo ciclos de ferramentas |
| Tokens de entrada / saída por chamada | 1.500 / 250 | 1.500 / 250 | Hipótese; substituir por usage do provedor |
| Fração encaminhada para revisão | 10% | 30% | Hipótese; medir revisões / confirmações |
| Minutos por revisão humana | 5 | 10 | Hipótese; medir atendimento |

Sejam **Ci/Co** preços por milhão de tokens de entrada/saída do modelo escolhido, **H** custo humano por hora e **I** infraestrutura mensal, todos na mesma moeda. Não foi consultada cotação comercial nesta revisão; não há alegação de custo zero nem valor público sem fonte.

- Base: 600 chamadas; 900.000 tokens de entrada e 150.000 de saída; 100 revisões × 5 min = 8,33 h. Total ilustrativo = `0,9 × Ci + 0,15 × Co + 8,33 × H + I`.

- Conservador: 4.000 chamadas; 6.000.000 tokens de entrada e 1.000.000 de saída; 300 revisões × 10 min = 50 h. Total ilustrativo = `6 × Ci + 1 × Co + 50 × H + I`.

Para produzir valor monetário faltam Ci/Co, H e I, com modelo, URL/fonte, moeda, data, limites de quota e responsável pela cotação. Produto consolida; Arquitetura mede uso de tokens/infra; Pesquisa mede esforço. Economia eventual requer baseline de esforço realmente evitado, não só quantidade de transações sinalizadas.

## 5. Métricas do protótipo × efeitos operacionais

| Métrica | Evidência no protótipo | Limite |
|---|---|---|
| Conclusão independente | Tarefas concluídas sem ajuda / tarefas tentadas | Piloto D13 ainda não executado |
| Compreensão | Respostas corretas / perguntas, por chave e condição | Sem generalizar a todos os associados |
| Decisões equivocadas | Contagem por cenário/condição e gravidade | Autorizar compra explicitamente desconhecida é achado crítico |
| Redução de atendimento | Não demonstrável só por teste de tela | Exige baseline e volume operacional real |
| Redução de perdas por fraude | Não demonstrada | Exige fraude confirmada e medição operacional |
| Desempenho do modelo em produção | Não demonstrado | Resultado sintético exploratório não prova eficácia real |

**Separação obrigatória (DEC-P1-03):** resultados do piloto (3–5 pessoas) não comprovam efeito operacional. Valor das transações sinalizadas ≠ perdas evitadas. Esta versão apresenta hipóteses mensuráveis, não resultados.

---

## 6. Este documento será atualizado após D13

Ao concluir D13 (validação), atualizar:

- Seção 1 (valor para o associado): substituir metas por resultados reais de compreensão e conclusão.

- Seção 1 (evidência): adicionar TST-xx com perfil dos participantes, versão testada e resultados.

- Seção 4 (premissas): incorporar contagem de mensagens de chat por caso se o piloto for instrumentado.

- Seção 2 (justificativa de IA): atualizar se o piloto mostrar que texto fixo resolve igualmente bem o caso de nome ambíguo.
