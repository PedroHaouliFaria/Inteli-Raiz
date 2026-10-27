"""Tabelas SQLAlchemy nos três blocos do modelo de dados: source, risk e analysis."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
