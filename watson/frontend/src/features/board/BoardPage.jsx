import { useNavigate } from 'react-router-dom';
import { Tile, Tag, Button } from '@carbon/react';
import { STATUS_LABELS, riskLevel, formatBRL } from '../../mocks/cases';
import { useWatson } from '../../state/store';
import Term from '../../components/Term';
import WatsonRail from '../../components/WatsonRail';

export default function BoardPage({ phoneSlot }) {
  const navigate = useNavigate();
  const { state, dispatch } = useWatson();
  const stalled = state.cases.filter((c) => c.status === 'awaiting_member' && parseInt(c.waitTime, 10) > 20).map((c) => c.id);
  return (
    <div className="watson-layout">
      <main className="watson-main" id="main-content">
        <h1 className="cds--type-heading-04">Quadro do processo</h1>
        <div style={{ overflowX: 'auto' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(220px, 1fr))', gap: '1rem', minWidth: 940 }}>
            {Object.entries(STATUS_LABELS).map(([status, label]) => {
              const list = state.cases.filter((c) => c.status === status);
              return (
                <section key={status} aria-label={label} className="watson-column">
                  <h2 className="cds--type-heading-compact-01">
                    {status === 'awaiting_member' ? <Term id="awaitingMember">{label}</Term> : label} · {list.length}
                  </h2>
                  {list.map((c) => (
                    <Tile key={c.id}>
                      <p className="cds--type-label-01">
                        Caso #{c.id} · {c.alertCount} <Term id="alert">{c.alertCount > 1 ? 'alertas' : 'alerta'}</Term>
                      </p>
                      <p className="cds--type-heading-03">{formatBRL(c.amount)}</p>
                      <p className="cds--type-body-compact-01">{c.merchant}</p>
                      <div style={{ display: 'flex', gap: '0.25rem', margin: '0.5rem 0', flexWrap: 'wrap' }}>
                        <Tag type={riskLevel(c.score).tagType} size="sm">{riskLevel(c.score).label} · {c.score.toFixed(2).replace('.', ',')}</Tag>
                        <Tag type="outline" size="sm">{c.channel}</Tag>
                        {c.autoNotice && c.status === 'awaiting_member' && <Tag type="blue" size="sm">Aviso pelo Watson</Tag>}
                        {c.decision && <Tag type={c.decision === 'blocked' ? 'red' : 'green'} size="sm">{c.decision === 'blocked' ? 'Bloqueado' : 'Liberado'} por {c.by}</Tag>}
                      </div>
                      <div style={{ display: 'flex', gap: '0.25rem', flexWrap: 'wrap' }}>
                        <Button kind="ghost" size="sm" onClick={() => navigate(`/cases/${c.id}`)}>Abrir caso</Button>
                        {c.id === '5107' && !c.ungrouped && (
                          <Button kind="ghost" size="sm" onClick={() => dispatch({ type: 'ungroup', caseId: c.id })}>Desagrupar</Button>
                        )}
                      </div>
                    </Tile>
                  ))}
                </section>
              );
            })}
          </div>
        </div>
      </main>
      <WatsonRail
        title="Gargalo"
        suggestion={stalled.length ? `${stalled.length} casos aguardam o associado há mais de 20 min. Sugiro reenviar o aviso de compra.` : 'Nenhum caso parado.'}
        reason="sem resposta, a compra segue pausada e o associado pode ser barrado no balcão."
        actionLabel={stalled.length ? `Reenviar aviso aos ${stalled.length}` : null}
        onAccept={() => dispatch({ type: 'resendNotices', ids: stalled })}
        chips={['Quais casos estão parados?']}
      />
      {phoneSlot}
    </div>
  );
}
