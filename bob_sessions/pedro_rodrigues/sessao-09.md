# Sessão 9 no Bob — Pedro Rodrigues

Tarefas rodadas no Bob IDE (modo agent), branches `entregas/p3-estrutura-arquitetura` e `docs/pessoa4-prototipo-validacao`, criadas a partir de `develop`.

| Tarefa | Início | Custo aprox. | Chamadas de ferramenta |
|---|---|---|---|
| `feat(p3)`: D09 — estrutura da solução e critérios de sucesso | 28/10 11:36 UTC | ~9.20 | 74 |
| `docs`: esclarece revisão, métricas e sinais (ajuste pós-revisão) | 29/10 10:42 UTC | ~1.40 | 15 |
| `docs(pessoa4)`: D12 protótipo, D11 fluxo MVP, D13 validação | 29/10 16:25 UTC | ~14.60 | 102 |
| **Total** | | **~25.20** | |

## O que a revisão humana verificou

- Leitura dos slides S4 pp.9–12 e 29 antes de escrever D09/D10; mermaid de componentes e de sequência revisados manualmente para garantir que o agente não chama `POST /confirmations/{id}/response` diretamente.
- D09: 12 requisitos (R01–R12) com necessidade, teste e evidência linkados ao plano §9; critérios separados por dimensão (modelo, sistema, agente, experiência, operação).
- D10: ficha do agente com saber/decidir/fazer explicitados; catálogo das 4 ferramentas com entrada, saída e erro; máquina de estados documentada com 7 estados.
- Ajuste `b5b82b0`: revisão cruzada identificou que D10 misturava "avaliação de risco" (domínio do modelo) com "sinalização" (domínio da política). Separados em duas caixas no diagrama e na descrição; o sinal não é o score bruto.
- D12/D13: leitura de D06 (persona Valdir) e D09 antes de descrever o protótipo; percurso cobre os 6 cenários do produto (autorizar, não reconhecer, dúvida, atendimento, expirar, falha de contexto).
- D11: casos de teste P4-T01–T12 baseados nos T-001–T-012 do plano §9; evidências P4-EVI-01 a P4-EVI-03 coletadas na execução do backend com curl.
- D13: protocolo de validação com perfis prioritários, tarefas e chave de avaliação; pendências PEN-01–PEN-10 registradas para reteste após as correções.

## Resumo final de cada tarefa

### `feat(p3)`: D09 — estrutura da solução + D10 — arquitetura técnica

`f732159`

```text
entregas/09_estrutura_solucao.md  (novo)

  Problema, usuário e jornada prioritária.
  Capacidades do agente: 3 × saber, 3 × decidir, 4 × fazer.
  Matriz saber/decidir/fazer com ator e ferramenta.
  12 requisitos R01–R12: necessidade, teste e evidência.
  Critérios de sucesso por dimensão:
    modelo (PR-AUC, limiar, baseline), sistema (fluxo ponta a ponta),
    agente (ferramentas corretas, sem autorização direta),
    experiência (conclusão independente, compreensão do resultado),
    operação (persistência, versão, falha tratada).
  Dados disponíveis, limitações e dependências de acesso.

entregas/10_arquitetura.md  (novo)

  Diagrama mermaid de componentes (7 nós, 10 arestas).
  Diagrama de sequência do fluxo principal (12 passos).
  Ficha do agente: objetivo, conhecimento permitido,
    instruções fixas, ferramentas, critérios de escolha,
    limites de autonomia.
  Catálogo de ferramentas: consultar_compra, consultar_status,
    avaliar_transacao, solicitar_revisao — cada uma com
    finalidade, entrada, saída, autorização e erro esperado.
  Política determinística documentada separada do agente.
  Estado inicial: "planejado" com nota de evidência pendente.
```

### `docs`: esclarece revisão, métricas e sinais

`b5b82b0`

```text
entregas/09_estrutura_solucao.md
  R07 reescrito: sinal comunicado ao agente é "há sinais que
  levantam dúvida", não o score numérico.
  Critério de modelo: "score calculado on-the-fly sem acesso
  ao histórico futuro" adicionado como condição de validade.

entregas/10_arquitetura.md
  Diagrama de componentes: caixa "Modelo de risco" separada de
  "Política de sinalização"; seta rotulada como "score (interno)".
  Ficha do agente: "conhecimento permitido" atualizado —
  score bruto não entra no contexto do LLM.
```

### `docs(pessoa4)`: D12 protótipo, D11 fluxo MVP, D13 validação

`466a4fc`

```text
docs/entregas/pessoa4/README.md  (novo)
  Índice do pacote, autoria, estado e pendências PEN-01–PEN-10.

docs/entregas/pessoa4/D12_prototipo_experiencia.md  (novo)
  Percurso testável: 6 telas/estados (lista, detalhe, chat,
  confirmação recebida, recusa, revisão).
  Decisões de interface:
    - Três botões com rótulos em linguagem natural, não técnica.
    - Texto de resultado identifica compra, resposta e próximo passo.
    - "Quero falar com alguém" não encerra a confirmação.
    - Status sem depender de cor (ícone + texto).
  Adaptações necessárias do Watson: SessionGate, PurchaseDetail,
  PurchaseChat com estado de carregamento.
  Pendências PEN-01–PEN-04 (Leonardo/Lucas).

docs/entregas/pessoa4/D11_fluxo_mvp.md  (novo)
  Pré-condições e versão (commit base: 202655c).
  12 casos P4-T01–T12 derivados de T-001–T-012 do plano.
  Instrução de reprodução com curl + SessionGate.
  Evidências P4-EVI-01 (autorização), P4-EVI-02 (recusa + revisão),
  P4-EVI-03 (expiração): saídas reais do backend, horários e
  estado persistido confirmado.
  Pendências PEN-05–PEN-07 (frontend, LLM real, reteste independente).

docs/entregas/pessoa4/D13_validacao_melhorias.md  (novo)
  Protocolo de validação: 2 perfis, 3 tarefas, ordem alternada.
  Chave de avaliação: conclusão independente, compreensão do
  resultado, ausência de decisão equivocada.
  Modelo de registro (formulário vazio).
  Pendências PEN-08–PEN-10 (piloto, reteste, atualização de D01/D08).

docs/README.md  — seção Pessoa 4 adicionada com links.
```
