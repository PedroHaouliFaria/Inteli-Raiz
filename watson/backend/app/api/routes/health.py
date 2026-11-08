from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.schemas.health import HealthResponse
from app.agents.providers import get_agent_provider
from app.db.session import get_session

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(session: Session = Depends(get_session)) -> HealthResponse:
    session.execute(select(1))  # cada dialeto gera o SELECT certo (no Db2, FROM SYSIBM.SYSDUMMY1)
    return HealthResponse(
        status="ok",
        database=session.bind.dialect.name,
        agent_provider=get_agent_provider().name,
    )
