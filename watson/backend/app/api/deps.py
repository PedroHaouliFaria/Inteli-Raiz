"""Dependências de autenticação e autorização (§4 do contrato).

current_user  → 401 NOT_AUTHENTICATED se não há sessão válida
require_role  → 403 FORBIDDEN_ROLE se o papel não corresponde
"""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from app.api.errors import ApiError
from app.domain.personas import PERSONAS, Persona


def current_user(request: Request) -> Persona:
    """Lê o persona_id do cookie de sessão e devolve o Persona.

    Levanta 401 NOT_AUTHENTICATED se o cookie não existe, foi adulterado ou
    o persona_id não corresponde a nenhuma pessoa conhecida.
    """
    session = request.session
    persona_id = session.get("persona_id")
    if not persona_id:
        raise ApiError(
            status_code=401,
            code="NOT_AUTHENTICATED",
            message="Sessão não encontrada ou expirada. Faça login novamente.",
        )
    persona = PERSONAS.get(persona_id)
    if persona is None:
        # persona_id válido no cookie mas não reconhecido (ex.: cookie de versão antiga)
        raise ApiError(
            status_code=401,
            code="NOT_AUTHENTICATED",
            message="Sessão inválida. Faça login novamente.",
        )
    return persona


CurrentUser = Annotated[Persona, Depends(current_user)]


def require_associado(persona: CurrentUser) -> Persona:
    """Garante que o usuário da sessão tem papel ASSOCIADO."""
    if persona.role != "ASSOCIADO":
        raise ApiError(
            status_code=403,
            code="FORBIDDEN_ROLE",
            message="Esta operação é exclusiva para associados.",
        )
    return persona


def require_analista(persona: CurrentUser) -> Persona:
    """Garante que o usuário da sessão tem papel ANALISTA."""
    if persona.role != "ANALISTA":
        raise ApiError(
            status_code=403,
            code="FORBIDDEN_ROLE",
            message="Esta operação é exclusiva para analistas.",
        )
    return persona


AssociadoUser = Annotated[Persona, Depends(require_associado)]
AnalistaUser = Annotated[Persona, Depends(require_analista)]
