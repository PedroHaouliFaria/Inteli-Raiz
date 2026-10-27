import { Tag } from '@carbon/react';
import { TRANSACTION_STATUS, formatBRL } from '../../mocks/cases';
import Term from '../../components/Term';

const formatWhen = (iso) => {
  const [date, time] = iso.split('T');
  const [, month, day] = date.split('-');
  return { date: `${day}/${month}`, time };
};

// Rajada como indicador (docs/dados/linha-do-tempo.md): o case traz só o contador, não as compras.
export function BurstIndicator({ velocity1h }) {
  if (velocity1h == null) return null;
  const strong = velocity1h >= 10;
  return (
    <div className={`watson-burst${strong ? ' watson-burst--strong' : ''}`}>
      <p className="watson-burst__value">{velocity1h}</p>
      <div>
        <p className="cds--type-body-compact-01">tentativas deste cartão no terminal na última hora</p>
        <p className="cds--type-helper-text-01"><Term id="burst">Rajada</Term> · fonte: contador do case (<code>cp_card_term_vel_1h</code>)</p>
      </div>
    </div>
  );
}

// Compras do cartão em ordem de horário. Tentativas simuladas levam o selo "Simulada".
export default function CardTimeline({ history }) {
  if (!history?.length) return null;
  const sorted = [...history].sort((a, b) => a.occurredAt.localeCompare(b.occurredAt));
  const firstReal = sorted.find((t) => !t.simulated);
  const hasSimulated = sorted.some((t) => t.simulated);
  return (
    <div className="watson-card-timeline">
      <h3 className="cds--type-heading-compact-01">Compras do cartão</h3>
      {hasSimulated && (
        <p className="cds--type-helper-text-01">
          Inclui <Term id="simulatedAttempt">tentativas simuladas</Term>, geradas para a demonstração a partir do contador. Elas não têm score nem viram alerta.
        </p>
      )}
      <ol className="watson-timeline">
        {sorted.map((t) => {
          const when = formatWhen(t.occurredAt);
          const status = TRANSACTION_STATUS[t.status];
          return (
            <li key={t.id} className={t.simulated ? 'watson-timeline__item--simulated' : t.current ? 'watson-timeline__item--current' : undefined}>
              <span className="watson-timeline__time">{when.date}<br />{when.time}</span>
              <div>
                <p className="cds--type-heading-compact-01">{formatBRL(t.amount)} · {t.merchant}</p>
                <p className="cds--type-helper-text-01">{t.city} · {t.channel}</p>
                <div className="watson-timeline__tags">
                  {t.simulated && <Tag type="outline" size="sm">Simulada</Tag>}
                  {t.current && <Tag type="blue" size="sm">Compra em análise</Tag>}
                  {t === firstReal && !t.simulated && <Tag type="purple" size="sm">Primeira compra deste cartão</Tag>}
                  {status && <Tag type={status.tagType} size="sm">{status.label}</Tag>}
                </div>
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
