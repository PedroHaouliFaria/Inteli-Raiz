import { Tag, Tile } from '@carbon/react';
import { ChartLineData, Currency, Purchase, UserMultiple } from '@carbon/icons-react';
import { formatMoney, statusMeta } from '../associate/utils.js';

const number = new Intl.NumberFormat('pt-BR');

function shortDate(value) {
  const [year, month, day] = value.split('-');
  return `${day}/${month}`;
}

function MetricCard({ icon: Icon, label, value, helper, tone = 'blue' }) {
  return (
    <Tile className={`analyst-dashboard-metric analyst-dashboard-metric--${tone}`}>
      <div className="analyst-dashboard-metric__top">
        <span className="cds--type-label-01">{label}</span>
        <Icon size={20} aria-hidden="true" />
      </div>
      <strong className="cds--type-heading-04">{value}</strong>
      <span className="cds--type-label-01 analyst-dashboard-metric__helper">{helper}</span>
    </Tile>
  );
}

function DailyVolumeChart({ items }) {
  const max = Math.max(...items.map((item) => Number(item.total_amount.value)), 1);
  return (
    <Tile className="analyst-dashboard-card analyst-dashboard-card--wide">
      <div className="analyst-dashboard-card__header">
        <div>
          <h2 className="cds--type-heading-compact-02">Volume financeiro por dia</h2>
          <p className="cds--type-label-01">Soma das compras registradas em cada data.</p>
        </div>
        <Tag type="blue" size="sm">{items.length} dias</Tag>
      </div>
      <div className="analyst-volume-chart" role="img" aria-label="Gráfico de barras do volume financeiro diário">
        {items.map((item) => {
          const height = Math.max((Number(item.total_amount.value) / max) * 100, 3);
          return (
            <div key={item.date} className="analyst-volume-chart__column">
              <span className="analyst-volume-chart__value cds--type-label-01">
                {formatMoney(item.total_amount)}
              </span>
              <div className="analyst-volume-chart__track">
                <div className="analyst-volume-chart__bar" style={{ height: `${height}%` }} />
              </div>
              <span className="cds--type-label-01">{shortDate(item.date)}</span>
              <span className="cds--type-helper-text-01">{item.transaction_count} tx.</span>
            </div>
          );
        })}
      </div>
    </Tile>
  );
}

function StatusChart({ items, total }) {
  const max = Math.max(...items.map((item) => item.transaction_count), 1);
  return (
    <Tile className="analyst-dashboard-card">
      <div className="analyst-dashboard-card__header">
        <div>
          <h2 className="cds--type-heading-compact-02">Distribuição por status</h2>
          <p className="cds--type-label-01">Situação atual das compras.</p>
        </div>
      </div>
      <div className="analyst-status-chart">
        {items.map((item, index) => (
          <div key={item.status} className="analyst-status-chart__row">
            <div className="analyst-status-chart__label">
              <span className="cds--type-body-compact-01">{statusMeta(item.status).shortLabel}</span>
              <strong className="cds--type-label-01">
                {item.transaction_count} · {Math.round((item.transaction_count / total) * 100)}%
              </strong>
            </div>
            <div className="analyst-status-chart__track">
              <div
                className={`analyst-status-chart__bar analyst-status-chart__bar--${(index % 4) + 1}`}
                style={{ width: `${(item.transaction_count / max) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </Tile>
  );
}

function ReviewChart({ open, closed, total }) {
  const openPercentage = total ? Math.round((open / total) * 100) : 0;
  return (
    <Tile className="analyst-dashboard-card">
      <div className="analyst-dashboard-card__header">
        <div>
          <h2 className="cds--type-heading-compact-02">Demandas de revisão</h2>
          <p className="cds--type-label-01">Carga atual e histórico de decisões.</p>
        </div>
      </div>
      <div className="analyst-review-chart">
        <div
          className="analyst-review-chart__donut"
          style={{ '--review-open': `${openPercentage * 3.6}deg` }}
          role="img"
          aria-label={`${open} revisões abertas e ${closed} encerradas`}
        >
          <div>
            <strong className="cds--type-heading-04">{total}</strong>
            <span className="cds--type-label-01">revisões</span>
          </div>
        </div>
        <dl className="analyst-review-chart__legend">
          <div>
            <dt><span className="analyst-review-chart__dot analyst-review-chart__dot--open" /> Abertas</dt>
            <dd>{open}</dd>
          </div>
          <div>
            <dt><span className="analyst-review-chart__dot analyst-review-chart__dot--closed" /> Encerradas</dt>
            <dd>{closed}</dd>
          </div>
        </dl>
      </div>
    </Tile>
  );
}

function CustomerChart({ items }) {
  const max = Math.max(...items.map((item) => Number(item.total_amount.value)), 1);
  return (
    <Tile className="analyst-dashboard-card analyst-dashboard-card--wide">
      <div className="analyst-dashboard-card__header">
        <div>
          <h2 className="cds--type-heading-compact-02">Movimentação por associado</h2>
          <p className="cds--type-label-01">Volume, quantidade e ticket médio por cliente.</p>
        </div>
      </div>
      <div className="analyst-customer-chart">
        {items.map((item) => (
          <div key={item.customer_id} className="analyst-customer-chart__row">
            <div className="analyst-customer-chart__identity">
              <strong className="cds--type-body-compact-02">{item.display_name}</strong>
              <span className="cds--type-label-01">{item.transaction_count} transações</span>
            </div>
            <div className="analyst-customer-chart__visual">
              <div className="analyst-customer-chart__track">
                <div style={{ width: `${(Number(item.total_amount.value) / max) * 100}%` }} />
              </div>
            </div>
            <div className="analyst-customer-chart__amounts">
              <strong>{formatMoney(item.total_amount)}</strong>
              <span className="cds--type-label-01">Ticket {formatMoney(item.average_ticket)}</span>
            </div>
          </div>
        ))}
      </div>
    </Tile>
  );
}

export default function AnalystDashboard({ data }) {
  const reviewRate = data.transaction_count
    ? Math.round((data.review_count / data.transaction_count) * 100)
    : 0;
  return (
    <div className="analyst-dashboard">
      <section className="analyst-dashboard-metrics" aria-label="Indicadores gerais">
        <MetricCard icon={Currency} label="Volume financeiro" value={formatMoney(data.total_amount)} helper="Soma de todas as compras" tone="green" />
        <MetricCard icon={Purchase} label="Transações" value={number.format(data.transaction_count)} helper={`Ticket médio ${formatMoney(data.average_ticket)}`} />
        <MetricCard icon={UserMultiple} label="Associados" value={number.format(data.customer_count)} helper="Clientes na base demonstrativa" tone="purple" />
        <MetricCard icon={ChartLineData} label="Média por associado" value={formatMoney(data.average_amount_per_customer)} helper={`${reviewRate}% das compras geraram revisão`} tone="cyan" />
      </section>

      <section className="analyst-dashboard-grid" aria-label="Gráficos operacionais">
        <DailyVolumeChart items={data.daily_volume} />
        <StatusChart items={data.status_breakdown} total={data.transaction_count} />
        <ReviewChart open={data.open_review_count} closed={data.closed_review_count} total={data.review_count} />
        <CustomerChart items={data.customer_breakdown} />
      </section>
    </div>
  );
}
