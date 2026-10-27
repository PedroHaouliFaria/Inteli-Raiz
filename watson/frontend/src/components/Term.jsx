import { Toggletip, ToggletipButton, ToggletipContent, ToggletipActions, Link } from '@carbon/react';
import { Information } from '@carbon/icons-react';
import { GLOSSARY } from '../mocks/glossary';
import { useGlossary } from './Glossary';

// Termo com tooltip educativa (Carbon toggletip) e atalho para o dicionário.
export default function Term({ id, children }) {
  const g = GLOSSARY[id];
  const { open } = useGlossary();
  return (
    <span className="watson-term">
      {children ?? g.term}
      <Toggletip align="bottom">
        <ToggletipButton label={`O que é ${g.term}?`}>
          <Information />
        </ToggletipButton>
        <ToggletipContent>
          <p>{g.definition}</p>
          <ToggletipActions>
            <Link href="#" onClick={(e) => { e.preventDefault(); open(id); }}>
              Ver no dicionário
            </Link>
          </ToggletipActions>
        </ToggletipContent>
      </Toggletip>
    </span>
  );
}
