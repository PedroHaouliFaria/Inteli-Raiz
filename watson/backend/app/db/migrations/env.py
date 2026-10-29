from logging.config import fileConfig

from alembic import context

from app.db.tables import Base  # noqa: F401 – importa todos os modelos

if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

target_metadata = Base.metadata


def _get_url() -> str:
    """Retorna a URL do banco: aceita override via `-x db_url=...` no CLI alembic."""
    # -x args ficam em context.config.attributes sob a chave cmd_opts.x (ou direto em attributes)
    x_args: dict = getattr(getattr(context.config, "cmd_opts", None), "x", None) or {}
    if isinstance(x_args, list):
        x_args = dict(kv.split("=", 1) for kv in x_args if "=" in kv)
    if x_args.get("db_url"):
        return x_args["db_url"]
    from app.db.session import get_engine
    return str(get_engine().url)


def run_migrations_offline() -> None:
    context.configure(url=_get_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine
    connectable = create_engine(_get_url())
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
