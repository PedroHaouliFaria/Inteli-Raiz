import { Toggletip, ToggletipButton, ToggletipContent, ToggletipActions, Link } from '@carbon/react';
import { Information } from '@carbon/icons-react';
import { GLOSSARIO } from '../data/glossario';
import { useDicionario } from './Dicionario';

// Termo com tooltip educativa (Carbon toggletip) e atalho para o dicionário.
export default function Termo({ chave, children }) {
  const g = GLOSSARIO[chave];
  const { abrir } = useDicionario();
  return (
    <span className="watson-termo">
      {children ?? g.termo}
      <Toggletip align="bottom">
        <ToggletipButton label={`O que é ${g.termo}?`}>
          <Information />
        </ToggletipButton>
        <ToggletipContent>
          <p>{g.definicao}</p>
          <ToggletipActions>
            <Link href="#" onClick={(e) => { e.preventDefault(); abrir(chave); }}>
              Ver no dicionário
            </Link>
          </ToggletipActions>
        </ToggletipContent>
      </Toggletip>
    </span>
  );
}
