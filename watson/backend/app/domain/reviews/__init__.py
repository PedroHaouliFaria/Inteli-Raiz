"""Serviço de domínio para revisões (§8 do contrato).

Um único serviço que tanto a rota do associado quanto a ferramenta do agente usam.
Criado em app/domain/reviews para separar da lógica de compras.
"""
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.tables.purchases import Purchase, Review


def _now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _next_review_id(session: Session) -> str:
    count = session.execute(select(func.count()).select_from(Review)).scalar() or 0
    return f"REV-{count + 1}"


def _next_protocol(session: Session) -> str:
    today = datetime.now(UTC).strftime("%Y%m%d")
    count = session.execute(select(func.count()).select_from(Review)).scalar() or 0
    return f"RZ-{today}-{count + 1:04d}"


_VALID_REASONS = {"NAO_RECONHECE_ESTABELECIMENTO", "VALOR_DIFERENTE", "DUVIDA_PROCESSO", "OUTRO"}

# Rótulo de status (§3)
_STATUS_LABELS: dict[str, str] = {
    "RECEBIDA": "Compra recebida",
    "EM_AVALIACAO": "Em avaliação",
    "AGUARDANDO_ASSOCIADO": "Aguardando sua resposta",
    "LIBERADA_SIMULACAO": "Compra liberada (simulação)",
    "RECUSADA_SIMULACAO": "Compra recusada (simulação)",
    "REVISAO_PENDENTE": "Em revisão por um analista",
    "CONFIRMACAO_EXPIRADA": "Prazo encerrado, compra não autorizada",
}


def create_or_get_review(
    *,
    session: Session,
    purchase: Purchase,
    reason: str,
    details: str | None,
    created_by: str,  # ASSOCIADO | AGENTE | SISTEMA
) -> tuple[dict, int]:
    """Cria uma revisão ou retorna a existente se já há uma ABERTA.

    Retorna (review_dict, http_status) onde http_status é 201 (nova) ou 200 (existente).
    Não muda o status da compra (§3: revisão não muda o estado sozinha).
    """
    from app.api.errors import ApiError

    if reason not in _VALID_REASONS:
        raise ApiError(400, "INVALID_REQUEST", f"reason inválido: {reason!r}")

    # Verifica se já há revisão aberta
    existing = _get_open_review(session, purchase)
    if existing is not None:
        return _build_review_dict(existing, purchase), 200

    now = _now()
    review = Review(
        review_id=_next_review_id(session),
        purchase_id=purchase.id,
        protocol=_next_protocol(session),
        kind="DUVIDA",
        reason=reason,
        status="ABERTA",
        created_by=created_by,
        details=details,
        created_at=now,
    )
    session.add(review)
    session.commit()
    session.refresh(review)
    return _build_review_dict(review, purchase), 201


def _get_open_review(session: Session, purchase: Purchase) -> Review | None:
    for rev in purchase.reviews:
        if rev.status == "ABERTA":
            return rev
    return None


def _build_review_dict(review: Review, purchase: Purchase) -> dict:
    """Monta o dict de resposta do POST /api/purchases/{case_id}/review (§8)."""
    return {
        "review_id": review.review_id,
        "protocol": review.protocol,
        "case_id": purchase.case_id,
        "kind": review.kind,
        "reason": review.reason,
        "status": review.status,
        "created_at": review.created_at,
        "created_by": review.created_by,
        "case_status": purchase.status,
        "message": (
            "Um analista vai olhar esta compra. "
            "Enquanto isso, você ainda pode responder se reconhece a compra."
        ),
    }
