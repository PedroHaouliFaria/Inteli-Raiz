/**
 * PurchaseList — grade responsiva das compras reais do associado vinda da API.
 *
 * Props:
 *   purchases     — array de PurchaseListItem (§5 do contrato)
 *   emptyMessage  — texto do estado vazio, inclusive quando há filtros ativos
 *   onSelect(id)  — callback ao clicar em uma compra
 */
import { ArrowUpRight } from '@carbon/icons-react';
import { formatDate, formatMoney } from './utils.js';
import { PurchaseStatusBadge } from './PurchaseStatus.jsx';

export default function PurchaseList({ purchases, onSelect, emptyMessage = 'Nenhuma compra encontrada.' }) {
  if (purchases.length === 0) {
    return (
      <p className="cds--type-body-01 associate-list__empty" role="status">
        {emptyMessage}
      </p>
    );
  }

  return (
    <ul className="associate-purchase-cards" aria-label="Suas compras">
      {purchases.map((p) => {
        return (
          <li key={p.case_id} className="associate-purchase-card">
            <button
              type="button"
              onClick={() => onSelect(p.case_id)}
              aria-label={`${p.merchant_display}, ${formatMoney(p.amount)}, ${p.status_label}`}
            >
              <div className="associate-purchase-card__top">
                <span className="cds--type-label-01 associate-purchase-card__case">Compra {p.case_id}</span>
                <ArrowUpRight size={20} aria-hidden className="associate-purchase-card__arrow" />
              </div>
              <div className="associate-purchase-card__body">
                <span className="cds--type-body-compact-02 associate-purchase-card__merchant">{p.merchant_display}</span>
                <strong className="cds--type-heading-04 associate-purchase-card__amount">{formatMoney(p.amount)}</strong>
              </div>
              <div className="associate-purchase-card__footer">
                <span className="cds--type-label-01 associate-purchase-card__date">{formatDate(p.occurred_at)}</span>
                <PurchaseStatusBadge status={p.status} label={p.status_label} />
              </div>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
