# frontend

Console da analista e app do associado em React 18 + Vite 5 + Carbon (`@carbon/react`).

```bash
cd watson/frontend
npm install
npm run dev        # http://localhost:5173  (?presentation liga o modo apresentação)
npm run build
```

## Pastas

| Pasta | Papel |
|---|---|
| `src/app/` | `App.jsx` (rotas e casca), `main.jsx` e estilos globais |
| `src/features/` | Uma pasta por tela: `queue/`, `board/`, `case/`, `member-app/` (celular do associado) e `coming-soon/` (itens do menu ainda sem tela) |
| `src/components/` | Só o que mais de uma tela usa: `WatsonRail`, `RailPreferences`, `Term`, `Glossary` |
| `src/api/` | Cliente HTTP do backend (`VITE_API_URL`) |
| `src/state/` | Store (useReducer) com as ações do fluxo ponta a ponta |
| `src/mocks/` | Casos fictícios e glossário, usados enquanto a tela não lê da API e no modo apresentação |

Rotas: `/` (fila), `/board` (quadro do processo), `/cases/:id` (caso), `/soon/:section` (telas previstas).

Navegação lateral esquerda: trilho de ícones do Carbon (`SideNav isRail`), como no mockup 3; o botão de menu do cabeçalho abre e recolhe os nomes.

Tela do caso: a fila fica à esquerda (master-detail, como no wireframe B), ordenada por risco × valor e recolhível; em telas estreitas ela some e a fila continua no menu.

Painel "Pergunte ao Watson": fechado, vira um botão flutuante no canto inferior direito; aberto, fica por cima do conteúdo, à direita. Começa fechado e a preferência fica salva no navegador.

Para publicar uma versão estática sem servidor: `VITE_ROUTER=memory npx vite build --base ./`.
