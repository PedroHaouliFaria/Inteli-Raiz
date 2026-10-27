import { createContext, useContext, useEffect, useState } from 'react';

// Como o painel "Pergunte ao Watson" encolhe. Três versões para o Leo escolher (pedido de 27/10/2026):
// strip: vira uma faixa estreita no lugar · header: some e volta por um botão no cabeçalho ·
// overlay: abre por cima do conteúdo e, fechado, vira um botão flutuante.
export const RAIL_VARIANTS = {
  strip: 'A · Faixa recolhida',
  header: 'B · Botão no cabeçalho',
  overlay: 'C · Sobreposição com botão flutuante',
};

const RailContext = createContext(null);

function read(key, fallback) {
  try { return localStorage.getItem(key) ?? fallback; } catch { return fallback; }
}

function write(key, value) {
  try { localStorage.setItem(key, value); } catch { /* sem armazenamento */ }
}

function initialVariant() {
  const fromUrl = new URLSearchParams(window.location.search).get('rail');
  if (fromUrl in RAIL_VARIANTS) return fromUrl;
  const stored = read('watson-rail-variant', 'strip');
  return stored in RAIL_VARIANTS ? stored : 'strip';
}

export function RailProvider({ children }) {
  const [variant, setVariant] = useState(initialVariant);
  const [collapsed, setCollapsed] = useState(() => read('watson-rail-collapsed', '0') === '1');

  useEffect(() => write('watson-rail-variant', variant), [variant]);
  useEffect(() => write('watson-rail-collapsed', collapsed ? '1' : '0'), [collapsed]);

  const toggle = () => setCollapsed((v) => !v);
  return (
    <RailContext.Provider value={{ variant, setVariant, collapsed, setCollapsed, toggle }}>
      {children}
    </RailContext.Provider>
  );
}

export function useRail() {
  return useContext(RailContext);
}
