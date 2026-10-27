# 0004 · Aviso de compra automático no risco médio

**Status:** aceita pelo Leo em 27/10/2026.

## Decisão
Nos casos de risco médio, o agente envia o aviso de compra ao associado sem esperar a analista. A analista só entra nas exceções:

| Situação | Quem trata |
|---|---|
| Risco alto | Analista, desde o início |
| Risco médio | Agente envia o aviso sozinho |
| "Fui eu" com biometria em aparelho conhecido | Watson libera a compra |
| "Fui eu" vindo de aparelho trocado recentemente | Analista |
| "Não reconheço" | Analista (a compra segue retida) |
| Pedido de atendimento ("Prefiro falar com uma pessoa") | Analista |
| Sem resposta no prazo | Analista |

## Onde está no código
- Backend: `watson/backend/app/domain/notices/policy.py` (`initial_handling`, `outcome_for_response`, `is_expired`), com testes em `tests/unit/test_notice_policy.py`.
- Frontend: `watson/frontend/src/state/noticePolicy.js`. A fila mostra só o que precisa da analista, com a coluna "Por que está com você" (escalation_reason) e o indicador "Conduzidos pelo Watson"; o quadro marca "Aviso pelo Watson".

## Configurável enquanto o time não decide
| Ponto | Backend (`.env`) | Frontend | Padrão |
|---|---|---|---|
| "Fui eu" fecha o caso sozinho? | `NOTICE_AUTO_CLOSE_ON_IT_WAS_ME` | `VITE_NOTICE_AUTO_CLOSE_ON_IT_WAS_ME` | `true` |
| Prazo de resposta do associado | `NOTICE_RESPONSE_TIMEOUT_MINUTES` | `VITE_NOTICE_RESPONSE_TIMEOUT_MINUTES` | 30 min |
| Limiares médio / alto | `NOTICE_MEDIUM_THRESHOLD`, `NOTICE_HIGH_THRESHOLD` | fixos em `noticePolicy.js` | 0,60 / 0,80 (provisórios) |

## Em aberto
- Valores finais dos limiares, vindos da versão do modelo.
- Bloqueio preventivo do cartão enquanto o caso aguarda o associado (sugestão da pesquisa): ainda não está no modelo de dados nem na tela.
