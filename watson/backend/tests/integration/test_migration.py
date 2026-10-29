"""Testa que alembic upgrade head num SQLite vazio cria as tabelas esperadas (Fix A)."""
import os
import tempfile

import pytest


def test_alembic_upgrade_creates_tables(tmp_path):
    """alembic upgrade head num banco vazio cria purchases, confirmations, reviews e events."""
    import subprocess
    import sys

    db_path = str(tmp_path / "test_migration.db")
    env = {**os.environ, "DATABASE_URL": f"sqlite:///{db_path}"}

    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        cwd=os.path.join(os.path.dirname(__file__), "..", ".."),
        env=env,
    )
    assert result.returncode == 0, f"alembic falhou:\n{result.stderr}"

    from sqlalchemy import create_engine, inspect

    engine = create_engine(f"sqlite:///{db_path}")
    tables = inspect(engine).get_table_names()
    engine.dispose()

    assert "purchases" in tables, f"Tabela purchases não criada. Tabelas: {tables}"
    assert "confirmations" in tables, f"Tabela confirmations não criada. Tabelas: {tables}"
    assert "reviews" in tables, f"Tabela reviews não criada. Tabelas: {tables}"
    assert "events" in tables, f"Tabela events não criada. Tabelas: {tables}"
