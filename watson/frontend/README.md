# frontend

Aplicação de confirmação de compras em React 18 + Vite 5 + Carbon (`@carbon/react`). O associado é o usuário principal; a analista resolve revisões de exceção.

```bash
cd watson/frontend
npm ci
npm run dev        # http://localhost:5173; backend local na porta 8000
npm run build
```

## Entrada e fluxo atual

O `App` começa em `SessionGate`: login com e-mail/senha fictícios e cookie de sessão. O papel ASSOCIADO abre `AssociateApp` e o papel ANALISTA abre `AnalystApp`. O associado lista compras, abre detalhes, responde pelos três botões, conversa ou pede atendimento. A analista pode liberar ou recusar uma compra em revisão; ao atualizar, o associado vê o resultado persistido.

Consulte o [guia de uso](../../docs/anexos/sistema/como-usar-a-demonstracao.md) para preparação, credenciais fictícias e demonstração completa; a [documentação principal](../../docs/documentacao-do-projeto.md#fluxo) explica as decisões.

## Pastas

| Pasta | Papel |
|---|---|
| `src/app/` | `App.jsx` (rotas e casca), `main.jsx` e estilos globais |
| `src/features/` | Fluxo atual em `session/`, `associate/` e `analyst/`; console legado em `queue/`, `board/`, `case/` e `member-app/`; laboratório em `model-lab/` |
| `src/components/` | Só o que mais de uma tela usa: `WatsonRail`, `RailPreferences`, `Term`, `Glossary` |
| `src/api/` | Cliente HTTP do backend (`VITE_API_URL`) |
| `src/state/` | Store (useReducer) do console legado; fluxo integrado usa `src/api/client.js` e o backend |
| `src/mocks/` | Casos fictícios e glossário, usados enquanto a tela não lê da API e no modo apresentação |

## Console legado

A fila, o quadro e o celular descritos abaixo pertencem ao console anterior. Não são o caminho atual de login e confirmação. A implementação legada continua no código como referência visual.

Rotas internas desse console: `/` (fila), `/board` (quadro do processo), `/cases/:id` (caso), `/soon/:section` (telas previstas).

Navegação lateral esquerda: trilho de ícones do Carbon (`SideNav isRail`), como no mockup 3. Só o botão de menu do cabeçalho abre os nomes; no hover e no foco, cada ícone mostra o nome da seção numa tooltip.

Transições: tokens de motion do Carbon (productive no uso do dia a dia, expressive no que aparece de novo), todas em `src/app/index.scss`, desligadas com "reduzir movimento" no sistema.

Tela do caso: a fila fica à esquerda (master-detail, como no wireframe B), ordenada por risco × valor e recolhível; em telas estreitas ela some e a fila continua no menu.

Painel "Pergunte ao Watson": abre pelo botão de IA no cabeçalho e fica por cima do conteúdo, à direita; fecha pelo X, pelo mesmo botão ou com Esc. Começa fechado e a preferência fica salva no navegador.

Para publicar uma versão estática sem servidor: `VITE_ROUTER=memory npx vite build --base ./`.
