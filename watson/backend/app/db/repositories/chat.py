"""Repositório de mensagens do chat (§7 e §10 do contrato)."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.tables.purchases import ChatMessage, Purchase


def _now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _next_message_id(session: Session) -> str:
    count = session.execute(select(func.count()).select_from(ChatMessage)).scalar() or 0
    return f"M-{count + 1}"


class ChatRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_messages(self, purchase: Purchase) -> list[ChatMessage]:
        """Todas as mensagens da compra, em ordem cronológica."""
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.purchase_id == purchase.id)
            .order_by(ChatMessage.id)
        )
        return list(self._session.execute(stmt).scalars().all())

    def save_message(
        self,
        *,
        purchase: Purchase,
        role: str,
        content: str,
        tools_used: list[str] | None = None,
    ) -> ChatMessage:
        """Grava uma mensagem e retorna o objeto salvo."""
        now = _now()
        msg = ChatMessage(
            message_id=_next_message_id(self._session),
            purchase_id=purchase.id,
            role=role,
            content=content,
            tools_used_json=tools_used or [],
            created_at=now,
        )
        self._session.add(msg)
        self._session.flush()
        return msg

    def count_recent(self, purchase: Purchase, window_seconds: int) -> int:
        """Conta mensagens do usuário nos últimos window_seconds."""
        cutoff = _now() - timedelta(seconds=window_seconds)
        stmt = (
            select(func.count())
            .select_from(ChatMessage)
            .where(
                ChatMessage.purchase_id == purchase.id,
                ChatMessage.role == "user",
                ChatMessage.created_at >= cutoff,
            )
        )
        return self._session.execute(stmt).scalar() or 0
