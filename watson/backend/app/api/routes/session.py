"""Endpoints de sessão (§4 do contrato).

GET  /api/session/personas   — público, lista as personas fictícias
POST /api/session             — login por e-mail/senha, grava cookie raiz_session
GET  /api/session             — retorna persona da sessão atual ou 401
DELETE /api/session           — logout, apaga o cookie
"""
from __future__ import annotations

import hmac
from datetime import timedelta

from fastapi import APIRouter, Request, Response

from app.api.errors import ApiError
from app.api.schemas.session import (
    PersonaItem,
    PersonaListResponse,
    SessionLoginRequest,
    SessionResponse,
)
from app.config import get_settings
from app.domain.personas import PERSONAS

router = APIRouter(prefix="/api/session", tags=["session"])

# Duração da sessão conforme o contrato: 8 horas
_SESSION_MAX_AGE = int(timedelta(hours=8).total_seconds())


def _persona_to_session_response(persona_id: str) -> SessionResponse:
    persona = PERSONAS[persona_id]
    return SessionResponse(
        persona_id=persona.persona_id,
        display_name=persona.display_name,
        role=persona.role,  # type: ignore[arg-type]
        simulation=True,
        demo_mode=get_settings().demo_mode,
    )


@router.get("/personas", response_model=PersonaListResponse)
def list_personas() -> PersonaListResponse:
    """Lista todas as personas fictícias disponíveis para login."""
    items = [
        PersonaItem(
            persona_id=p.persona_id,
            display_name=p.display_name,
            role=p.role,  # type: ignore[arg-type]
        )
        for p in PERSONAS.values()
    ]
    return PersonaListResponse(personas=items, simulation=True)


@router.post("", status_code=200)
def create_session(
    body: SessionLoginRequest,
    request: Request,
    response: Response,
) -> SessionResponse:
    """Valida e-mail/senha fictícios e define o cookie ``raiz_session``."""
    from app.config import get_settings

    settings = get_settings()
    persona = None

    # Compatibilidade opt-in usada apenas pela suíte de integração antiga.
    if body.persona_id is not None and settings.allow_legacy_persona_login:
        persona = PERSONAS.get(body.persona_id)
    elif body.email is not None and body.password is not None:
        credentials = {
            settings.mock_ana_email.strip().casefold(): ("ana", settings.mock_ana_password),
            settings.mock_bruno_email.strip().casefold(): ("bruno", settings.mock_bruno_password),
            settings.mock_carla_email.strip().casefold(): ("carla", settings.mock_carla_password),
        }
        matched = credentials.get(body.email.strip().casefold())
        expected_password = matched[1] if matched else "invalid-mock-password"
        password_matches = hmac.compare_digest(
            body.password.encode("utf-8"),
            expected_password.encode("utf-8"),
        )
        if matched and password_matches:
            persona = PERSONAS[matched[0]]

    if persona is None:
        raise ApiError(
            status_code=401,
            code="AUTHENTICATION_FAILED",
            message="E-mail ou senha inválidos.",
        )
    # Starlette SessionMiddleware grava no cookie ao set
    request.session["persona_id"] = persona.persona_id
    return _persona_to_session_response(persona.persona_id)


@router.get("", status_code=200)
def get_session(request: Request) -> SessionResponse:
    """Retorna os dados da sessão atual ou 401 se não há sessão."""
    persona_id = request.session.get("persona_id")
    if not persona_id or persona_id not in PERSONAS:
        raise ApiError(
            status_code=401,
            code="NOT_AUTHENTICATED",
            message="Sessão não encontrada. Faça login.",
        )
    return _persona_to_session_response(persona_id)


@router.delete("", status_code=204)
def delete_session(request: Request) -> None:
    """Encerra a sessão e apaga o cookie."""
    request.session.clear()
