# D13 — Validação da Experiência e Registro de Melhorias

**ID:** D13 · **Versão:** 0.2 · **Data:** 28/10/2026 (corrigido após revisão do Codex)
**Responsável:** Pessoa 4 (organiza, aplica e consolida); Pessoa 2 (modera sessões)  
**Estado:** **protocolo pronto** — tarefas, chave de avaliação e modelos de registro definidos; pesquisa não executada; sem participantes ou resultados reais.  
**Fontes:** plano `8942cc5` §9; D06 `8a7aefc`; roteiro Pessoa 2 `8a7aefc`; D09 `f732159` §5.

> **Protocolo pronto é um estado intermediário, não conclusão de D13.** D13 só fica concluída no recorte testado após coleta real, síntese, correções necessárias e reteste.

---

## 1. Perguntas e hipóteses a verificar

As hipóteses abaixo vêm do pacote da Pessoa 2 (`evidencias_e_hipoteses.md` de `8a7aefc`) e do plano. IDs `HIP-xx` pertencem ao registro da Pessoa 2 — não são resultados novos.

| ID | Hipótese | Impacto se falsa | Medida correspondente |
|---|---|---|---|
| HIP-01 | Associado confunde "não reconheço" com "bloquear todo o cartão" | Tela de resultado precisa ser corrigida; linguagem atual invalida D12 | C5 — compreensão do efeito de `DENY` |
| HIP-02 | Associado não sabe se pode responder após pedir ajuda | Tela de atendimento precisa mostrar status da confirmação | C4 — compreensão após pedido de ajuda |
| HIP-03 | Nome ambíguo do estabelecimento gera abandono ou decisão equivocada | Agente precisa informar o limite; tela precisa mostrar dado disponível | C6 — compreensão do que o sistema sabe |
| HIP-05 | Associado não sabe o efeito de cada resposta antes de escolher | Descrição de efeito abaixo de cada botão (ver D12 §3.2) | C2 — efeito de cada opção |
| HIP-09 | Associado não entende o desfecho após responder | Tela de resultado precisa ser explícita | C1/C2 — compreensão pós-resposta |

**Perguntas de pesquisa adicionais de D13:**
1. O fluxo com ajuda contextual do agente reduz dúvidas sobre o alerta em comparação ao fluxo com texto fixo, sem aumentar autorizações equivocadas?
2. A distinção entre "Estou em dúvida" e "Quero falar com alguém" é compreendida antes de qualquer instrução?
3. O associado consegue concluir a tarefa sem ajuda do moderador?

---

## 2. Participantes e contexto

**Proposta interna:** 3–5 participantes no total, conforme acesso. Essa quantidade é uma proposta de planejamento; não é exigência oficial nem amostra representativa.

| Perfil prioritário | Por que incluir | Como registrar |
|---|---|---|
| Associado de cooperativa de crédito (qualquer idade) | Usuário direto | "Associado — cooperativa" |
| Usuário de serviços financeiros com cartão | Comportamento análogo quando associado não está acessível | "Usuário financeiro — não cooperativa" |
| Colega de equipe sem envolvimento na implementação | Testa reprodutibilidade do roteiro e detecta viés | "Colega — equipe (sem impl.)" |

Registrar se é colega de equipe, parente, conhecido ou externo. Não generalizar resultado de uma única sessão para "os associados".

**Sem participantes disponíveis:** entregar protocolo e modelos de registro preenchidos com "não executado". Não inventar observações.

---

## 3. Versão a testar

| Item | Requisito | Estado atual |
|---|---|---|
| Protótipo (texto + tela) | Mínimo para Bloco B | Não disponível na versão `212655c` sem adaptação de C10 |
| Aplicação integrada | Necessário para D13 completo | Bloqueado (ver D11) |
| Commit e ambiente declarados | Obrigatório para qualquer resultado | A preencher quando disponível |

Enquanto o protótipo adaptado não existir, o Bloco B e as tarefas de compreensão de interface não podem ser executados. Bloco A (entrevista de experiência real) pode ser executado de forma independente.

---

## 4. Desenho do piloto — duas condições

