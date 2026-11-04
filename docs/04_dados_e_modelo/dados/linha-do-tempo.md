# Dá para traçar a linha do tempo de um cartão com os dados do case?

> Fontes: dicionário do case; saídas do `notebooks/01_eda.ipynb` (branch `develop`), rodado sobre o CSV bruto de 160 mil linhas; e contagem própria em `data/processed/teste_proporcao_real.csv`. Não li o CSV bruto diretamente, porque ele só existe no PC do time.

## Resposta curta
**Sim, mas a linha do tempo fica curta e espaçada.** O CSV bruto tem o que é preciso para montar a linha do tempo: horário, cartão, associado, local e dispositivo. O problema é que a maioria dos cartões tem só 1 ou 2 compras no ano, e as **rajadas não aparecem como linhas**. Elas só existem como contadores prontos.

## As colunas que montam a linha do tempo
| Para | Coluna (CSV bruto) | Observação |
|---|---|---|
| Horário | `event_occurred_at` | Igual a `local_datetime` (a EDA confirmou). Período de 01/01/2025 a 31/12/2025 |
| Cartão | `card_id`, `card_last4` | `card_last4` serve para "final 4821" |
| Associado | `customer_id`, `customer_name` | |
| Valor e loja | `amount`, `acceptor_name`, `mcc` | `amount` tem 599 nulos |
| Canal | `modalidade_transacao`, `card_presence_flag` | presente ou não presente |
| Local | `terminal_city`, `terminal_latitude/longitude`, `acceptor_city`, `acceptor_latitude/longitude`, `device_ip_latitude/longitude` | todas as coordenadas são válidas, segundo a EDA |
| Dispositivo | `device_id`, `device_fingerprint` | |
| Distância e velocidade prontas | `cp_card_prev_term_dist_1h`, `cp_card_term_vel_1h`, `cardid_count_1m` | já vêm calculadas, por transação |

`data/processed/` **não serve** para isso: não tem horário (só `hora` e `dia_semana`), nem cidade, nem loja, e o teste é uma amostra sorteada de 20%. A linha do tempo precisa do CSV bruto.

## Quantas transações por cartão
| | Base bruta (EDA, 160 mil) | Teste (32 mil) |
|---|---|---|
| Cartões distintos | 56.772 | 22.190 |
| Transações por cartão (mediana) | **2** | 1 |
| Máximo num cartão | 448 | 85 |
| Associados distintos | 33.037 | 15.033 |
| Transações por associado (mediana) | 2 | 1 |

Sobre as fraudes: 145 cartões, **uma fraude por cartão**, e **70% delas na 1ª compra do cartão** dentro da base.

## O ponto que muda a tela: as rajadas não estão nas linhas
A EDA mediu o tempo desde a compra anterior do mesmo cartão:
- mediana na fraude: cerca de **21 mil minutos (14 dias)**; na legítima, cerca de 38 dias;
- compras com outra compra do mesmo cartão a menos de 60 min: **0%** na fraude.

Ou seja, o "5 tentativas em 7 min" do wireframe **não existe como 5 linhas** no CSV. A rajada só aparece nos contadores prontos: `cp_card_term_vel_1h` tem mediana de 47 na fraude contra 2 na legítima, e `cardid_count_1m` tem 17 contra 1. Esses contadores são exatamente as features que deixam o modelo perfeito.

## Como sugiro resolver na tela do caso
1. **Linha do tempo real:** as compras do cartão vindas do CSV bruto, ordenadas por `event_occurred_at`. Na maioria dos casos ela mostra de 1 a 3 compras espaçadas, e isso conta uma história: "primeira compra deste cartão" e "fora da cidade de costume".
2. **Rajada como indicador, não como linhas:** um destaque do tipo "47 tentativas deste cartão no terminal na última hora" lido de `cp_card_term_vel_1h`, com a origem indicada.
3. **Se a demo precisar das linhas da rajada:** a simulação gera tentativas sintéticas recusadas ou retidas, coerentes com o contador, e marca cada uma como gerada (`card_transaction.is_simulated`). Assim a tela fica igual ao wireframe sem fingir que veio do case.

**Decisão (Leo, 27/10/2026):** aplicar as três opções. A regra ficou no [modelo de dados](modelo-de-dados.md), na seção "Rajada: indicador e tentativas simuladas".
