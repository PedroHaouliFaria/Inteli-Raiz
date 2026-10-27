# Como os dados do case chegam ao Watson

> **Leia antes:** [como os dados já foram usados](como-os-dados-ja-foram-usados.md). O time já fez a EDA e treinou um modelo na branch `develop`, e este caminho reaproveita esse trabalho.
>
> A pasta `data/` do repositório tem três arquivos do case Sicredi. Só dois vão para o git: o dicionário (`dicionario_dados_case_prevencao_sicredi.xlsx`) e as orientações (`.txt`). O arquivo principal, `case_transacoes_cartoes_sintetico_900k.csv` (o case descreve 900 mil linhas; o arquivo que o time tem traz 160 mil linhas × 297 colunas), está no `.gitignore` por ser grande, então cada pessoa do time guarda o seu em `data/`, no próprio computador.

## O caminho em 6 passos

```
data/case_...900k.csv
   │ 1. carga (só as colunas do modelo)
   ▼
tabelas de origem: member, account, card, merchant, device, card_transaction
   │ 2. recorte para a demo
   │ 3. score (modelo treinado pelo time de dados)
   ▼
risk_assessment + risk_factor
   │ 4. simulação: as transações "chegam" em ordem de horário
   ▼
alert → fraud_case → (risco médio) purchase_notice pelo agente / (alto) fila da analista
   │ 5. API FastAPI (/cases, /cases/{n}, /cases/{n}/notices...)
   ▼
6. frontend: fila, caso, quadro e app do associado
```

### 1. Carga (`watson/backend/app/simulation/`)
Um script de carga lê o CSV em blocos com pandas (o arquivo não cabe inteiro na memória com folga) e faz três coisas:
- **Separa as entidades.** As linhas repetem associado, cartão, loja e dispositivo, então o script deduplica por `customer_id`, `card_id`, `acceptor_id` e `device_id` e grava cada um na tabela dele. Cada linha vira uma `card_transaction`.
- **Usa só as cerca de 60 colunas mapeadas** em [modelo-de-dados.md](modelo-de-dados.md) e descarta as outras 230. Documentos pessoais e o número completo do cartão nunca entram no banco.
- **Deixa de fora as colunas de vazamento** (`decision`, `transaction_status`, `dispute_*`, `fdz_*`, `oob_*`, `alert_id`), seguindo a triagem da EDA.
- **Trata os nulos.** O case tem nulos de propósito. O script guarda o nulo como nulo e não inventa valor. A imputação é trabalho do modelo.

### 2. Recorte para a demo
As 160 mil linhas cabem no PostgreSQL. Para a demo, o recorte parte das **32 mil transações de `data/processed/teste_proporcao_real.csv`**, com 29 fraudes que o modelo nunca viu no treino. As colunas completas vêm do CSV bruto, buscadas pelo id:
- todas as transações do teste;
- o histórico completo dos cartões dessas fraudes, porque a linha do tempo e os sinais de velocidade precisam das compras anteriores;
- uma amostra de outros cartões, só com compras legítimas, para a fila parecer real.

A amostra é por **cartão**, não por linha. Sortear linhas soltas quebra as rajadas.

### 3. Score
- O modelo **já existe**: é o Random Forest do `notebooks/03_modelo.ipynb` (branch `develop`), que deve ser publicado no watsonx.ai. `app/risk/` não treina nada. Ele monta as 28 features na mesma ordem de `agente/tools/pontuar_transacao.py`, chama o modelo publicado e registra a versão em `model_version`.
- Se o modelo publicado não responder, entra o plano B do time, que é um score por regras. A coluna `fraud_score` do case também funciona como score provisório para a tela, mas ela já "sabe a resposta" e não pode ser apresentada como resultado.
- O score vai para `risk_assessment`, e as 28 features ficam em `signals`. Os fatores com peso vão para `risk_factor`, a partir da importância das features ou de SHAP. É isso que aparece em "Por que é suspeito".

### 4. Simulação de chegada
Em vez de abrir todos os casos de uma vez, `app/simulation/` "toca" as transações do recorte em ordem de horário, como se estivessem chegando agora. Se o score passa do limiar, o sistema cria um `alert` e cria ou agrupa um `fraud_case`. No risco médio, o agente envia o `purchase_notice`. No risco alto, o caso vai para a fila.

O app do associado também pode ser simulado: o `feedback_label` decide a resposta, com "Não reconheço" se for fraude e "Fui eu" se for legítima. Esse rótulo **nunca aparece na tela** da analista.

### 5 e 6. API e telas
Hoje o frontend lê dados fixos, de `src/mocks/cases.js`. Quando o banco estiver carregado, ele passa a chamar a API:

| Tela | Rota | Tabelas |
|---|---|---|
| Fila | `GET /cases` | `fraud_case` (ordenada por `priority`) |
| Caso | `GET /cases/{n}` | `fraud_case`, `card_transaction`, `risk_factor`, `agent_recommendation` |
| Linha do tempo | `GET /cards/{id}/transactions` | `card_transaction` do mesmo cartão |
| Quadro | `GET /cases?status=...` | `fraud_case.status` |
| Decisão | `POST /cases/{n}/decision` | `decision`, `executed_action`, `case_event` |
| App do associado | `GET/POST /cases/{n}/notices` | `purchase_notice` |

## O que falta construir
1. Tabelas SQLAlchemy em `app/db/tables/` e a primeira migração (o esqueleto existe e está vazio).
2. Script de carga e de recorte em `app/simulation/`.
3. Score provisório com `fraud_score` e, depois, o modelo do time de dados.
4. Rotas `/cases` e afins, e troca dos mocks do frontend pela API.
