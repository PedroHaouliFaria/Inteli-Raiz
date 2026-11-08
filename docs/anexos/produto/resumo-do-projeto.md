# D07 — Ideia preliminar: assistente de confirmação de compras

**ID:** D07 · **Versão:** 0.2 · **Data:** 04/11/2026
**Responsável:** Produto · **Estado:** rascunho revisado documentalmente; revisão cruzada pendente
**Fontes:** registro de evidências, plano de implementação e direcional.

**Revisor:** Integração e validação · **Estado:** rascunho

---

## Sumário

- [1. Ficha da ideia](#1-ficha-da-ideia)
- [2. Versão de ~30 segundos (pitch falado)](#2-versão-de-30-segundos-pitch-falado)
- [3. Mini-roteiro de teste da explicação](#3-mini-roteiro-de-teste-da-explicação)
- [4. Coerência com D05 e D11/D12](#4-coerência-com-d05-e-d11d12)

---

## 1. Ficha da ideia

| Campo | Conteúdo |
|---|---|
| **Nome descritivo** | Assistente de confirmação de compras |
| **Problema** | Hipótese: o associado pode ter dificuldade para entender e responder à compra no canal disponível; processo atual da instituição não confirmado |
| **Usuário** | Associado do Sicredi com uma compra sinalizada aguardando confirmação |
| **Solução em uma frase** | Um assistente no app que mostra a compra, esclarece dúvidas com o contexto disponível e registra a resposta explícita do associado — com revisão humana das exceções |
| **Três capacidades essenciais** | (1) Apresentar a compra com o contexto disponível e o motivo do alerta; (2) responder dúvidas contextuais sobre a compra sem inventar informação; (3) registrar a resposta explícita do associado (autorizar / recusar / dúvida) e mostrar o desfecho |
| **Resultado esperado** | O associado conclui a confirmação sem ligar para ninguém, entendendo o que autorizou e o que acontece a seguir |
| **Estágio** | API e interface integradas no código; 207 testes de backend aprovados nesta revisão; ensaio UI independente e LLM real pendentes |
| **Maior hipótese aberta** | HIP-P1-05: o agente faz diferença real nos casos de nome ambíguo. Se a confirmação com texto fixo resolver bem, a necessidade do agente precisa ser demonstrada em outro cenário |

---

## 2. Versão de ~30 segundos (pitch falado)

> **Nota:** os "30 segundos" são o tempo do pitch oral, não uma meta de tempo de uso do produto. As metas de tempo de uso (Hills do Leonardo) são aspirações de design, não resultados medidos.

---

"Quando o sistema identifica uma compra suspeita, o associado recebe uma notificação no app. A tela mostra os detalhes da compra, o motivo do alerta e três opções: autorizar, não reconhecer ou informar dúvida. Se tiver uma pergunta — por exemplo, 'esse nome na fatura é o restaurante que fui?' — o assistente responde com o contexto disponível. Se não souber, ele diz que não sabe e oferece revisão humana. A resposta é sempre do associado. Tudo é simulado — nenhuma transação financeira real é executada."

---

## 3. Mini-roteiro de teste da explicação

> **Objetivo:** verificar se alguém de fora do grupo entende a ideia após ouvir o pitch de 30 s acima.

| Pergunta | O que quer verificar |
|---|---|
| "Quem usa esse produto?" | O associado está claro (não o analista, não o banco) |
| "O que o produto faz?" | As três capacidades estão presentes |
| "O que acontece quando o associado não reconhece a compra?" | Distinção entre recusa e bloqueio do cartão |
| "O agente pode autorizar a compra por você?" | Limite do agente está claro |
| "Alguma transação financeira real acontece?" | Simulação está clara |

<p align="justify">&ensp;&ensp; <strong>Estado:</strong> pendente — não executado. Executar antes de fechar D07.</p>

---

## 4. Coerência com D05 e D11/D12

<p align="justify">&ensp;&ensp; D07 descreve o mesmo assistente de D05, em linguagem acessível. As três capacidades de D07 mapeiam para os momentos 1–3 de D05. D11 (Integração e validação) documenta o fluxo técnico que implementa essas capacidades; D12 (Integração e validação) documenta a interface.</p>

<p align="justify">&ensp;&ensp; Fluxo integrado atual: SessionGate → AssociateApp → PurchaseDetail, com AUTHORIZE/DENY/UNSURE e API. A inspeção antiga de MemberPhone não descreve esse caminho; o legado permanece como referência visual, fora do aceite integrado.</p>

---
