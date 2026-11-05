# Sessão 2 no Bob — Isadora

Tarefas rodadas no Bob IDE (modo Agent, interação direta no chat).
Aparecem em **Tasks → All workspaces**.

| Tarefa | ID | Início | Custo | Chamadas de ferramenta |
|---|---|---|---|---|
| Identificação dos arquivos bob_sessions; reformulação do canvas; push; setup do projeto; criação das sessões da Isadora | `675f0316891855b08c1d66dddc0ffa37` | 05/11 12:36 UTC | 21.93 | 88 |
| **Total** | | | **$21.93** | |

O custo vem do `_meta.spend.cost` de cada mensagem de assistant no histórico local do Bob (`~/.bob/db/bob.db`).

## O que foi feito nesta sessão

- Explicação do que são os arquivos `bob_sessions/lucas/*.md` (diário de execução das sessões do Lucas).
- Decisão de manter ou remover os arquivos (mantidos como histórico).
- **Reformulação do Canvas de Proposta de Valor** (`docs/01_negocios/canvas_proposta_de_valor.md`): adicionado template visual correto com dois blocos (Mapa de Valor × Perfil do Cliente), sumário clicável e parágrafos justificados no estilo do projeto `g03`.
- **Padronização de estilo em 8 documentos** de `docs/`: D01, D02, D03, D04, D05, D06, D07, D08 — sumários clicáveis e parágrafos narrativos formatados com `<p align="justify">`.
- Criação da branch `docs/reformulacao-canvas` e commit + push (`85beeaea`).
- Configuração do `.env` do backend com as chaves fornecidas (SESSION\_SECRET, GROQ\_API\_KEY e demais variáveis).
- Subida do backend (`uvicorn`) em background usando venv Windows — rodando em http://localhost:8000.
- Subida do frontend (`npm run dev`) — rodando em http://localhost:5173.
- Criação das pastas e arquivos de sessão da Isadora em `bob_sessions/isadora/`.

## O que a revisão humana corrigiu ou verificou

- Identificado que a distro WSL Ubuntu não estava disponível na máquina (só `docker-desktop`) — backend rodou via Python 3.14 do Windows com venv local `.venv-win`.
- O extra `risk` (scikit-learn) não instalou no Python 3.14 por falta de wheel compatível; o modelo de risco local ficou indisponível, mas o restante do backend funcionou normalmente.
- O `uvicorn.exe` que estava no `.venv` original era um wrapper do WSL, não um executável Windows real — necessário criar `.venv-win` separado.

## Resumo final da tarefa

```text
Tudo rodando:

Backend:  http://localhost:8000        (FastAPI + uvicorn, .venv-win)
Frontend: http://localhost:5173        (React + Vite, npm run dev)
Docs:     http://localhost:8000/docs   (Swagger)

Logins de demonstração:
  Ana Souza   | ana@raiz.demo    | Ana@123    (Associado)
  Bruno Lima  | bruno@raiz.demo  | Bruno@123  (Associado)
  Carla Reis  | carla@raiz.demo  | Carla@123  (Analista)

Para mexer no código:
  Frontend → watson/frontend/src/  (Vite recarrega automaticamente)
  Backend  → watson/backend/app/   (uvicorn --reload recarrega automaticamente)
```
