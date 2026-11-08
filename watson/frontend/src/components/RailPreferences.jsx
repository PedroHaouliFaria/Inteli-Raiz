import { createContext, useContext, useEffect, useRef, useState } from 'react';

// Estado do painel "Pergunte ao Watson": abre e fecha pelo botão de IA no cabeçalho e fica por cima do conteúdo,
// à direita (27/10/2026: o botão flutuante cobria "Bloquear cartão"). Começa fechado; a preferência fica salva no navegador.
const RailContext = createContext(null);

function readCollapsed() {
  try { return localStorage.getItem('watson-rail-open') !== '1'; } catch { return true; }
}

export function RailProvider({ children }) {
  const [collapsed, setCollapsed] = useState(readCollapsed);
  const triggerRef = useRef(null);

  useEffect(() => {
    try { localStorage.setItem('watson-rail-open', collapsed ? '0' : '1'); } catch { /* sem armazenamento */ }
  }, [collapsed]);

  const toggle = () => setCollapsed((v) => !v);
  return (
    <RailContext.Provider value={{ collapsed, setCollapsed, toggle, triggerRef }}>
      {children}
    </RailContext.Provider>
  );
}

export function useRail() {
  return useContext(RailContext);
}