| Condição | Descrição | O que mede |
|---|---|---|
| **A — Sem ajuda contextual** | Participante usa a mesma interface e vê as mesmas informações da compra; chat **não está disponível** | Decisão e compreensão sem apoio contextual do agente |
| **B — Com ajuda contextual** | Participante usa a mesma interface e vê as mesmas informações da compra; chat **está disponível** | Decisão e compreensão com apoio contextual do agente |

**As duas condições usam a mesma interface e as mesmas informações.** O que varia é exclusivamente a disponibilidade do chat do agente. Não apresentar informações diferentes entre as condições; não usar uma tela mais completa em B. Alternar a ordem entre participantes (A→B / B→A) e registrar qual condição veio primeiro. Se apenas uma condição estiver disponível, registrar "apenas condição X" e não comparar.

Uma comparação de especificações ou walkthrough da equipe não é resultado de teste comparativo com usuários.

---

## 5. Sequência da sessão

1. **Apresentação e autorização** (adaptar do roteiro da Pessoa 2, `roteiro_pesquisa.md` `8a7aefc`, Bloco intro): fins educacionais, sem dados sensíveis, anonimização, participante pode interromper.
2. **Bloco A — Experiência real** (usar roteiro P2, perguntas P1–P7): sem mostrar a solução; deixar a pessoa falar; não sugerir respostas.
3. **Intervalo de transição:** não revelar o que está sendo avaliado.
4. **Bloco B — Tarefa de compreensão** (novo neste pacote): apresentar cenário controlado; tarefa primeiro, perguntas depois.
5. **Encerramento:** agradecimento; perguntar se há algo a acrescentar.

**Regra de aplicação do Bloco B:** apresentar a tela/texto e pedir que a pessoa aja primeiro. Só depois fazer as perguntas. Perguntas antes da tarefa preparam artificialmente e invalidam a observação.

**Intervenções do moderador:** registrar toda ajuda oferecida, momento e tipo (ajuda de navegação / ajuda de compreensão / dica de conceito). Separar respostas espontâneas de respostas após pergunta específica.

---

## 6. Tarefas e cenários controlados (Bloco B)

As instruções abaixo são **neutras** — não revelam a resposta esperada.

### Tarefa 1 — Compra que o participante fictício reconhece

> **Contexto dado ao participante antes de ver a tela** (lido em voz alta):
> "Imagine que você é o Valdir. Ontem você foi à farmácia perto de casa e comprou um remédio. Você usou o cartão final 7821."
>
> **Estímulo** (mostrar a tela ou ler o texto):
> R$ 35,00 · Farmácia Central · cartão final 7821 · ontem, 14:32 · compra presencial
>
> "Sem que eu explique nada, faça o que faria de verdade e pense em voz alta."

### Tarefa 2 — Compra que o participante fictício não reconhece

> **Contexto dado ao participante antes de ver a tela**:
> "Imagine que você é o Valdir. Nas últimas duas semanas você não fez nenhuma compra online nem em São Paulo. Você não reconhece nenhuma transação desse tipo."
>
> **Estímulo**:
> R$ 2.349,90 · identificação não disponível (MCC 5411 — supermercado) · cartão final 4821 · hoje, 03:14 · compra online em São Paulo, SP
>
> "Faça o que faria de verdade."

### Tarefa 3 — Compra ambígua

> **Contexto dado ao participante antes de ver a tela**:
> "Imagine que você é o Valdir. Você comprou algo numa farmácia recentemente, mas não lembra exatamente o valor. Pode ter sido esse ou outro estabelecimento — você não tem certeza."
>
> **Estímulo**:
> R$ 189,00 · MCC 5912 — farmácia · cartão final 4821 · ontem, 22:50 · compra online
>
> "Faça o que faria de verdade."

Em cenário ambíguo, pedir ajuda, registrar dúvida (`UNSURE`) ou pedir atendimento são respostas possíveis e aceitáveis. Não contar escolha prudente como erro só porque diferiu de uma resposta esperada pelo pesquisador.

---

## 7. Métricas e chave de avaliação

Definir **antes da coleta**. Usar para preencher o registro após a sessão, nunca durante.

### 7.1 Medidas quantitativas

