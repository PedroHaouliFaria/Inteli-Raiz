import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IconButton, Tag } from '@carbon/react';
import { SidePanelClose, SidePanelOpen } from '@carbon/icons-react';
import { riskLevel, formatBRL } from '../../mocks/cases';
import { useWatson } from '../../state/store';
import { analystQueue } from '../../state/queue';

function readCollapsed() {
  try { return localStorage.getItem('watson-case-queue-collapsed') === '1'; } catch { return false; }
}

// Fila ao lado do caso (master-detail do wireframe B): trocar de caso sem voltar para a fila.
// Recolhível numa faixa estreita para dar a tela ao caso (escolha do Leo em 27/10/2026).
export default function CaseQueue({ currentId }) {
  const navigate = useNavigate();
  const { state } = useWatson();
  const [collapsed, setCollapsed] = useState(readCollapsed);
  const queue = analystQueue(state.cases);

  useEffect(() => {
    try { localStorage.setItem('watson-case-queue-collapsed', collapsed ? '1' : '0'); } catch { /* sem armazenamento */ }
  }, [collapsed]);

  if (collapsed) {
    return (
      <nav className="watson-case-queue watson-case-queue--collapsed" aria-label="Fila de casos (recolhida)">
        <IconButton kind="ghost" size="md" label="Mostrar a fila" align="right" onClick={() => setCollapsed(false)}>
          <SidePanelOpen />
        </IconButton>
        <span className="watson-case-queue__vertical-label">Fila · {queue.length}</span>
      </nav>
    );
  }

  return (
    <nav className="watson-case-queue" aria-label="Fila de casos">
      <div className="watson-case-queue__header">
        <div>
          <h2 className="cds--type-heading-compact-01">Fila</h2>
          <p className="cds--type-helper-text-01">Por risco × valor · {queue.length} casos</p>
        </div>
        <IconButton kind="ghost" size="sm" label="Recolher a fila" align="right" onClick={() => setCollapsed(true)}>
          <SidePanelClose />
        </IconButton>
      </div>
      <ul className="watson-case-queue__list">
        {queue.map((c) => {
          const risk = riskLevel(c.score);
          const active = c.id === currentId;
          return (
            <li key={c.id}>
              <button type="button" className={`watson-case-queue__item${active ? ' watson-case-queue__item--active' : ''}`}
                aria-current={active ? 'page' : undefined} onClick={() => navigate(`/cases/${c.id}`)}>
                <span className={`watson-case-queue__bar watson-case-queue__bar--${risk.tagType}`} aria-hidden="true" />
                <span className="watson-case-queue__text">
                  <span className="cds--type-heading-compact-01">#{c.id} · {c.member}</span>
                  <span className="cds--type-helper-text-01">{formatBRL(c.amount)} · {c.waitTime} na fila</span>
                </span>
                <span className="watson-case-queue__score">
                  <span className="cds--type-code-01">{c.score.toFixed(2).replace('.', ',')}</span>
                  <Tag type={risk.tagType} size="sm">{risk.label}</Tag>
                </span>
              </button>
            </li>
          );
        })}
        {queue.length === 0 && <li className="cds--type-helper-text-01" style={{ padding: '1rem' }}>Nenhum caso esperando você.</li>}
      </ul>
    </nav>
  );
}
