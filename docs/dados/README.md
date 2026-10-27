# Watson · Dados

Quais dados o Watson precisa guardar e como organizá-los num banco. Tudo aqui é **proposta para discussão** (v0.3, 27/10/2026: nomes de tabelas e colunas em inglês, com tabela de correspondência para o glossário).

| Arquivo | O que tem | Status |
|---|---|---|
| [levantamento-de-dados.md](levantamento-de-dados.md) | Cada dado ligado à necessidade de uma persona ou tela, e o que aproveitamos (ou descartamos) das 297 colunas do case | pronto para revisão |
| [modelo-de-dados.md](modelo-de-dados.md) | Modelo relacional inicial: diagrama, entidades, atributos, relações, regras e decisões em aberto | pronto para revisão |

## Resumo em uma linha
Três blocos: **Origem** (associado, conta, cartão, estabelecimento, dispositivo, transação; só leitura), **Risco** (versão do modelo, score, fatores explicáveis) e **Análise** (alerta, caso, recomendação do agente, eventos do caso, decisão da analista, aviso de compra ao associado, desfecho e auditoria). Termos alinhados ao [glossário](../design/glossario.md).

## Fontes
- Descoberta: [../design/00-descoberta/](../design/00-descoberta/README.md)
- Wireframes (escolhido: B com a fila da A e o quadro da C): [../design/01-wireframe/](../design/01-wireframe/README.md)
- Case Sicredi no repositório: `data/dicionario_dados_case_prevencao_sicredi.xlsx` e `data/Orientacoes_case_prevencao_sicredi.txt`

## Próximos passos sugeridos
1. Time responde às decisões em aberto do modelo.
2. Escrever o DDL (script de criação das tabelas) e um script de carga do case.
3. Diagrama visual no estilo IBM (Carbon) para a apresentação.
