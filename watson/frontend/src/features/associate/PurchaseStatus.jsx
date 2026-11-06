import {
  CheckmarkFilled,
  CloseFilled,
  InformationFilled,
  Time,
  WarningFilled,
} from '@carbon/icons-react';
import { statusMeta } from './utils.js';

const ICONS = {
  check: CheckmarkFilled,
  close: CloseFilled,
  info: InformationFilled,
  time: Time,
  warning: WarningFilled,
};

export function PurchaseStatusBadge({ status, label }) {
  const meta = statusMeta(status);
  const Icon = ICONS[meta.icon] ?? InformationFilled;

  return (
    <span
      className={`purchase-status-badge purchase-status-badge--${meta.tone}`}
      aria-label={label}
      title={label}
    >
      <Icon size={14} aria-hidden />
      <span>{meta.shortLabel ?? label}</span>
    </span>
  );
}

export function PurchaseStatusPanel({ status, label, aside }) {
  const meta = statusMeta(status);
  const Icon = ICONS[meta.icon] ?? InformationFilled;

  return (
    <section
      className={`purchase-status-panel purchase-status-panel--${meta.tone}`}
      aria-labelledby="purchase-current-status"
    >
      <div className="purchase-status-panel__icon" aria-hidden>
        <Icon size={24} />
      </div>
      <div className="purchase-status-panel__content">
        <p className="cds--type-label-01 purchase-status-panel__eyebrow">Status atual</p>
        <h2 id="purchase-current-status" className="cds--type-heading-compact-02">
          {label}
        </h2>
        <p className="cds--type-body-compact-01 purchase-status-panel__description">
          {meta.description}
        </p>
        {meta.nextStep && (
          <p className="cds--type-label-01 purchase-status-panel__next-step">
            Próximo passo: <strong>{meta.nextStep}</strong>
          </p>
        )}
      </div>
      {aside && <div className="purchase-status-panel__aside">{aside}</div>}
    </section>
  );
}
