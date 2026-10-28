# Regras do backend (watson/backend)

## Fontes da verdade
- Contrato da API: `docs/specs/contrato_api.md`. Não mude nome de campo, código de erro, status HTTP ou formato de resposta por conta própria. Se a spec estiver ambígua ou incompleta, pare e pergunte.
- Produto e regras: `docs/plano_implementacao.md`, em especial §3, §5 e "Alinhamento com o Watson (28/10)". Quando o código existente do Watson discordar do plano, vale o plano.

## Stack e organização
- Python 3.12, FastAPI, Pydantic v2, pydantic-settings, SQLAlchemy 2 sobre SQLite, pytest. Nada de dependência nova sem eu pedir.
- Siga as camadas do Watson: `app/api` (rotas e esquemas) → `app/domain` (regras, sem FastAPI nem SQL) → `app/db` (tabelas e repositórios). SQL só em `app/db/repositories/`.
- Rotas novas do contrato ficam sob `/api`. Não mexa em `/health` nem em `/model-lab`.
- Configuração por variável de ambiente, no `app/config.py`, no mesmo estilo dos campos que já existem. Nenhum segredo no código ou em arquivo versionado.
- Código, rotas, tabelas e colunas em inglês. Mensagens ao usuário e comentários em português.
- O venv fica em `watson/backend/.venv`. Rode os testes com `cd watson/backend && .venv/bin/python -m pytest -q`.

## Regras de negócio que não se negociam
- Identidade vem só do cookie de sessão. Nunca aceite `customer_id` do corpo, da URL ou do texto do LLM. Compra de outra pessoa responde 404, igual a uma inexistente.
- Nunca exponha ao associado: `feedback_label`, `customer_id`, `card_id` completo, renda, saldo, limite ou score.
- Respostas do associado: `AUTHORIZE`, `DENY`, `UNSURE`. Recusar a compra não bloqueia o cartão.
- Sem biometria nem aparelho: a base não tem esses dados.
- Nada de score, sinal ou evento inventado. Sinal só de feature com significado documentado.

## Forma de trabalhar
- Teste primeiro: escreva o teste, rode e mostre a falha, implemente, rode de novo e mostre a saída do pytest. Nunca diga que passou sem mostrar a saída.
- Os 27 testes que já existem continuam passando.
- Termine o que foi pedido e pare. Não adiante passos seguintes.
