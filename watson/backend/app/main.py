from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import add_error_handlers
from app.api.routes import health, model_lab
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Executa o seed na inicialização se o banco estiver vazio."""
    settings = get_settings()
    try:
        from sqlalchemy import create_engine, inspect
        from sqlalchemy.orm import sessionmaker
        from app.db.tables import Base
        from app.db.seed import run_seed

        engine = create_engine(settings.database_url, pool_pre_ping=True)
        # Cria as tabelas se ainda não existirem (para dev/teste sem Alembic)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        with Session() as session:
            run_seed(session, ttl_seconds=settings.confirmation_ttl_seconds)
    except Exception:
        import logging
        logging.getLogger(__name__).exception("Seed falhou na inicialização")
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Watson API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_error_handlers(app)
    app.include_router(health.router)
    app.include_router(model_lab.router)
    return app


app = create_app()
