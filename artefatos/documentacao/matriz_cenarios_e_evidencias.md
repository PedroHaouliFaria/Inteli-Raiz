# Matriz de cenários e evidências

**Versão:** 0.3 · **Data:** 04/11/2026 · **Responsável:** Integração e validação.\
**Execução:** develop f741a35, 207 testes aprovados. [Log](../evidencias/2026-11-04/pytest.log) e [ambiente](../evidencias/2026-11-04/ambiente.json). Os casos P4-T mantêm IDs históricos; não representam pastas por pessoa.

| Requisito | Casos | Arquivo de teste em watson/backend/tests/ | Estado técnico atual | Evidência adicional necessária |
|---|---|---|---|---|
| R01 Avaliação/política | P4-T10 | integration/test_analysis.py, test_seed.py, test_demo.py | Suíte aprovada; score/falha cobertos | Revisão de qualidade do modelo e UI |
| R02 Compra correta | P4-T01/T02 | integration/test_purchases.py | Suíte aprovada | Inspeção UI |
| R03 Respostas distintas | P4-T01/T02/T03 | integration/test_confirmations.py | Suíte aprovada | Três percursos UI |
| R04 Expiração | P4-T06 | integration/test_confirmations.py, test_purchases.py | Suíte aprovada | Expiração visível; ajuda não estende prazo |
| R05 Dono/sessão | P4-T08 | integration/test_session.py, test_purchases.py, test_chat.py | Suíte aprovada | Troca de sessão UI |
| R06 Repetição/concorrência | P4-T07 | integration/test_confirmations.py | Suíte aprovada | Retry/duplo clique UI |
| R07 Explicação fiel | P4-T09/T10 | integration/test_analysis.py, test_chat.py; unit/test_avaliar_transacao_security.py | Regras/ferramentas em teste controlado aprovadas | Explicação de LLM real comparada aos dados |
| R08 Dúvida contextual | P4-T04/T05/T12 | integration/test_chat.py, test_reviews.py | Ferramentas/revisão com modelo controlado aprovadas | LLM real e compreensão em D13 |
| R09 Falha segura | P4-T09/T10/T12 | integration/test_chat.py, test_chat_no_lock.py, test_analysis.py | Suíte aprovada | UI em falha de rede/LLM |
| R10 Persistência | P4-T11 | integration/test_confirmations.py, test_chat.py, test_purchases.py | Segunda instância/histórico aprovados | Reinício/recarga UI independente |
| R11 Simulação | P4-T01/T02/T03 | integration/test_purchases.py, test_confirmations.py | Respostas de API aprovadas | Linguagem/tela e compreensão |
| R12 Reprodução | Todos | Roteiro D11 | Backend reproduzido nesta revisão | Outra pessoa percorre UI sem ajuda |

O backend usa bancos temporários nos testes e modelos controlados para LLM. Nenhuma chamada externa real nem sessão de pesquisa foi executada nesta revisão. O resultado histórico 151/15/3 de 28/10 não se aplica ao código atual; permanece identificado no histórico de evidências.

## Encadeamento de experiência

HIP-01 → compreensão recusa/bloqueio → D12 textos de resultado → R03/R11 → P4-T02 + C5 de D13.\
HIP-02 → ajuda sem encerrar confirmação → R03/R04/R08 → P4-T04/T05/T06 + C4.\
HIP-P1-05 → vantagem da conversa → A/B com mesmos dados → R08 → D13, ainda não executado.\
HIP-09 → desfecho compreensível → R10/R11 → P4-T11 + perguntas de resultado.
