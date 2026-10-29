import { useEffect, useId, useRef, useState } from 'react';
import { Popover, PopoverContent, Link } from '@carbon/react';
import { Information } from '@carbon/icons-react';
import { GLOSSARY } from '../mocks/glossary';
import { useGlossary } from './Glossary';

// Tempo para o mouse atravessar do ícone até a caixa do texto sem a tooltip fechar.
const CLOSE_DELAY_MS = 200;

// Termo com tooltip educativa e atalho para o dicionário. Visual do toggletip do Carbon,
// mas abre no hover e continua aberta enquanto o mouse estiver no ícone ou na caixa do texto.
// Pelo teclado, abre com o foco e fecha com Esc ou ao sair do foco.
export default function Term({ id, children }) {
  const g = GLOSSARY[id];
  const { open: openGlossary } = useGlossary();
  const [open, setOpen] = useState(false);
  const closeTimer = useRef(null);
  const buttonRef = useRef(null);
  const contentId = useId();

  const cancelClose = () => clearTimeout(closeTimer.current);
  const show = () => { cancelClose(); setOpen(true); };
  const hideSoon = () => { cancelClose(); closeTimer.current = setTimeout(() => setOpen(false), CLOSE_DELAY_MS); };
  useEffect(() => cancelClose, []);

  const onKeyDown = (e) => {
    if (open && e.key === 'Escape') {
      e.stopPropagation();
      setOpen(false);
      buttonRef.current?.focus();
    }
  };
  const onBlur = (e) => {
    if (!e.currentTarget.contains(e.relatedTarget)) setOpen(false);
  };

  return (
    <span className="watson-term">
      {children ?? g.term}
      <Popover align="bottom" autoAlign caret highContrast dropShadow={false} open={open}
        className="cds--toggletip" onMouseEnter={show} onMouseLeave={hideSoon} onKeyDown={onKeyDown} onBlur={onBlur}>
        <button ref={buttonRef} type="button" className="cds--toggletip-button" aria-label={`O que é ${g.term}?`}
          aria-expanded={open} aria-controls={contentId} onFocus={show} onClick={show}>
          <Information />
        </button>
        <PopoverContent id={contentId}>
          <div className="cds--toggletip-content">
            <p>{g.definition}</p>
            <div className="cds--toggletip-actions">
              <Link href="#" onClick={(e) => { e.preventDefault(); setOpen(false); openGlossary(id); }}>
                Ver no dicionário
              </Link>
            </div>
          </div>
        </PopoverContent>
      </Popover>
    </span>
  );
}
