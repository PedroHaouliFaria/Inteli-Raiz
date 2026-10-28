# D03 — Cenário Atual: do alerta à resolução da dúvida

**ID:** D03  
**Versão:** 0.1 · 28/10/2026  
**Responsável:** Pessoa 2  
**Revisor principal:** Pessoa 4  
**Estado:** rascunho para revisão — cenário hipotético; canais, tempos e etapas não confirmados com associados ou com a Sicredi  
**Origem:** cenário as-is do Leonardo (`origin/watson` `212655c`, `docs/design/00-descoberta/cenario-as-is.md`); revisado e expandido conforme plano vigente (`origin/develop` `8942cc5`)

---

## 1. Delimitação do episódio

| Elemento | Descrição |
|---|---|
| **Início** | O associado percebe um sinal de que algo diferente ocorreu com o cartão — uma notificação, uma tentativa de compra recusada ou uma fatura com valor inesperado |
| **Ator principal** | Associado (protopersona Valdir, FON-04) |
| **Ator secundário** | Central de atendimento / prevenção a fraudes — aparece quando o associado busca ajuda ou o bloqueio exige contato |
| **Objetivo do associado** | Entender o que aconteceu com o cartão e resolver — autorizar, contestar ou obter ajuda — sem precisar ir à agência |
| **Possíveis desfechos** | Compra reconhecida e autorizada; compra contestada; dúvida encaminhada para revisão; caso abandonado sem resolução |
| **Status do cenário** | Hipótese investigável, construída a partir do cenário as-is do Leonardo (FON-06) e do briefing do desafio Sicredi (FON-11); não representa descrição confirmada do processo interno da instituição |

---

## 2. Jornada principal — cenário hipotético

> **Atenção:** as etapas abaixo são hipóteses de pesquisa. Cada coluna de "fonte/hipótese" indica o que sustenta a afirmação. Tempos não foram medidos. Canais e atores são inferidos, não confirmados.

| # | Etapa | Objetivo / ação do associado | Informação / canal | Pensamento / sentimento (hipótese) | Fricção | Consequência hipotética | Fonte / hipótese | Pergunta aberta |
|---|---|---|---|---|---|---|---|---|
| 1 | **Sinal percebido** | Identificar que algo diferente aconteceu | Notificação no app, SMS, mensagem de rede social (imitação de banco), recusa no balcão ou fatura inesperada | "O que é isso?" / Insegurança — pode ser golpe (HIP-04) | Não saber se o canal é confiável; múltiplos canais com aparência similar | Ignora (se desconfiar de golpe) ou abre o app | FON-04; HIP-04; HIP-06 | Qual canal o associado percebe primeiro? Com qual frequência o primeiro sinal é a recusa no balcão? |
| 2 | **Tentativa de entender a compra** | Descobrir o que foi comprado, onde e quando | Informação no app ou SMS: valor, estabelecimento, data — potencialmente incompleta ou com nome de empresa desconhecido | "Não reconheço esse nome" / Hesitação; dúvida se foi legítima ou suspeita (HIP-03) | Nome do estabelecimento pode não corresponder ao nome percebido pelo associado; falta de contexto adicional | Tenta resolver sozinho ou pede ajuda a familiar | FON-04; FON-05; HIP-03 | O associado sabe onde buscar mais informação sobre a compra (app, fatura, extrato)? |
| 3 | **Tentativa de contato com a cooperativa** | Confirmar se a mensagem é legítima / entender o que fazer | Ligação para a central; URA; tempo de espera desconhecido | "Ninguém atende" / Frustração; sensação de abandono (HIP-08) | Ligação de número desconhecido é ignorada; URA burocrática; repetição de informação | Desiste do contato; aguarda; ou consegue falar e é orientado | FON-06 (etapas 2 e 4); FON-04; HIP-04; HIP-08 | Existe um canal atual de confirmação que o associado usa antes de ligar? |
| 4 | **Descoberta do bloqueio** | Compreender o que aconteceu com o cartão | Recusa na maquininha / loja; notificação de bloqueio no app (se existir); ligação da central | "Por que bloquearam meu cartão?" / Vergonha; surpresa (HIP-01; HIP-08) | Associado não sabia que o bloqueio ocorreria; falta de explicação prévia sobre o alcance da ação | Passa vergonha; vai à agência; liga para a central | FON-06 (etapa 3); FON-04; HIP-01; HIP-08 | O bloqueio automático do cartão inteiro é o comportamento atual em todos os casos suspeitos ou apenas em alguns? (Pergunta para especialista do domínio) |
| 5 | **Resolução ou abandono** | Contestar ou regularizar a compra; receber novo cartão se necessário | Central de atendimento; agência física; prazo desconhecido | "Não sei se a compra foi estornada" / Incerteza sobre o desfecho (HIP-09) | Sem retorno claro do status; prazo incerto para regularização; necessidade de deslocamento | Caso resolvido (com esforço); caso não resolvido por falta de retorno; associado satisfeito com outra compra legítima recusada | FON-06 (etapas 4 e 5); HIP-09 | Qual é o tempo médio de resolução hoje? O associado recebe confirmação de que a compra foi tratada? |

