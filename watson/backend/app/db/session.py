from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


@lru_cache
def get_engine() -> Engine:
    url = get_settings().database_url
    engine = create_engine(url, pool_pre_ping=True)
    # Para SQLite: ativa WAL mode e usa BEGIN IMMEDIATE para serializar escritas.
    # BEGIN IMMEDIATE adquire reserva na abertura, impedindo que duas transações
    # concorrentes leiam o mesmo estado e gravem dois eventos (§6, R06).
    if url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _set_sqlite_wal(conn, _rec):
            conn.execute("PRAGMA journal_mode=WAL")

        @event.listens_for(engine, "begin")
        def _do_begin_immediate(conn):
            conn.exec_driver_sql("BEGIN IMMEDIATE")

    return engine


def get_session() -> Iterator[Session]:
    session = sessionmaker(bind=get_engine())()
    try:
        yield session
    finally:
        session.close()


# Alias mantido para compatibilidade — com BEGIN IMMEDIATE no engine, toda sessão
# já é serializada; não há necessidade de uma sessão especial separada.
get_write_session = get_session
