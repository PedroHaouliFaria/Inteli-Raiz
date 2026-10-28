"""Tabelas SQLAlchemy para o fluxo de confirmação de compras (§3, §5 e §6)."""
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.tables import Base
from app.db.types import PortableJSON


class Purchase(Base):
    """Compra recebida para confirmação.

    - case_id: "T-007"
    - customer_id: ID interno do cliente (C-ANA, C-BRUNO); nunca exposto ao associado
    - amount_cents: valor em centavos inteiros
    - card_last4: últimos 4 dígitos do card_id sintético
    - features_json: as 28 features do CSV como texto
    - version: incrementa a cada transição de estado
    """

    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    customer_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fixture_id: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="AGUARDANDO_ASSOCIADO")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Dados da compra
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="BRL")
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    mcc: Mapped[str] = mapped_column(String(10), nullable=False)
    card_brand: Mapped[str] = mapped_column(String(30), nullable=False)
    card_type: Mapped[str] = mapped_column(String(20), nullable=False)
    card_last4: Mapped[str] = mapped_column(String(4), nullable=False)
    channel: Mapped[str] = mapped_column(String(30), nullable=False)

    # Features como dict (texto no SQLite, JSON no Postgres)
    features_json: Mapped[dict] = mapped_column(PortableJSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
    )

    confirmations: Mapped[list["Confirmation"]] = relationship(
        "Confirmation", back_populates="purchase", cascade="all, delete-orphan"
    )
    events: Mapped[list["Event"]] = relationship(
        "Event", back_populates="purchase", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="purchase", cascade="all, delete-orphan"
    )


class Confirmation(Base):
    """Desafio de confirmação enviado ao associado."""

    __tablename__ = "confirmations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    challenge_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"), nullable=False, index=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    answered_response: Mapped[str | None] = mapped_column(String(20), nullable=True)
    answered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), nullable=True)

    purchase: Mapped["Purchase"] = relationship("Purchase", back_populates="confirmations")


class Review(Base):
    """Pedido de revisão humana (§8)."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    review_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"), nullable=False, index=True)
    protocol: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    kind: Mapped[str] = mapped_column(String(20), nullable=False)  # DUVIDA, PROTECAO, FALHA_AVALIACAO
    reason: Mapped[str] = mapped_column(String(50), nullable=False, default="OUTRO")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ABERTA")
    created_by: Mapped[str] = mapped_column(String(20), nullable=False)  # ASSOCIADO, AGENTE, SISTEMA
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

    purchase: Mapped["Purchase"] = relationship("Purchase", back_populates="reviews")


class Event(Base):
    """Registro de auditoria imutável de cada transição ou ação."""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(40), nullable=False)  # SEED, ANSWER, EXPIRE, ...
    payload: Mapped[dict | None] = mapped_column(PortableJSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

    purchase: Mapped["Purchase"] = relationship("Purchase", back_populates="events")