| Medida | Definição | Como registrar |
|---|---|---|
| **Conclusão independente** | Tarefa atingiu o objetivo sem qualquer ajuda do moderador | `S` (sim) / `N` (não) por tarefa; preservar falhas e abandonos |
| **Tempo** | Início da tarefa (apresentação da tela/texto) até estado final definido (resposta enviada ou abandono) | Minutos e segundos; registrar interrupções separadamente |
| **Dúvidas / retrabalho** | Hesitações observáveis, voltas, pedidos de explicação, cliques errados | Contagem e descrição breve |

### 7.2 Chave de compreensão

| Pergunta | Resposta **correta** | Resposta **parcial** | Resposta **incorreta** | Resposta **"não sei"** |
|---|---|---|---|---|
| **C1 — O que está sendo verificado** | Descreve o valor e/ou o estabelecimento da tela, sem dados de outras compras | Descreve só parte dos dados visíveis (ex.: só o valor, sem o estabelecimento) | Descreve compra diferente da apresentada | "Não entendi o que está pedindo" / sem resposta |
| **C2 — Efeito de cada opção** | Descreve efeito distinto e correto para as três opções: "Reconheço" → liberação simulada; "Não reconheço" → recusa da compra + revisão aberta (sem bloquear o cartão inteiro); "Estou em dúvida" → revisão pendente | Descreve corretamente 2 de 3 efeitos; ou omite a distinção de bloqueio do cartão mas não a afirma | Descreve o mesmo efeito para duas ou mais opções; afirma que qualquer opção bloqueia o cartão inteiro | "Não sei o que aconteceria" para pelo menos uma opção |
| **C3 — Opção de falar com alguém** | Identifica que é ação separada dos três botões; não confunde com "Estou em dúvida" | Identifica como ação separada mas associa incorretamente a algum efeito colateral (ex.: "encerra a confirmação") | Afirma que pedir atendimento responde à confirmação, ou que é a mesma coisa que "Estou em dúvida" | "Não vi essa opção" / "Não sei o que faz" |
| **C4 — Pode responder após pedir ajuda?** | "Sim, enquanto o prazo não tiver expirado" (ou equivalente) | "Acho que sim, mas não tenho certeza" | "Não" ou "O prazo foi prorrogado ao pedir ajuda" | "Não sei" |
| **C5 — O que acontece com o cartão ao não reconhecer** | "A compra foi recusada / encaminhada para revisão" — qualquer resposta que não afirme bloqueio automático do cartão inteiro | "Não sei o que acontece com o cartão, mas sei que a compra foi recusada" | Afirma que o cartão inteiro foi bloqueado automaticamente | "Não sei o que acontece" (sem mencionar a compra nem o cartão) |
| **C6 — O que o sistema sabe sobre a compra** | Menciona dados presentes na tela (valor, categoria, data) e/ou que o nome não estava disponível | Menciona só parte dos dados visíveis | Menciona informações que não estavam na tela; afirma que o sistema sabe o nome completo quando ele não estava disponível | "Não presti atenção" / sem resposta |

**Regras de aplicação da chave:**
- Registrar a resposta literal antes de classificar.
- Informação ausente no estímulo: não marcar como erro o que o teste não apresentou (ex.: se a tela não mostrou prazo, não marcar como erro não saber o prazo).
- "Não bloqueia o cartão" (C5): não marcar como incorreto só por mencionar a palavra "bloqueio" — o critério é afirmar bloqueio automático do cartão inteiro.
- Resposta parcial ≠ incorreta: registrar o que estava correto e o que estava ausente ou errado.
- "Não sei" ≠ incorreto: registrar separadamente; não contar como erro de compreensão quando o estímulo não fornecia a informação necessária.

---

## 8. Modelo de registro por sessão

