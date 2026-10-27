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
`watson/backend/app/domain/notices/policy.py` (`initial_handling` e `outcome_for_response`), com testes em `tests/unit/test_notice_policy.py`.

## Em aberto
- Limiares: o padrão provisório é médio a partir de 0,60 e alto a partir de 0,80 (glossário). Os valores finais vêm da versão do modelo.
- Prazo de resposta do associado.
- No protótipo do frontend, quem envia o aviso ainda é a analista ("Perguntar ao associado"); a tela precisa refletir o envio automático.
