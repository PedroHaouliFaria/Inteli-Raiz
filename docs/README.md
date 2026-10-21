# Documentação: Prevenção Inteligente a Fraudes (Sicredi)

Documentação do projeto da Trilha 4 do **IBM AI Experiential Learning Lab 2026**, desenvolvido na optativa IBM do Inteli.

## Documentos

| # | Documento | Conteúdo |
|---|---|---|
| 01 | [Análise Exploratória](01_analise_exploratoria.md) | Linha de raciocínio, decisões e insights sobre os dados de transações |

## Estrutura do repositório

```
docs/            documentação do projeto (este diretório)
  assets/        imagens usadas nos documentos
notebooks/       análises em Jupyter (01_eda, 02_base_balanceada)
scripts/         scripts auxiliares (ex.: gerar as figuras da documentação)
outputs/         resultados gerados pelos notebooks (ex.: triagem de colunas)
data/            dicionário e orientações do case
  processed/     bases prontas para o modelo (treino balanceado e teste)
```

> O CSV original (~290 MB) **não é versionado**. Para rodar os notebooks, coloque `case_transacoes_cartoes_sintetico_900k.csv` em `data/`. Para regerar as figuras desta documentação: `python scripts/gerar_figuras_docs.py`.