---

## 3. Diagrama simplificado

> Este diagrama é uma representação das hipóteses acima. O conteúdo é idêntico à tabela; o estado do cenário é hipotético.

```
Associado percebe sinal
        │
        ├─ Desconfia do canal ──────────────────────────┐
        │                                               │
        ▼                                               │
Tenta entender a compra no app/fatura             Ignora / não age
        │
        ├─ Reconhece ──────────────────────────────────►  Nenhuma ação
        │
        ├─ Não reconhece → tenta ligar para a central
        │       │
        │       ├─ Consegue contato → orienta sobre próximos passos
        │       │
        │       └─ Não consegue contato → espera
        │
        └─ Descobre o bloqueio no balcão (surpresa)
                │
                └─ Liga / vai à agência → resolução com esforço
                        │
                        └─ Desfecho incerto (HIP-09)
```

---

## 4. Ponto de ruptura prioritário

**Etapa 2/3 — O associado não tem canal direto confiável para entender e resolver uma compra ambígua.**

Justificativa (hipotética): a situação mais frequente não é necessariamente o bloqueio no balcão, mas a dificuldade de entender o que aconteceu, reconhecer a compra e decidir o que fazer — num canal que o associado não consegue distinguir de uma tentativa de golpe. Essa fricção pode ocorrer independentemente de a compra ser bloqueada: ela existe sempre que o canal de comunicação é incerto (HIP-04) ou a informação da compra é insuficiente para reconhecimento (HIP-03). FON-06 registra o bloqueio no balcão como etapa 3 do cenário as-is do Leonardo; ele é aqui tratado como **uma das possíveis consequências** da ruptura principal, não a ruptura em si.

**Bloqueio no balcão como ramificação hipotética:** pode ocorrer quando o sistema aciona um bloqueio antes de o associado ser contactado. É uma consequência grave quando acontece (FON-04: frustração do Valdir), mas confirmar se é o desfecho padrão ou uma exceção depende de pesquisa ou informação do domínio (ver Lacuna 1 abaixo).

**O que poderia mudar essa prioridade:** descobrir, em pesquisa, que o associado raramente tenta reconhecer a compra por conta própria e age apenas quando já impactado. Nesse caso, o evento de impacto (recusa no balcão ou cobrança inesperada) voltaria a ser o ponto de entrada mais relevante para o design.

---

## 5. Lacunas — o que só entrevista ou fonte de domínio pode confirmar

| Lacuna | Por que importa | Quem pode responder |
|---|---|---|
| O bloqueio automático do cartão inteiro é o processo atual padrão da Sicredi? | Define se a etapa 4 é a ruptura mais frequente ou uma exceção | Especialista do domínio / mentor do programa |
| Qual canal o associado recebe primeiro — app, SMS ou ligação? | Muda onde a intervenção precisa acontecer | Entrevista com 2–3 associados |
| O associado tem acesso ao app no momento do alerta (campo, sinal fraco)? | Define restrições de formato e conectividade | Entrevista de descoberta; pergunta sobre contexto de uso |
| Qual a frequência de compras legítimas com nome ambíguo que geram dúvida? | Define quão central é a hipótese HIP-03 | Entrevista + análise de domínio |
| O associado sabe ligar para a central diretamente ou usa o número que aparece na notificação? | Risco de golpe por canal falso (HIP-04) | Entrevista de descoberta |

---

## 6. Relação com o cenário futuro proposto

O cenário atual (hipotético) apresenta como principal problema a ausência de um canal de confirmação direta que o associado reconheça como legítimo, com informação suficiente para decidir e retorno claro sobre o desfecho. O cenário futuro proposto (documentado em D06) endereça especificamente esse ponto: a confirmação acontece no app autenticado, com três opções explícitas, ajuda contextual e status pós-resposta.

**O que o cenário futuro não muda (limites do MVP):** o bloqueio automático, o novo cartão e o estorno real não são escopo do produto. O cenário futuro não promete ausência de fraude ou de bloqueio; propõe um caminho de resposta explícita antes de qualquer ação automática, dentro de uma política experimental.

O atual e o futuro são descritos com base na mesma situação-problema (compra sinalizada cujo contexto não é imediatamente reconhecido) para permitir comparação. A comparação está em D06.
