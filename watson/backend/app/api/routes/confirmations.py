"""Rota POST /api/confirmations/{challenge_id}/response (§6 do contrato)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.api.deps import AssociadoUser
from app.api.errors import ApiError
from app.api.schemas.confirmations import ConfirmationResponseIn, ConfirmationResponseOut
from app.db.repositories.confirmations import ConfirmationRepository
from app.db.session import get_write_session

router = APIRouter(prefix="/api/confirmations", tags=["confirmations"])


@router.post("/{challenge_id}/response", response_model=ConfirmationResponseOut)
def post_confirmation_response(
    challenge_id: str,
    body: ConfirmationResponseIn,
    persona: AssociadoUser,
    session: Session = Depends(get_write_session),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> ConfirmationResponseOut:
    """Registra a resposta do associado à confirmação (§6).

    Apenas ASSOCIADO pode chamar. O agente não tem ferramenta para isso (§4 do plano).
    """
    if idempotency_key is None:
        raise ApiError(
            428,
            "IDEMPOTENCY_KEY_REQUIRED",
            "É necessário enviar o cabeçalho Idempotency-Key nesta requisição.",
        )

    repo = ConfirmationRepository(session)
    result = repo.respond(
        customer_id=persona.customer_id,
        challenge_id=challenge_id,
        response=body.response,
        version=body.version,
        idempotency_key=idempotency_key,
    )
    return ConfirmationResponseOut(**result, simulation=True)
