# Watson · frontend (alta fidelidade)

React 18 + Vite 5 + Carbon (`@carbon/react`). Estado compartilhado entre console e app do associado em `src/state/store.jsx`.

```bash
npm install
npm run dev        # http://localhost:5173  (?apresentacao liga o modo apresentação)
npm run build
```

Pastas:

- `src/pages/`: Fila, Quadro do processo, Caso
- `src/components/`: trilho do Watson, celular do associado, dicionário e tooltips de termos
- `src/data/`: casos fictícios e glossário
- `src/state/`: store (useReducer) com as ações do fluxo ponta a ponta

Para publicar uma versão estática sem servidor: `VITE_ROUTER=memory npx vite build --base ./`.
