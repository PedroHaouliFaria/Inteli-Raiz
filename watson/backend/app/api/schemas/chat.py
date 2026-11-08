"""Esquemas do chat (§7 do contrato)."""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.api.schemas.common import SimulationTrue, UtcDatetime


class ChatMessageOut(BaseModel):
    """Mensagem do chat (user ou assistant)."""
    model_config = {"extra": "forbid"}

    message_id: str
    role: str
    content: str
    created_at: UtcDatetime
    tools_used: list[str] = Field(default_factory=list)


class ChatHistoryResponse(BaseModel):
    """GET /api/purchases/{case_id}/chat."""
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "case_id": "T-007",
                "messages": [
                    {
                        "message_id": "M-1",
                        "role": "assistant",
                        "content": "Olá, Ana. Posso explicar por que pedimos sua confirmação ou tirar dúvidas sobre esta compra. Para autorizar ou recusar, use os botões da tela.",
                        "created_at": "2026-10-28T03:12:05Z",
                        "tools_used": [],
                    }
                ],
                "agent_available": True,
                "simulation": True,
            }
        },
    }

    case_id: str
    messages: list[ChatMessageOut]
    agent_available: bool
    simulation: SimulationTrue


class ChatRequest(BaseModel):
    """Corpo do POST /api/purchases/{case_id}/chat."""
    model_config = {"extra": "forbid"}

    message: str = Field(..., min_length=1, max_length=1000)


class ChatReplyMessageOut(BaseModel):
    """Mensagem de resposta do assistente."""
    model_config = {"extra": "forbid"}

    message_id: str
    role: str
    content: str
    created_at: UtcDatetime
    tools_used: list[str] = Field(default_factory=list)


class ChatUserMessageOut(BaseModel):
    """Mensagem do usuário (sem tools_used)."""
    model_config = {"extra": "forbid"}

    message_id: str
    role: str
    content: str
    created_at: UtcDatetime


class ChatPostResponse(BaseModel):
    """POST /api/purchases/{case_id}/chat — 200."""
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "case_id": "T-007",
                "user_message": {
                    "message_id": "M-2",
                    "role": "user",
                    "content": "Pode ser o nome da empresa que aparece na fatura?",
                    "created_at": "2026-10-28T03:13:10Z",
                },
                "reply": {
                    "message_id": "M-3",
                    "role": "assistant",
                    "content": "Não consigo confirmar isso.",
                    "created_at": "2026-10-28T03:13:14Z",
                    "tools_used": ["consultar_compra"],
                },
                "review_protocol": None,
                "simulation": True,
            }
        },
    }

    case_id: str
    user_message: ChatUserMessageOut
    reply: ChatReplyMessageOut
    review_protocol: str | None = None
    simulation: SimulationTrue
