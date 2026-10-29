"""Repositório para o fluxo de resposta à confirmação (§6 do contrato).  # noqa

Toda a lógica de escrita fica aqui; a rota chama respond() e recebe um resultado
que pode serializar direto.

Concorrência: SQLite com isolation_level="SERIALIZABLE" (configurado no engine)
garante semântica de BEGIN IMMEDIATE — a primeira transação que tocar a linha
da confirmação vence; as outras esperam ou recebem OperationalError.
"""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.tables.purchases import Confirmation, Event, IdempotencyKey, Purchase, Review

# Mapeamento de resposta → status final (§6 do contrato)
_STATUS_BY_RESPONSE: dict[str, str] = {
    "AUTHORIZE": "LIBERADA_SIMULACAO",
    "DENY": "RECUSADA_SIMULACAO",
    "UNSURE": "REVISAO_PENDENTE",
}

# Rótulos dos botões (mesmo que _ALLOWED_RESPONSES em domain/cases/purchases.py)
_RESPONSE_LABELS: dict[str, str] = {
    "AUTHORIZE": "Reconheço e autorizo",
    "DENY": "Não reconheço",
    "UNSURE": "Estou em dúvida",
}

# Tipo de revisão aberta por resposta (§6)
_REVIEW_KIND_BY_RESPONSE: dict[str, str | None] = {
    "AUTHORIZE": None,
    "DENY": "PROTECAO",
    "UNSURE": "DUVIDA",
}


def _now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _body_hash(response: str, version: int) -> str:
    return hashlib.sha256(f"{response}:{version}".encode()).hexdigest()


class _DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            if obj.tzinfo is None:
                obj = obj.replace(tzinfo=timezone.utc)
            return obj.strftime("%Y-%m-%dT%H:%M:%SZ")
        return super().default(obj)


def _result_to_json(result_data: dict) -> str:
    """Serializa result_data para JSON, convertendo datetimes para ISO strings."""
    return json.dumps(result_data, cls=_DatetimeEncoder)


def _result_from_json(raw: str) -> dict:
    """Desserializa result_data, convertendo answered_at de volta para datetime."""
    data = json.loads(raw)
    if "answered_at" in data and isinstance(data["answered_at"], str):
        data["answered_at"] = datetime.fromisoformat(
            data["answered_at"].replace("Z", "+00:00")
        ).replace(tzinfo=None)
    return data


def _next_review_id(session: Session) -> str:
    from sqlalchemy import func
    count = session.execute(select(func.count()).select_from(Review)).scalar() or 0
    return f"REV-{count + 1}"


def _next_protocol(session: Session) -> str:
    from sqlalchemy import func
    today = datetime.now(UTC).strftime("%Y%m%d")
    count = session.execute(select(func.count()).select_from(Review)).scalar() or 0
    return f"RZ-{today}-{count + 1:04d}"


class ConfirmationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def respond(
        self,
        *,
        customer_id: str,
        challenge_id: str,
        response: str,
        version: int,
        idempotency_key: str,
    ) -> dict:
        """Processa uma resposta à confirmação.

        Retorna um dict pronto para serialização pelo schema ConfirmationResponseOut.
        Levanta ApiError para todos os casos de erro do contrato.
        """
        from app.api.errors import ApiError

        # 1. Busca a confirmação e a compra; verifica propriedade
        stmt_conf = select(Confirmation).where(Confirmation.challenge_id == challenge_id)
        confirmation = self._session.execute(stmt_conf).scalar_one_or_none()
        if confirmation is None:
            raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")

        purchase = self._session.get(Purchase, confirmation.purchase_id)
        if purchase is None or purchase.customer_id != customer_id:
            raise ApiError(404, "NOT_FOUND", "O recurso solicitado não foi encontrado.")

        # 2. Chave de idempotência: busca registro existente
        stmt_idem = select(IdempotencyKey).where(
            IdempotencyKey.key == idempotency_key,
            IdempotencyKey.challenge_id == challenge_id,
        )
        idem_record = self._session.execute(stmt_idem).scalar_one_or_none()

        this_body_hash = _body_hash(response, version)

        if idem_record is not None:
            if idem_record.body_hash != this_body_hash:
                # Mesma chave, corpo diferente → 422
                raise ApiError(
                    422,
                    "IDEMPOTENCY_KEY_REUSED",
                    "Esta chave de idempotência já foi usada com um corpo diferente.",
                )
            # Mesmo corpo → replay
            return {**_result_from_json(idem_record.response_json), "replayed": True}

        # 3. Verificações de estado (após chave de idempotência, antes de qualquer escrita)

        # Expiração: confere antes de VERSION_MISMATCH (§6)
        now = _now()
        expires_at = confirmation.expires_at
        if expires_at.tzinfo is not None:
            expires_at = expires_at.replace(tzinfo=None)

        if now > expires_at and purchase.status == "AGUARDANDO_ASSOCIADO":
            # Grava expiração e devolve 410
            from app.domain.cases.purchases import check_and_expire
            check_and_expire(purchase, confirmation, self._session)
            self._session.commit()
            raise ApiError(
                410,
                "CONFIRMATION_EXPIRED",
                "O prazo para responder a esta compra terminou. Ela não foi autorizada.",
                {
                    "status": "CONFIRMACAO_EXPIRADA",
                    "expired_at": expires_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
            )

        if purchase.status == "CONFIRMACAO_EXPIRADA":
            # Segunda tentativa: prazo já expirou em chamada anterior → também 410
            _ea = confirmation.expires_at
            if _ea.tzinfo is not None:
                _ea = _ea.replace(tzinfo=None)
            raise ApiError(
                410,
                "CONFIRMATION_EXPIRED",
                "O prazo para responder a esta compra terminou. Ela não foi autorizada.",
                {
                    "status": "CONFIRMACAO_EXPIRADA",
                    "expired_at": _ea.strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
            )

        if purchase.status != "AGUARDANDO_ASSOCIADO":
            # Pode ter sido respondida antes
            if confirmation.answered_response is not None:
                if confirmation.answered_response == response:
                    # Mesma resposta, chave nova → replay
                    result = self._build_result_dict(purchase, confirmation, replayed=True)
                    return result
                else:
                    answered_label = _RESPONSE_LABELS.get(
                        confirmation.answered_response, confirmation.answered_response
                    )
                    raise ApiError(
                        409,
                        "ALREADY_ANSWERED",
                        f'Esta compra já foi respondida como "{answered_label}". A resposta não foi alterada.',
                        {
                            "response": confirmation.answered_response,
                            "status": purchase.status,
                            "version": purchase.version,
                        },
                    )
            raise ApiError(
                409,
                "NOT_AWAITING_RESPONSE",
                "Esta compra não está aguardando resposta.",
                {"status": purchase.status},
            )

        # VERSION_MISMATCH
        if purchase.version != version:
            raise ApiError(
                409,
                "VERSION_MISMATCH",
                "A versão enviada não é a atual. Atualize a tela e tente novamente.",
                {"current_version": purchase.version},
            )

        # 4. Grava a resposta em transação
        answered_at = now
        new_status = _STATUS_BY_RESPONSE[response]
        from_status = purchase.status

        # Atualiza Purchase
        purchase.status = new_status
        purchase.version += 1
        purchase.updated_at = answered_at

        # Atualiza Confirmation
        confirmation.answered_response = response
        confirmation.answered_at = answered_at
        confirmation.idempotency_key = idempotency_key

        # Evento ANSWER
        event = Event(
            purchase_id=purchase.id,
            event_type="ANSWER",
            from_status=from_status,
            to_status=new_status,
            payload={"response": response},
            created_at=answered_at,
        )
        self._session.add(event)

        # Revisão (DENY → PROTECAO, UNSURE → DUVIDA ou reaproveita)
        review: Review | None = None
        review_kind = _REVIEW_KIND_BY_RESPONSE[response]
        if review_kind is not None:
            # Verifica se já há revisão aberta (UNSURE pode reaproveitar)
            existing_review = self._get_open_review(purchase)
            if existing_review is not None and response == "UNSURE":
                review = existing_review
            else:
                review = Review(
                    review_id=_next_review_id(self._session),
                    purchase_id=purchase.id,
                    protocol=_next_protocol(self._session),
                    kind=review_kind,
                    reason="OUTRO",
                    status="ABERTA",
                    created_by="SISTEMA",
                    created_at=answered_at,
                )
                self._session.add(review)
                self._session.flush()  # preenche review.id para pegar o protocolo

        self._session.flush()

        # Monta a resposta antes de gravar a chave (precisa do protocolo)
        result_data = self._build_result_dict(purchase, confirmation, replayed=False, review=review)

        # Grava chave de idempotência
        idem_key = IdempotencyKey(
            key=idempotency_key,
            challenge_id=challenge_id,
            body_hash=this_body_hash,
            response_json=_result_to_json({k: v for k, v in result_data.items() if k != "replayed"}),
            created_at=answered_at,
        )
        self._session.add(idem_key)
        self._session.commit()

        return result_data

    def _get_open_review(self, purchase: Purchase) -> Review | None:
        for rev in purchase.reviews:
            if rev.status == "ABERTA":
                return rev
        return None

    def _build_result_dict(
        self,
        purchase: Purchase,
        confirmation: Confirmation,
        replayed: bool,
        review: Review | None = None,
    ) -> dict:
        """Monta o dict de resposta do endpoint (§6)."""
        from app.domain.cases.purchases import _STATUS_LABELS, _build_result, _get_open_review

        if review is None:
            review = _get_open_review(purchase)

        review_protocol = review.protocol if review else None

        result_block = _build_result(purchase, review)
        # Garantia: result nunca é None para estado terminal pós-resposta
        if result_block is None:
            result_block = {"title": "", "description": "", "next_steps": []}

        answered_at = confirmation.answered_at
        if answered_at is None:
            from datetime import timezone
            answered_at = datetime.now(timezone.utc).replace(tzinfo=None)
        elif answered_at.tzinfo is not None:
            answered_at = answered_at.astimezone().replace(tzinfo=None)

        return {
            "challenge_id": confirmation.challenge_id,
            "case_id": purchase.case_id,
            "response": confirmation.answered_response,
            "answered_at": answered_at,
            "version": purchase.version,
            "status": purchase.status,
            "status_label": _STATUS_LABELS.get(purchase.status, purchase.status),
            "review_protocol": review_protocol,
            "result": result_block,
            "replayed": replayed,
        }