```
Sessão: P4-SES-[nn]
Data:
Participante anonimizado: P4-PAR-[nn]
Perfil:
Condição / ordem: A→B ou B→A
Versão / commit testado:
Moderador:

Bloco A — Experiência real
  Resposta a P1 (último episódio):
  Resposta a P2 (primeira informação):
  Resposta a P3 (confiança no canal):
  Resposta a P4 (reconhecimento da compra):
  Resposta a P5 (buscou ajuda?):
  Resposta a P6 (consequência esperada):
  Resposta a P7 (desfecho):
  Intervenções do moderador:

Bloco B — Tarefa e compreensão
  Tarefa 1:
    Conclusão independente: S / N
    Tempo:
    Ação observada:
    Dúvidas / retrabalho:
    Intervenção do moderador:
  Tarefa 2: [idem]
  Tarefa 3: [idem]

  Perguntas abertas (após tarefas):
    C1 (resposta literal):
    C2 (resposta literal por opção):
    C3 (resposta literal):
    C4 (resposta literal):
    C5 (resposta literal):
    C6 (resposta literal):

  Avaliação segundo chave (por pergunta): correto / parcial / incorreto / não sei / não aplicado
  Justificativa de cada avaliação:
  Resposta parcial — o que estava correto / o que faltou:

Observações gerais:
Achados desta sessão (P4-OBS-[nn]):
```

---

## 9. Tabela de resultados — modelo a preencher

Legenda: **C** = correto · **P** = parcial · **I** = incorreto · **NS** = não sei · **NA** = não aplicado

| Participante | Perfil | Condição/ordem | Versão | Tarefa | Conclusão indep. | Tempo | C1 | C2 | C3 | C4 | C5 | C6 | Observação | Achado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P4-PAR-01 | — | — | — | T1 | — | — | — | — | — | — | — | — | não executado | — |
| P4-PAR-01 | — | — | — | T2 | — | — | — | — | — | — | — | — | não executado | — |
| P4-PAR-01 | — | — | — | T3 | — | — | — | — | — | — | — | — | não executado | — |

---

## 10. Prefixos de registro

| Prefixo | Uso |
|---|---|
| `P4-SES-xx` | Sessões desta execução de D13 |
| `P4-PAR-xx` | Participantes anonimizados |
| `P4-OBS-xx` | Observações desta execução |
| `P4-ACH-xx` | Achados desta execução |
| `P4-EVI-xx` | Evidências desta execução |

Não sobrescrever `HIP-xx`, `OBS-xx`, `FON-xx` do pacote da Pessoa 2. Citar IDs da pesquisa como origem, não como resultados novos.

---

## 11. Modelo de achado

Cada achado após a coleta precisa de:

```
ID: P4-ACH-[nn]
Observação de origem: P4-OBS-[nn] ou P4-SES-[nn]
Hipótese relacionada: HIP-xx (Pessoa 2) ou nova
Evidência: P4-EVI-[nn]
Descrição:
Impacto: [barreira crítica / dificuldade / confusão / sugestão]
Gravidade: [crítica / alta / média / baixa]
  Crítica: autorização indevida, perda/duplicação de resposta, acesso cruzado, decisão incorreta baseada em informação errada
  Alta: falha de compreensão que levaria a abandono ou erro sistemático
  Média: dificuldade observada; tarefa concluída com esforço adicional
  Baixa: problema visual ou de texto; não afeta a decisão
Alteração solicitada:
Responsável por função:
Estado: [identificado / em correção / corrigido / retestado]
Reteste: [versão/commit + resultado]
```

---

## 12. Relatório e reteste

Após coleta, sintetizar:
1. Contagem de conclusão independente por tarefa e condição.
2. Distribuição de respostas por pergunta da chave.
3. Achados por gravidade com evidência.
4. Alterações propostas, responsável e estado.
5. Reteste: para cada achado crítico/alto, executar novamente o cenário afetado após correção e registrar resultado.

Apresentar contagens e limitações; não prometer redução de fraudes ou perdas com um piloto de 3–5 pessoas.

---

## 13. Aceite de D13

**Protocolo pronto é estado intermediário.** Para avançar:

- [ ] Protótipo ou aplicação disponível (D12 ou D11).
- [ ] Pessoa 2 executa Bloco A com pelo menos 2 participantes; Pessoa 4 executa Bloco B.
- [ ] Tabela de resultados (§9) preenchida com dados reais.
- [ ] Achados (§11) documentados com evidência.
- [ ] Reteste executado para achados críticos.

Então D13 passa para **"validado neste piloto"** — no recorte e versão testados, com limitações declaradas.
