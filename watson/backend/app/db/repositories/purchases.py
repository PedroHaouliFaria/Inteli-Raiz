"""Repositório de compras — única camada que fala SQLAlchemy (§4 da arquitetura)."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.tables.purchases import Confirmation, Purchase


class PurchaseRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_owner(self, customer_id: str) -> list[tuple[Purchase, Confirmation | None]]:
        """Compras do associado ordenadas da mais recente para a mais antiga."""
        stmt = (
            select(Purchase)
            .where(Purchase.customer_id == customer_id)
            .order_by(Purchase.occurred_at.desc())
        )
        purchases = self._session.execute(stmt).scalars().all()
        result = []
        for p in purchases:
            conf = self._get_confirmation(p)
            result.append((p, conf))
        return result

    def get_by_owner(self, customer_id: str, case_id: str) -> tuple[Purchase, Confirmation | None] | None:
        """Retorna (purchase, confirmation) se o dono bate; None se não existe ou é de outra pessoa."""
        stmt = select(Purchase).where(Purchase.case_id == case_id)
        purchase = self._session.execute(stmt).scalar_one_or_none()
        if purchase is None or purchase.customer_id != customer_id:
            return None
        conf = self._get_confirmation(purchase)
        return purchase, conf

    def _get_confirmation(self, purchase: Purchase) -> Confirmation | None:
        stmt = select(Confirmation).where(Confirmation.purchase_id == purchase.id)
        return self._session.execute(stmt).scalar_one_or_none()
