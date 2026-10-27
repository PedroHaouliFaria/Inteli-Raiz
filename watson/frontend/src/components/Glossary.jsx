import { createContext, useContext, useState } from 'react';
import { HeaderPanel } from '@carbon/react';
import { GLOSSARY } from '../mocks/glossary';

const GlossaryContext = createContext({ open: () => {} });

export function useGlossary() {
  return useContext(GlossaryContext);
}

export function GlossaryProvider({ children }) {
  const [isOpen, setIsOpen] = useState(false);
  const [highlight, setHighlight] = useState(null);
  const open = (key = null) => {
    setHighlight(key);
    setIsOpen(true);
  };
  const toggle = () => setIsOpen((v) => !v);
  return (
    <GlossaryContext.Provider value={{ isOpen, highlight, open, toggle, close: () => setIsOpen(false) }}>
      {children}
    </GlossaryContext.Provider>
  );
}

export function GlossaryPanel() {
  const { isOpen, highlight } = useGlossary();
  return (
    <HeaderPanel expanded={isOpen} aria-label="Dicionário do Watson">
      <div style={{ padding: '1rem' }}>
        <h2 className="cds--type-heading-02">Dicionário do Watson</h2>
        <dl className="watson-glossary">
          {Object.entries(GLOSSARY).map(([key, g]) => (
            <div key={key} style={highlight === key ? { background: 'var(--cds-highlight)', padding: '0 0.5rem 0.5rem' } : undefined}>
              <dt>{g.term}</dt>
              <dd>{g.definition}</dd>
              <dd>Onde aparece: {g.where}</dd>
            </div>
          ))}
        </dl>
      </div>
    </HeaderPanel>
  );
}
