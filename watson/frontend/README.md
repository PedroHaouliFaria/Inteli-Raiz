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

Painel "Pergunte ao Watson": encolhe em três versões para escolha (seletor "Painel do Watson" nos controles da demonstração, ou `?rail=strip|header|overlay`):
A · faixa recolhida no lugar; B · some e volta por um botão no cabeçalho; C · abre por cima do conteúdo e, fechado, vira um botão flutuante.

Para publicar uma versão estática sem servidor: `VITE_ROUTER=memory npx vite build --base ./`.
