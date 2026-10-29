"""Endpoints de demonstração (§9 do contrato).

POST /api/demo/purchases  — cria compra nova a partir de uma fixture para a sessão
POST /api/demo/reset      — apaga tudo e reinicia o seed

Registrados só com DEMO_MODE=true (verificado em main.py).
"""
from __future__ import annotations

import json
import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.api.deps import AssociadoUser, CurrentUser
from app.api.errors import ApiError
from app.api.schemas.common import _serialize_utc
from app.api.schemas.purchases import PurchaseDetailResponse
from app.db.repositories.purchases import PurchaseRepository
from app.db.session import get_session
from app.db.tables.purchases import (
    ChatMessage,
    Confirmation,
    Event,
    IdempotencyKey,
    Purchase,
    Review,
)
from app.domain.cases.intake import receive_and_evaluate_purchase
from app.domain.cases.purchases import build_purchase_detail

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/demo", tags=["demo"])


def _load_fixtures() -> dict[str, dict]:
    """Carrega purchases.json e retorna dict fixture_id → fixture."""
    import pathlib
    # demo.py → routes → api → app → backend; fixtures está em app/fixtures/
    fixtures_path = pathlib.Path(__file__).resolve().parents[2] / "fixtures" / "purchases.json"
    with open(fixtures_path, encoding="utf-8") as fh:
        items = json.load(fh)
    return {item["fixture_id"]: item for item in items}


def _detail_to_json_safe(data: dict) -> dict:
    """Converte datetimes do dict de detalhe para strings ISO 8601 UTC."""
    from datetime import datetime

    def _convert(obj):
        if isinstance(obj, datetime):
            return _serialize_utc(obj)
        if isinstance(obj, dict):
            return {k: _convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_convert(i) for i in obj]
        return obj

    return _convert(data)


# ---------------------------------------------------------------------------
# POST /api/demo/purchases
# ---------------------------------------------------------------------------

@router.post("/purchases", status_code=201)
def demo_create_purchase(
    body: dict,
    persona: AssociadoUser,
    session: Session = Depends(get_session),
):
    """Cria uma compra nova para a sessão a partir de uma fixture (§9).

    - 201 com corpo igual a GET /api/purchases/{case_id}
    - Se o modelo falhar: REVISAO_PENDENTE + warning: SCORE_UNAVAILABLE
    - fixture_id desconhecido: 400 INVALID_REQUEST
    - Score inventado nunca.
    """
    fixture_id = body.get("fixture_id", "")
    fixtures = _load_fixtures()
    fixture = fixtures.get(fixture_id)
    if fixture is None:
        raise ApiError(400, "INVALID_REQUEST", f"fixture_id desconhecido: {fixture_id!r}")

    from app.config import get_settings
    settings = get_settings()

    purchase, confirmation, score_failed = receive_and_evaluate_purchase(
        session=session,
        fixture=fixture,
        customer_id=persona.customer_id,
        ttl_seconds=settings.confirmation_ttl_seconds,
        model_path=settings.risk_model_path,
        is_seed=False,
    )
    session.commit()
    session.refresh(purchase)
    if confirmation is not None:
        session.refresh(confirmation)
    # Recarrega relações
    session.expire(purchase)
    purchase = session.get(Purchase, purchase.id)

    detail = build_purchase_detail(purchase, confirmation, session=None)
    detail["simulation"] = True
    detail_safe = _detail_to_json_safe(detail)

    if score_failed:
        detail_safe["warning"] = "SCORE_UNAVAILABLE"

    return JSONResponse(content=detail_safe, status_code=201)


# ---------------------------------------------------------------------------
# POST /api/demo/reset
# ---------------------------------------------------------------------------

@router.post("/reset", status_code=204)
def demo_reset(
    current: CurrentUser,
    session: Session = Depends(get_session),
):
    """Apaga todas as compras, confirmações, revisões, análises, eventos,
    chaves de idempotência, conversas e roda o seed de novo. 204.

    Qualquer papel pode chamar (só precisa de sessão).
    """
    # Apaga em ordem que respeita FK (filhos antes dos pais)
    session.execute(delete(ChatMessage))
    session.execute(delete(IdempotencyKey))
    session.execute(delete(Event))
    session.execute(delete(Review))
    session.execute(delete(Confirmation))
    session.execute(delete(Purchase))
    session.commit()

    # Relança o seed
    from app.config import get_settings
    settings = get_settings()
    from app.db.seed import run_seed
    run_seed(session, ttl_seconds=settings.confirmation_ttl_seconds)

    return Response(status_code=204)
