# Dados da aplicação

Que dados a aplicação de confirmação de compras guarda, de onde vêm e como chegam à tela. **Revisão:** 04/11/2026, alinhada ao [plano](../../gestao/regras-do-produto.md) e ao código em `watson/backend/`.

| Arquivo | O que tem | Estado |
|---|---|---|
| [levantamento-de-dados.md](levantamento-de-dados.md) | Cada dado ligado a uma necessidade do associado ou da analista, e o que aproveitamos das 297 colunas do case | atualizado |
| [modelo-de-dados.md](modelo-de-dados.md) | As 6 tabelas do banco, estados da compra e regras garantidas | atualizado (descreve o código) |
| [uso-dos-dados-na-aplicacao.md](uso-dos-dados-na-aplicacao.md) | Caminho das fixtures até a tela: modelo, política, API e telas | atualizado |
| [como-os-dados-ja-foram-usados.md](como-os-dados-ja-foram-usados.md) | Histórico do trabalho de dados: EDA, base balanceada, modelo e teste no watsonx.ai | histórico + seções 4–5 atualizadas |
| [linha-do-tempo.md](linha-do-tempo.md) | Se o case permite montar a linha do tempo de um cartão; rajadas | análise válida; recomendações de tela eram do console antigo |

## Resumo em uma linha
A compra (linha real da base de teste, sem rótulo) é avaliada pelo modelo local, vira um **pedido de confirmação** ao associado e termina **liberada, recusada, em revisão ou expirada** — tudo simulado e registrado em eventos.

## Fontes
- Contrato da API: [contrato_api.md](../../sistema/specs/contrato-da-api.md)
- Arquitetura atual: [D10](../../sistema/arquitetura-do-sistema.md)
- Case Sicredi no repositório: `data/dicionario_dados_case_prevencao_sicredi.xlsx` e `data/Orientacoes_case_prevencao_sicredi.txt`
