# Laboratório do modelo

Pedido do Leo em 27/10/2026: uma aba de ambiente experimental onde submetemos uma transação e vemos o que o modelo de risco inferiu (score, faixa baixa/média/alta e os sinais que mais pesaram). Não gera alerta, caso nem aviso.

| Versão | Ideia | Canvas |
|---|---|---|
| A · Bancada | Formulário dos 28 campos à esquerda, resultado à direita | [LAB-A-Bancada](canvas/LAB-A-Bancada.dc.html) |
| **B · E se?** (escolhida) | Original × editado lado a lado, tabela de campos e histórico da sessão | [LAB-B-E-se](canvas/LAB-B-E-se.dc.html) |
| C · Explorador | Tabela do conjunto de teste pontuado, filtro por faixa e painel lateral | [LAB-C-Explorador](canvas/LAB-C-Explorador.dc.html) |

Canvas: https://claude.ai/artifact/2pfM7J8PKDaoX4rYW5mUpA (privado; compartilhar pelo menu Share).

## Decisões
- Faixas: as da política do aviso de compra (decisão 0004): médio a partir de 0,60, alto a partir de 0,80. O tracejado é o limiar F2 do modelo (0,817).
- Fatores: quanto o score cai se só aquele campo volta ao valor típico das compras legítimas do treino.
- Nenhuma transação do conjunto de teste cai no risco médio (maior legítima 0,58, menor fraude 0,82). O médio só aparece editando campos, por exemplo baixar "Uso cartão × terminal (1h)" de 70 para 2 na EVT_SYN_000094500 leva o score de 0,99 para 0,69.

## Código
- Frontend: `watson/frontend/src/features/model-lab/` (rota `/model-lab`).
- Backend: `watson/backend/app/risk/` (modelo, bases, fatores) e `app/api/routes/model_lab.py`.
