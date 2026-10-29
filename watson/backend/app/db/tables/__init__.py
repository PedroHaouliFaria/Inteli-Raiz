"""Tabelas SQLAlchemy nos três blocos do modelo de dados: source, risk e analysis."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Importa todas as tabelas para que o Alembic as detecte automaticamente
from app.db.tables.purchases import Purchase, Confirmation, Review, Event, IdempotencyKey  # noqa: E402, F401
