# Documentação: Prevenção Inteligente a Fraudes (Sicredi)

Documentação do projeto da Trilha 4 do **IBM AI Experiential Learning Lab 2026**, desenvolvido na optativa IBM do Inteli.

## Documentos

| # | Documento | Conteúdo |
|---|---|---|
| 01 | [Análise Exploratória](01_analise_exploratoria.md) | Linha de raciocínio, decisões e insights sobre os dados de transações |
| 02 | [Base Balanceada](02_base_balanceada.md) | Construção das bases de treino/teste e as 7 features criadas a partir dos insights |
| 03 | [Modelo](03_modelo.md) | Pipeline de pré-processamento, Random Forest, avaliação por PR-AUC e análise crítica dos resultados |

## Plano de implementação proposto

- [Plano revisado: confirmação de compras pelo associado](plano_implementacao.md).
- [Direcional das entregas recomendadas nas aulas](direcional_entregas.md): 11 entregas, estruturas para preencher, instruções, fontes/templates, revisão e critérios de qualidade; inclui prototipação e validação como apoio.
- [Versão em PDF — v2 de 23/10/2026](plano_implementacao.pdf). A ampliação de 27/10/2026 está no plano Markdown e no direcional acima; ainda não está incorporada a esse PDF.

O sistema avalia a compra e decide o tratamento inicial; o associado autoriza, recusa ou informa dúvida, e o analista trata exceções. Ações financeiras são simuladas no MVP. A proposta inclui regras, arquitetura, requisitos, backlog e testes; não representa implementação concluída.

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
