# 04 · Alta fidelidade (em código)

Protótipo 3 (ponta a ponta em tempo real) com os chips de pergunta do protótipo 2, feito direto em React + Carbon (`@carbon/react`, tema g10, cabeçalho g100).

- Versão clicável (privada, compartilhar pelo menu Share): https://claude.ai/artifact/HnhD256hVacK5soMm5i3oU
- Código: [watson/frontend/](../../../watson/frontend/README.md)
- Telas de referência: [telas/](telas/)

## Escolha do Leo (26/10/2026): 2 no produto, 3 na banca

Das 3 variações apresentadas (1 lado a lado, 2 celular sob demanda, 3 apresentação), ficaram duas:

| Modo | Como o celular do associado aparece | Para quê |
|---|---|---|
| Produto (variação 2) | Painel que abre sozinho quando o Watson envia o aviso (ícone de celular no cabeçalho) | Interface real da analista, console limpo |
| Modo apresentação (variação 3) | Coluna fixa + narração em 5 passos no topo | Banca, vídeo e teste de usabilidade guiado |

A barra tracejada "Controles da demonstração" liga o modo apresentação e o cenário de aparelho trocado. Ela não faz parte do produto. Link direto para o modo apresentação: acrescente `#apresentacao` ao link publicado (ou `?apresentacao` no servidor local).

## O que dá para testar

1. Fila: KPIs com tooltip, tabela ordenada por risco × valor, sugestão do Watson.
2. Caso #4821: fatores do score, linha do tempo, chips "Por que 0,92?", "Compare com o histórico", "Redija a justificativa" (insere no campo).
3. "Preparar aviso" ou "Perguntar ao associado": modal com a regra combinada; o caso vai para "Aguardando associado".
4. No celular: "Não reconheço" bloqueia com um toque; "Sim, fui eu" pede a digital.
5. Cenário "Aparelho trocado há 2 dias" (contramedida da anti-persona): mesmo com a digital, o caso volta para a analista.
6. Quadro do processo: colunas por estado, desagrupar o #5107, reenviar avisos parados.
7. Dicionário (ícone "?") e tooltips em Alerta, Caso, Score, Tempo até a decisão, Aguardando associado, Confiança.

Dados fictícios. O "Tempo até a decisão" mostra um valor fictício até termos o registro de eventos.
