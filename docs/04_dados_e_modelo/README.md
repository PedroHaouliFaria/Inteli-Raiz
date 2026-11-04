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

A pasta [dados/](dados/README.md) explica que dados a aplicação guarda e como chegam à tela: levantamento por necessidade, as 6 tabelas do banco, o caminho das fixtures até o app do associado e o histórico do trabalho de dados. Revisada em 04/11 para o fluxo atual.
