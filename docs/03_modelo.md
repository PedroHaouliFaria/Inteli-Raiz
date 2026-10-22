# Modelo: Prevenção a Fraudes em Cartões (Sicredi)

> **Trilha 4, IBM AI Experiential Learning Lab 2026:** *Como podemos utilizar IA Agêntica para prever e intervir em possíveis fraudes relacionadas a compras com cartões, aumentando a segurança dos associados e reduzindo perdas para o Sicredi?*

## Sumário

1. [Introdução](#1-introdução)
2. [Linha de raciocínio](#2-linha-de-raciocínio)
3. [O modelo](#3-o-modelo)
4. [Avaliação e comparação com o baseline](#4-avaliação-e-comparação-com-o-baseline)
5. [Distribuição dos scores: o modelo está decidido?](#5-distribuição-dos-scores-o-modelo-está-decidido)
6. [Limiar de decisão](#6-limiar-de-decisão)
7. [Análise crítica](#7-análise-crítica)

---

## 1. Introdução

Este documento cobre o treinamento e a avaliação do classificador de fraudes. As bases usadas aqui foram preparadas no documento anterior — [02 — Base Balanceada](02_base_balanceada.md).

**O ponto de partida.**

| | |
|---|---|
| Treino | `treino_balanceado.csv` · 234 linhas · 50% fraudes |
| Teste | `teste_proporcao_real.csv` · 32.000 linhas · 0,09% fraudes |
| Features | 31 (24 originais + 7 criadas) |

**O notebook deste documento.**

| Notebook | Conteúdo |
|---|---|
| [`03_modelo.ipynb`](../notebooks/03_modelo.ipynb) | Pré-processamento, treinamento, avaliação e análise crítica |

---

## 2. Linha de raciocínio

```mermaid
flowchart LR
    A[Treino 1:1<br/>234 linhas] --> B[Pipeline sklearn<br/>imputa + codifica]
    B --> C[Random Forest<br/>300 árvores]
    C --> D[Avalia no teste<br/>PR-AUC · F2]
    D --> E[Compara com<br/>fraud_score]
    E --> F[Análise crítica<br/>importância das features]
```

---

## 3. O modelo

**Por que Random Forest?** Lida bem com dados mistos (numéricos + categóricos), nulos imputados, escalas diferentes e desbalanceamento residual. A importância das features é nativa e direta — o agente pode usá-la para justificar um alerta em linguagem natural.

### Pipeline de pré-processamento

Antes de entrar no modelo, cada grupo de colunas passa por uma transformação:

| Grupo | Colunas | Transformação | Motivo |
|---|---|---|---|
| **Numéricas** | 16 | Imputa com a mediana | Robusto a outliers de valor e renda |
| **Categóricas** | 9 | Converte para `str` → imputa `"desconhecido"` → OrdinalEncoder | Colunas com nulos lidos do CSV ficam com tipos mistos (`float` + `str`); a conversão resolve antes do encoder |
| **Binárias** | 3 | Imputa com `0` | Ausência do sinal = 0 é semanticamente correto |

### Hiperparâmetros

| Parâmetro | Valor | Decisão |
|---|---|---|
| `n_estimators` | 300 | Convergência estável |
| `max_depth` | 10 | Evita overfitting no treino pequeno (234 linhas) |
| `min_samples_leaf` | 2 | Idem |
| `class_weight` | `balanced` | Reforça a minoria mesmo com treino já 1:1 |
| `random_state` | 42 | Reprodutibilidade |

---

## 4. Avaliação e comparação com o baseline

> **Por que PR-AUC e não ROC-AUC?** Com 0,09% de fraudes no teste, um modelo que acerta 99,9% das legítimas pode ter ROC-AUC alto sem detectar nada. PR-AUC (Precision-Recall) penaliza essa falsa segurança.

![Curva Precision-Recall](assets/pr_curve.png)

| Modelo | PR-AUC | ROC-AUC |
|---|---|---|
| **Nosso modelo** | **1,000** | **1,000** |
| `fraud_score` (baseline externo) | 1,000 | 1,000 |
| `visa_fraud_score` | 0,956 | 0,968 |
| `mc_fraud_score` | 0,882 | 0,903 |

**Matriz de confusão** (com o limiar F2 ótimo):

| | Previsto: legítima | Previsto: fraude |
|---|---|---|
| **Real: legítima** | 31.971 (VN) | 0 (FP) |
| **Real: fraude** | 0 (FN) | 29 (VP) |

29 de 29 fraudes detectadas, zero falsos alarmes.

---

## 5. Distribuição dos scores: o modelo está decidido?

Um bom classificador não é só aquele que acerta — é aquele que **sabe quando está certo**. Se as probabilidades se concentrarem perto de 0 e de 1, o modelo está decidido: separa as classes com confiança. Se ficarem empilhadas no meio (~0,5), ele está em dúvida.

![Distribuição dos scores por classe](assets/distribuicao_scores.png)

O painel da esquerda mostra os histogramas em escala logarítmica (necessário porque há 31.971 legítimas e apenas 29 fraudes). O painel da direita é um zoom nas legítimas com score ≤ 0,10 para mostrar onde elas se concentram.

| Medida | Legítimas | Fraudes |
|---|---|---|
| Score médio | 0,022 | 0,967 |
| Score mínimo | 0,000 | **0,817** |
| Score máximo | 0,573 | 1,000 |

**O modelo está completamente decidido:** todas as legítimas ficam abaixo de 0,58 e todas as fraudes acima de 0,82 — sem nenhuma sobreposição. Isso confirma o PR-AUC = 1,000 e, ao mesmo tempo, reforça a suspeita de que as features de velocidade pré-calculadas estão "entregando" a resposta diretamente (ver seção 6).

---

## 6. Limiar de decisão

O modelo retorna uma probabilidade entre 0 e 1. O **limiar** define a partir de qual valor a transação é bloqueada. Escolher esse ponto é uma decisão de negócio:

- **Limiar baixo** → mais alertas → mais fraudes capturadas → mais falsos alarmes (associado incomodado)
- **Limiar alto** → menos alertas → menos falsos alarmes → mais fraudes passam

Usamos o **F2-score** (recall pesa 2× mais que precisão) como critério, porque o custo de deixar uma fraude passar é maior do que o de gerar um falso alarme.

| Métrica | Valor |
|---|---|
| Limiar ótimo (F2) | 0,817 |
| Precisão nesse limiar | 1,000 |
| Recall nesse limiar | 1,000 |

> O Sicredi pode ajustar esse limiar conforme a política de risco: aceitar mais falsos alarmes para garantir mais recall, ou o contrário.

---

## 7. Análise crítica

### PR-AUC = 1,0 é um sinal de alerta

Em produção real, fraudes e compras legítimas sempre se sobrepõem. Uma separação perfeita indica que o modelo encontrou um atalho — e encontrou.

![Importância das features](assets/feature_importance.png)

As **4 features de velocidade pré-calculadas** dominam o modelo:

| Feature | Importância |
|---|---|
| `cp_card_term_vel_1h` | 25,4% |
| `digitalwallettoken_count_3m` | 20,0% |
| `cardid_count_1m` | 14,1% |
| `cp_card_prev_term_dist_1h` | 9,3% |
| **Total velocidade** | **68,8%** |

Essas colunas vieram prontas no dataset. Na base sintética, o gerador provavelmente as construiu com acesso à label ou as exagerou para facilitar o exercício. O efeito é que elas **denunciam a fraude diretamente** — e qualquer modelo que as use vai parecer perfeito, inclusive o baseline `fraud_score` (PR-AUC = 1,000).

### O que as features da equipe valem?

As 7 features criadas (`madrugada`, `cnp_credito`, `valor_vs_media_cartao`, `valor_vs_limite`, `primeira_compra_cartao`, `hora`, `dia_semana`) respondem por apenas **~11% da importância** — não porque sejam fracas, mas porque as features de velocidade dominam antes delas ter chance. Para medir o poder real dessas features, o próximo passo é rodar o modelo sem as 4 pré-calculadas.