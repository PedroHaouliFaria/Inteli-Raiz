import { createContext, useContext, useEffect, useState } from 'react';

// Estado do painel "Pergunte ao Watson": aberto ou encolhido numa faixa estreita no lugar
// (versão A, escolhida pelo Leo em 27/10/2026). A preferência fica salva no navegador.
const RailContext = createContext(null);

function readCollapsed() {
  try { return localStorage.getItem('watson-rail-collapsed') === '1'; } catch { return false; }
}

export function RailProvider({ children }) {
  const [collapsed, setCollapsed] = useState(readCollapsed);

  useEffect(() => {
    try { localStorage.setItem('watson-rail-collapsed', collapsed ? '1' : '0'); } catch { /* sem armazenamento */ }
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
