/**
 * PurchaseList — lista as compras reais do associado vinda da API.
 *
 * Props:
 *   purchases     — array de PurchaseListItem (§5 do contrato)
 *   selectedId    — case_id selecionado atualmente
 *   onSelect(id)  — callback ao clicar em uma compra
 */
import { Tag } from '@carbon/react';
import { formatDate, formatMoney, statusMeta } from './utils.js';

export default function PurchaseList({ purchases, selectedId, onSelect }) {
  if (purchases.length === 0) {
    return (
      <p className="cds--type-body-01 associate-list__empty" role="status">
        Nenhuma compra encontrada para esta sessão.
      </p>
    );
  }

  return (
    <ul className="associate-list" aria-label="Suas compras">
      {purchases.map((p) => {
        const meta = statusMeta(p.status);
        const isSelected = p.case_id === selectedId;
        return (
          <li key={p.case_id} className={`associate-list__item${isSelected ? ' associate-list__item--active' : ''}`}>
            <button
              type="button"
              onClick={() => onSelect(p.case_id)}
              aria-current={isSelected ? 'true' : undefined}
              aria-label={`${p.merchant_display}, ${formatMoney(p.amount)}, ${p.status_label}`}
            >
              <div className="associate-list__main">
                <span className="cds--type-body-compact-02 associate-list__merchant">{p.merchant_display}</span>
                <span className="cds--type-heading-compact-01 associate-list__amount">{formatMoney(p.amount)}</span>
              </div>
              <div className="associate-list__meta">
                <span className="cds--type-label-01 associate-list__date">{formatDate(p.occurred_at)}</span>
                <Tag size="sm" type={meta.tagType}>{p.status_label}</Tag>
              </div>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
