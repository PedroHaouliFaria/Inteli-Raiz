# Como os dados do case já foram usados no projeto

> Levantamento feito em 27/10/2026 nas branches do repositório `inteli-raiz`. O trabalho de dados está na branch **`develop`** (PRs #1, #2, #3 e #5, de 20 a 26/10, feitos por Isadora, Pedro R. e Pedro H.). O teste de integração do modelo com o agente está em **`agente/teste-integracao`** (Lucas). A branch `watson` não tem nada disso.

## Resumo
Sim, parte dos dados já foi usada para treinar um modelo. O time fez a EDA, montou as bases de treino e teste e treinou um Random Forest. O plano é publicar esse modelo no watsonx.ai e chamá-lo pelo agente no watsonx Orchestrate.

## 1. O arquivo que o time tem é menor do que o case descreve
| | Orientações do case | Arquivo que o time usou |
|---|---|---|
| Linhas | 900.000 | **160.000** (jan a dez/2025) |
| Fraudes | 900 (0,10%) | **146 (0,09%)** |
| Colunas | 297 | 297 |

O nome do arquivo é o mesmo, `case_transacoes_cartoes_sintetico_900k.csv` (cerca de 290 MB, fora do git). A EDA registra a diferença e diz que é só rodar de novo quando a base completa chegar.

## 2. O que foi feito, passo a passo
| Etapa | Onde | Resultado |
|---|---|---|
| **EDA** | `notebooks/01_eda.ipynb`, `docs/01_analise_exploratoria.md` | Qualidade, sinais da fraude, vazamentos. Triagem de 297 para **31 colunas** (`outputs/triagem_colunas.csv`) |
| **Base balanceada** | `notebooks/02_base_balanceada.ipynb`, `docs/02_base_balanceada.md` | Criou 7 features e separou um teste com a proporção real, mais um treino 1:1 |
| **Modelo** | `notebooks/03_modelo.ipynb`, `docs/03_modelo.md` | Random Forest com 300 árvores, 28 features, avaliado por PR-AUC e F2 |
| **Integração** | `agente/tools/pontuar_transacao.py`, `docs/specs/teste_integracao_orchestrate_wml.md` | Ferramenta do Orchestrate que manda as 28 features ao modelo publicado no watsonx.ai Runtime e recebe o score. Se não funcionar, o plano B é um score por regras |

**Arquivos gerados e versionados** (`data/processed/`):
- `treino_balanceado.csv`: 234 linhas (117 fraudes e 117 legítimas);
- `teste_proporcao_real.csv`: 32.000 linhas (29 fraudes), que o modelo **não viu** no treino;
- `dicionario_base_modelo.csv`: as 35 colunas da base do modelo.

## 3. O que o time descobriu e que muda o nosso modelo de dados
1. **Vazamento.** `decision`, `transaction_status`, `device_ip_country_code = ZZ` e as colunas `dispute_*`, `fdz_*`, `oob_*` e `alert_id` só existem depois que se sabe que foi fraude. A EDA removeu 30 colunas por isso. **Correção no nosso modelo:** `card_transaction.status` não pode vir de `transaction_status`. Na carga, toda transação começa como `approved`, e quem muda o status é o Watson.
2. **Scores prontos.** `fraud_score` acerta 100%, igual ao modelo, então ele também "sabe a resposta". Usar essa coluna como score provisório na demo funciona, mas não pode ser apresentado como resultado.
3. **As features de velocidade dominam.** Com `cardid_count_1m`, `cp_card_term_vel_1h`, `cp_card_prev_term_dist_1h` e `digitalwallettoken_count_3m`, o PR-AUC é 1,000. Sem elas, cai para **0,144**. A conclusão do próprio time é que detectar a fraude nesta base é quase trivial, e o valor está no que acontece depois do alerta, que é justamente o Watson.
4. **Sinais que a analista e o associado entendem.** As 7 features criadas são `hora`, `dia_semana`, `madrugada` (100% das fraudes entre 0h e 4h), `cnp_credito` (83% das fraudes), `valor_vs_media_cartao` (fraude vale 3,9 vezes a média), `primeira_compra_cartao` (70% das fraudes) e `valor_vs_limite`. Elas viram os textos de "Por que é suspeito" (`risk_factor`).
5. **Limiar.** O limiar F2 deu 0,817, perto do 0,80 do glossário. O plano de 23/10 pede que o limiar saia da validação, e não de uma escolha para a demo ficar bonita.

## 4. Como isso entra no Watson
- **Score:** `app/risk/` não treina nada. Ele monta as 28 features na mesma ordem de `pontuar_transacao.py` e chama o modelo publicado no watsonx.ai. Se o modelo não responder, usa as regras do plano B. A versão fica registrada em `model_version`.
- **`risk_assessment.signals`** guarda exatamente as 28 features enviadas ao modelo, para auditoria.
- **Recorte da demo:** usar as transações de `teste_proporcao_real.csv`, buscando as colunas completas no CSV bruto pelo id. Assim a demo mostra casos que o modelo nunca viu, e não um resultado inflado pelo treino.

## 5. Uma divergência de produto para alinhar
O `docs/plano_implementacao.md` v2, de 23/10 (PR #5, Pedro H.), diz que **o associado é o usuário principal** e que o analista trata as exceções. Isso combina com a decisão de 27/10 de o agente mandar o aviso sozinho no risco médio, mas os nomes são diferentes:

| Plano v2 (develop) | Watson (glossário e modelo) |
|---|---|
| "Reconheço e autorizo" / "Não reconheço" / "Estou em dúvida" | "Fui eu" / "Não reconheço" / "Prefiro falar com uma pessoa" |
| `LIBERADA_SIMULACAO`, `AGUARDANDO_ASSOCIADO`, `REVISAO_PENDENTE` | `release`, `awaiting_member`, `escalated` |
| Sem resposta até expirar: **encerra como expirada, sem autorizar** | Sem resposta em 10 min: **passa para a analista** |

A regra da falta de resposta é a diferença que importa: no plano, o caso fecha sozinho; no nosso modelo, vai para a analista. Os nomes dá para alinhar depois.
