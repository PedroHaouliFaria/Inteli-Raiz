import { createContext, useContext, useState } from 'react';
import { HeaderPanel } from '@carbon/react';
import { GLOSSARIO } from '../data/glossario';

const DicionarioContext = createContext({ abrir: () => {} });

export function useDicionario() {
  return useContext(DicionarioContext);
}

export function DicionarioProvider({ children }) {
  const [aberto, setAberto] = useState(false);
  const [destaque, setDestaque] = useState(null);
  const abrir = (chave = null) => {
    setDestaque(chave);
    setAberto(true);
  };
  const alternar = () => setAberto((v) => !v);
  return (
    <DicionarioContext.Provider value={{ aberto, destaque, abrir, alternar, fechar: () => setAberto(false) }}>
      {children}
    </DicionarioContext.Provider>
  );
}

export function PainelDicionario() {
  const { aberto, destaque } = useDicionario();
  return (
    <HeaderPanel expanded={aberto} aria-label="Dicionário do Watson">
      <div style={{ padding: '1rem' }}>
        <h2 className="cds--type-heading-02">Dicionário do Watson</h2>
        <dl className="watson-dicionario">
          {Object.entries(GLOSSARIO).map(([chave, g]) => (
            <div key={chave} style={destaque === chave ? { background: 'var(--cds-highlight)', padding: '0 0.5rem 0.5rem' } : undefined}>
              <dt>{g.termo}</dt>
              <dd>{g.definicao}</dd>
              <dd>Onde aparece: {g.onde}</dd>
            </div>
          ))}
        </dl>
      </div>
    </HeaderPanel>
  );
}
