import { createContext, useContext, useEffect, useState } from 'react';

// Estado do painel "Pergunte ao Watson": fechado, ele vira um botão flutuante; aberto, fica por cima
// do conteúdo (versão C, escolhida pelo Leo em 27/10/2026). Começa fechado; a preferência fica salva no navegador.
const RailContext = createContext(null);

function readCollapsed() {
  try { return localStorage.getItem('watson-rail-open') !== '1'; } catch { return true; }
}

export function RailProvider({ children }) {
  const [collapsed, setCollapsed] = useState(readCollapsed);

  useEffect(() => {
    try { localStorage.setItem('watson-rail-open', collapsed ? '0' : '1'); } catch { /* sem armazenamento */ }
  }, [collapsed]);

  const toggle = () => setCollapsed((v) => !v);
  return (
    <RailContext.Provider value={{ collapsed, setCollapsed, toggle }}>
      {children}
    </RailContext.Provider>
  );
}

export function useRail() {
  return useContext(RailContext);
}
