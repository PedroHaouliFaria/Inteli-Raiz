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


_STATUS_BY_ANALYST_DECISION = {
    "AUTHORIZE": "LIBERADA_SIMULACAO",
    "DENY": "RECUSADA_SIMULACAO",
}


def resolve_review(
    *,
    session: Session,
    review_id: str,
    decision: str,
    analyst_id: str,
) -> dict:
    """Fecha uma revisão e aplica a decisão simulada da analista atomicamente."""
    from app.api.errors import ApiError
    from app.db.tables.purchases import Event

    if decision not in _STATUS_BY_ANALYST_DECISION:
        raise ApiError(400, "INVALID_REQUEST", f"decision inválida: {decision!r}")

    review = session.execute(
        select(Review).where(Review.review_id == review_id).with_for_update()
    ).scalar_one_or_none()
    if review is None:
        raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")
    if review.status != "ABERTA":
        raise ApiError(
            409,
            "REVIEW_ALREADY_CLOSED",
            "Esta revisão já foi encerrada. Atualize a fila.",
            {"review_id": review_id},
        )

    purchase = session.get(Purchase, review.purchase_id)
    if purchase is None:
        raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")

    now = _now()
    from_status = purchase.status
    new_status = _STATUS_BY_ANALYST_DECISION[decision]

    purchase.status = new_status
    purchase.version += 1
    purchase.updated_at = now
    # Uma decisão encerra toda revisão aberta da mesma compra para não deixar
    # pendências órfãs na fila.
    for pending in purchase.reviews:
        if pending.status == "ABERTA":
            pending.status = "FECHADA"

    session.add(
        Event(
            purchase_id=purchase.id,
            event_type="ANALYST_DECISION",
            from_status=from_status,
            to_status=new_status,
            payload={
                "review_id": review.review_id,
                "decision": decision,
                "analyst_id": analyst_id,
            },
            created_at=now,
        )
    )
    session.commit()

    action = "liberada" if decision == "AUTHORIZE" else "recusada"
    return {
        "review_id": review.review_id,
        "case_id": purchase.case_id,
        "decision": decision,
        "review_status": "FECHADA",
        "case_status": new_status,
        "message": f"Compra {action} na simulação e revisão encerrada.",
    }
