# Dados e modelo

Da base sintética do case ao modelo de risco usado pela aplicação.

## Análise e modelo

| # | Documento | Conteúdo |
|---|---|---|
| 01 | [Análise exploratória](01_analise_exploratoria.md) | Qualidade dos dados, sinais da fraude e triagem de colunas |
| 02 | [Base balanceada](02_base_balanceada.md) | Bases de treino/teste e as 7 features criadas |
| 03 | [Modelo](03_modelo.md) | Random Forest, avaliação por PR-AUC/F2 e análise crítica |

As figuras ficam em [assets/](assets/) e são geradas por `python scripts/gerar_figuras_docs.py`. Os notebooks correspondentes estão em [notebooks/](../../notebooks/).

## Dados na aplicação

A pasta [dados/](dados/README.md) explica que dados a aplicação guarda e como eles saem do CSV do case até a tela: levantamento, modelo relacional, linha do tempo do cartão e uso na aplicação.

> Esses documentos foram escritos quando a analista era a usuária principal. O modelo de dados continua válido para o backend, mas termos como "caso da analista" se referem hoje às exceções.
