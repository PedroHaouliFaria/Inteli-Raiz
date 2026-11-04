# Como os dados do case já foram usados no projeto

> Levantamento feito em 27/10/2026 nas branches do repositório `inteli-raiz`. O trabalho de dados está na branch **`develop`** (PRs #1, #2, #3 e #5, de 20 a 26/10, feitos por Isadora, Pedro R. e Pedro H.). O teste de integração do modelo com o agente está em **`agente/teste-integracao`** (Lucas). A branch `watson` não tem nada disso.

> **Atualização de 04/11/2026:** as seções 1 a 3 são o histórico do trabalho de dados e continuam válidas. As seções 4 e 5 foram reescritas: o Orchestrate saiu do escopo em 27/10, o modelo roda localmente no backend e a divergência de produto foi resolvida a favor do plano.

## Resumo
Sim, parte dos dados já foi usada para treinar um modelo. O time fez a EDA, montou as bases de treino e teste e treinou um Random Forest. O modelo foi publicado no watsonx.ai como teste de integração e hoje roda **localmente** no backend da aplicação.

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
| **EDA** | `notebooks/01_eda.ipynb`, `docs/04_dados_e_modelo/01_analise_exploratoria.md` | Qualidade, sinais da fraude, vazamentos. Triagem de 297 para **31 colunas** (`outputs/triagem_colunas.csv`) |
| **Base balanceada** | `notebooks/02_base_balanceada.ipynb`, `docs/04_dados_e_modelo/02_base_balanceada.md` | Criou 7 features e separou um teste com a proporção real, mais um treino 1:1 |
| **Modelo** | `notebooks/03_modelo.ipynb`, `docs/04_dados_e_modelo/03_modelo.md` | Random Forest com 300 árvores, 28 features, avaliado por PR-AUC e F2 |
| **Integração** | `agente/tools/pontuar_transacao.py`, `docs/03_computacao/specs/teste_integracao_orchestrate_wml.md` | Teste histórico: ferramenta do Orchestrate mandou as 28 features ao modelo publicado no watsonx.ai e recebeu o score. O Orchestrate saiu do escopo em 27/10 |

**Arquivos gerados e versionados** (`data/processed/`):
- `treino_balanceado.csv`: 234 linhas (117 fraudes e 117 legítimas);
- `teste_proporcao_real.csv`: 32.000 linhas (29 fraudes), que o modelo **não viu** no treino;
- `dicionario_base_modelo.csv`: as 35 colunas da base do modelo.

## 3. O que o time descobriu e que muda o nosso modelo de dados
1. **Vazamento.** `decision`, `transaction_status`, `device_ip_country_code = ZZ` e as colunas `dispute_*`, `fdz_*`, `oob_*` e `alert_id` só existem depois que se sabe que foi fraude. A EDA removeu 30 colunas por isso. **Consequência:** o estado da compra na aplicação nunca vem de `transaction_status`; ele começa em `AGUARDANDO_ASSOCIADO` (ou revisão) e muda só pelo fluxo de confirmação.
2. **Scores prontos.** `fraud_score` acerta 100%, igual ao modelo, então ele também "sabe a resposta". Por isso a aplicação não usa essa coluna.
3. **As features de velocidade dominam.** Com `cardid_count_1m`, `cp_card_term_vel_1h`, `cp_card_prev_term_dist_1h` e `digitalwallettoken_count_3m`, o PR-AUC é 1,000. Sem elas, cai para **0,144**. A conclusão do próprio time é que detectar a fraude nesta base é quase trivial, e o valor está no que acontece depois do alerta, que é justamente a confirmação pelo associado.
4. **Sinais que o associado entende.** As 7 features criadas são `hora`, `dia_semana`, `madrugada` (100% das fraudes entre 0h e 4h), `cnp_credito` (83% das fraudes), `valor_vs_media_cartao` (fraude vale 3,9 vezes a média), `primeira_compra_cartao` (70% das fraudes) e `valor_vs_limite`. Três delas viram os sinais mostrados ao associado (seção 4).
5. **Limiar.** O limiar F2 deu 0,817. O plano de 23/10 pede que o limiar saia da validação, e não de uma escolha para a demo ficar bonita.

## 4. Como isso entra na aplicação
- **Score:** `app/risk/` não treina nada. Ele monta as 28 features na mesma ordem do treino e chama o modelo de `outputs/modelo_rf.joblib` (provedor `local`, padrão). O caminho `watsonx`, que chama o modelo publicado, é opcional. A versão fica em `purchases.analysis_model_version`.
- **Features guardadas:** `purchases.features_json` guarda as 28 features usadas, para auditoria.
- **Sinais para o associado:** das 7 features criadas, `cnp_credito`, `madrugada` e `primeira_compra_cartao` viram sinais em linguagem simples. As de velocidade ficam de fora da tela.
- **Recorte da demo:** as compras da demonstração são linhas de `teste_proporcao_real.csv`, que o modelo nunca viu, sem o rótulo de fraude. Detalhes em [uso dos dados na aplicação](uso-dos-dados-na-aplicacao.md).
- **Limiar:** a política em uso é conservadora e manda toda compra avaliada para confirmação; o limiar F2 (0,817) aparece como referência no Laboratório do modelo e não decide o fluxo.

## 5. Divergência de produto: resolvida
Em 27/10 havia duas versões do produto: o plano (associado no centro) e o protótipo do Watson (analista no centro, com "Fui eu" e repasse à analista depois de 10 minutos sem resposta). O grupo seguiu o plano em 28/10:

| Antes (protótipo do Watson) | Agora (plano e código) |
|---|---|
| "Fui eu" / "Não reconheço" / "Prefiro falar com uma pessoa" | "Reconheço e autorizo" / "Não reconheço" / "Estou em dúvida", e "Quero falar com alguém" como ação separada |
| `release`, `awaiting_member`, `escalated` | `LIBERADA_SIMULACAO`, `AGUARDANDO_ASSOCIADO`, `REVISAO_PENDENTE`, `RECUSADA_SIMULACAO`, `CONFIRMACAO_EXPIRADA` |
| Sem resposta em 10 min: passa para a analista | Sem resposta no prazo: **encerra como expirada, sem autorizar** |
| Aviso automático no risco médio (ADR 0004) | Política conservadora: toda compra avaliada pede confirmação |
