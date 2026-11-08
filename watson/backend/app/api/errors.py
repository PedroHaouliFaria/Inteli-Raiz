"""Envelope de erro e handlers globais (§2 do contrato)."""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class ApiError(Exception):
    """Erro de negócio com código, mensagem e detalhes opcionais."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: dict | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


def _error_body(code: str, message: str, details: dict | None = None) -> dict:
    payload: dict = {"code": code, "message": message}
    if details is not None:
        payload["details"] = details
    return {"error": payload}


def add_error_handlers(app: FastAPI) -> None:
    """Registra todos os handlers de erro no envelope padrão do contrato."""

    @app.exception_handler(ApiError)
    async def api_error_handler(request: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        if exc.status_code == 404:
            return JSONResponse(
                status_code=404,
                content=_error_body("NOT_FOUND", "O recurso solicitado não foi encontrado."),
            )
        # Outros HTTPException: repassa o status e usa um code genérico
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body("HTTP_ERROR", str(exc.detail)),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # exc.errors() pode trazer o objeto da exceção em "ctx.error" quando um
        # validador customizado levanta ValueError — isso quebra o JSON.
        # Devolver só loc, msg e type é suficiente para o front (§2 do contrato).
        safe_errors = [
            {"loc": list(e.get("loc", [])), "msg": e.get("msg", ""), "type": e.get("type", "")}
            for e in exc.errors()
        ]
        return JSONResponse(
            status_code=400,
            content=_error_body(
                "INVALID_REQUEST",
                "Dados inválidos. Verifique os campos enviados.",
                {"validation_errors": safe_errors},
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Erro não tratado: %s %s", request.method, request.url)
        return JSONResponse(
            status_code=500,
            content=_error_body(
                "INTERNAL_ERROR",
                "Ocorreu um erro interno. Tente novamente em instantes.",
            ),
        )
