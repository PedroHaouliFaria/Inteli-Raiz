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
| `src/features/` | Uma pasta por tela: `queue/`, `board/`, `case/` e `member-app/` (celular do associado) |
| `src/components/` | Só o que mais de uma tela usa: `WatsonRail`, `Term`, `Glossary` |
| `src/api/` | Cliente HTTP do backend (`VITE_API_URL`) |
| `src/state/` | Store (useReducer) com as ações do fluxo ponta a ponta |
| `src/mocks/` | Casos fictícios e glossário, usados enquanto a tela não lê da API e no modo apresentação |

Rotas: `/` (fila), `/board` (quadro do processo), `/cases/:id` (caso).

Para publicar uma versão estática sem servidor: `VITE_ROUTER=memory npx vite build --base ./`.
