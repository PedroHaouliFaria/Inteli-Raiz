from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.errors import add_error_handlers
from app.api.routes import health, model_lab, purchases, session
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Executa o seed na inicialização se o banco estiver vazio.

    Usa o get_engine() compartilhado pelo resto da aplicação (não cria engine próprio).
    Qualquer falha no seed derruba a subida — banco sem dados é pior que app que não sobe.
    """
    from sqlalchemy.orm import sessionmaker
    from app.db.session import get_engine
    from app.db.tables import Base
    from app.db.seed import run_seed

    settings = get_settings()
    engine = get_engine()
    # Cria as tabelas se ainda não existirem (para dev/teste sem Alembic)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        run_seed(session, ttl_seconds=settings.confirmation_ttl_seconds)
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
    # Cookie de sessão com timestamp (§4); SESSION_SECRET é obrigatório no config
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.session_secret,
        session_cookie="raiz_session",
        same_site="lax",
        https_only=settings.session_secure,
        max_age=int(8 * 3600),  # 8 horas
    )
    add_error_handlers(app)
    app.include_router(health.router)
    app.include_router(model_lab.router)
    app.include_router(session.router)
    app.include_router(purchases.router)
    return app


app = create_app()
