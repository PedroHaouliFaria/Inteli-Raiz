# Como os dados do case chegam à aplicação

**Versão:** 1.0 · 04/11/2026 · **Estado:** descreve o código atual do backend (`watson/backend/app/`).

> **Leia antes:** [como os dados já foram usados](como-os-dados-ja-foram-usados.md) — a EDA, a base balanceada e o modelo que este caminho reaproveita.

O CSV completo do case (`case_transacoes_cartoes_sintetico_900k.csv`, ~290 MB) não é versionado nem carregado pela aplicação. A demo usa **compras fixas (fixtures)** tiradas de linhas reais da base de teste do modelo.

## O caminho em 5 passos

```
data/processed/teste_proporcao_real.csv
   │ 1. fixtures: linhas escolhidas, sem o rótulo de fraude
   ▼
app/fixtures/purchases.json
   │ 2. entrada (seed ou POST /api/demo/purchases)
   ▼
modelo local (outputs/modelo_rf.joblib) → score, versão do modelo
   │ 3. política conservadora
   ▼
purchases + confirmations + events      (ou reviews FALHA_AVALIACAO se o modelo falhar)
   │ 4. API FastAPI com sessão do associado
   ▼
5. frontend: app do associado (compra, sinais, resposta, chat, ajuda)
   e lista de revisões da analista
```

### 1. Fixtures
`app/fixtures/purchases.json` traz as compras da demonstração. Cada uma é uma linha de `teste_proporcao_real.csv` (que o modelo **não viu** no treino), com as 28 features e **sem** `feedback_label`, para o rótulo nunca chegar ao agente nem à tela. A data é sintética e coerente com a `hora` e o `dia_semana` da linha.

| Fixture | Associado | Uso |
|---|---|---|
| `fraude_supermercado_madrugada` (T-007) | Ana | Autorizar ou recusar |
| `legitima_farmacia` (T-003) | Ana | Dúvida contextual no chat |
| `compra_do_bruno` (T-011) | Bruno | Teste de acesso cruzado |
| `falha_modelo` | Ana | Só pela demo: feature ausente → revisão segura |

Detalhes no [contrato da API](../../sistema/specs/contrato-da-api.md) §11.

### 2. Entrada
O seed (banco vazio) e o endpoint de demo usam **a mesma função** (`domain/cases/intake.py`), para que o que se vê na demo seja o mesmo caminho do seed.

### 3. Score e política
- O modelo é o Random Forest do [notebook 03](../avaliacao-do-modelo.md), carregado de `outputs/modelo_rf.joblib` (`RISK_MODEL_PROVIDER=local`, padrão). O caminho `watsonx` chama o modelo publicado no watsonx.ai e é opcional.
- O score fica em `purchases.analysis_score` com a origem e a versão do modelo. Ele aparece **só** para a analista, como "score interno do modelo"; o associado e o agente não o veem.
- O associado vê **sinais** com significado documentado (`domain/signals/rules.py`): compra sem o cartão físico, feita de madrugada, primeira compra do cartão. As features de velocidade ficam de fora, porque não têm explicação compreensível.
- Política conservadora: toda compra avaliada vai para `AGUARDANDO_ASSOCIADO`, com prazo de `CONFIRMATION_TTL_SECONDS` (900 s por padrão). Se o modelo falha: `REVISAO_PENDENTE` e revisão `FALHA_AVALIACAO`, sem score.

### 4. API

| Para quê | Rota |
|---|---|
| Entrar como associado fictício | `POST /api/session`, `GET /api/session/personas` |
| Listar e abrir compras da sessão | `GET /api/purchases`, `GET /api/purchases/{case_id}`, `.../status` |
| Responder à confirmação | `POST /api/confirmations/{challenge_id}/response` (com `Idempotency-Key`) |
| Conversar com o agente | `GET/POST /api/purchases/{case_id}/chat` |
| Pedir revisão / falar com alguém | `POST /api/purchases/{case_id}/review` |
| Revisões (analista) | `GET /api/reviews` |
| Demo | `POST /api/demo/purchases`, `POST /api/demo/reset` (só com `DEMO_MODE=true`) |
| Laboratório do modelo | `/model-lab/info`, `/samples`, `/score` |

### 5. Telas
- **Associado** (`features/associate/`): lista de compras, detalhe com sinais e prazo, três respostas, chat e pedido de atendimento. Descrição e decisões em [D12](../../experiencia-do-usuario/telas-e-fluxo-do-usuario.md).
- **Analista** (`features/analyst/`): lista de revisões abertas, somente leitura.
- O console antigo da analista (fila, quadro e caso, com dados fixos de `src/mocks/`) continua no código só como interface de reserva; não lê o banco.

## O que não está coberto
- Carga do CSV completo e simulação contínua de chegada de transações: fora do MVP.
- Mais casos de demo no mesmo formato das fixtures: previsto no contrato §11.
