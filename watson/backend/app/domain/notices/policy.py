"""Política do aviso de compra (decisão do Leo em 27/10/2026).

Risco médio: o agente envia o aviso sozinho. A analista só entra nas exceções:
risco alto, sem resposta, "Não reconheço", pedido de atendimento ou "Fui eu" vindo de aparelho trocado.
Os limiares vêm da versão do modelo (modelo_versao); os valores padrão são provisórios.
Ainda sem resposta do time, por isso configuráveis: se "Fui eu" fecha o caso sozinho
e quanto tempo o agente espera a resposta.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum


class RiskBand(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InitialHandling(StrEnum):
    NO_ACTION = "no_action"
    AUTO_SEND_NOTICE = "auto_send_notice"
    ROUTE_TO_ANALYST = "route_to_analyst"


class MemberResponse(StrEnum):
    IT_WAS_ME = "it_was_me"
    NOT_ME = "not_me"
    TALK_TO_PERSON = "talk_to_person"
    NO_RESPONSE = "no_response"


class ResponseOutcome(StrEnum):
    RELEASE_PURCHASE = "release_purchase"
    ROUTE_TO_ANALYST = "route_to_analyst"


@dataclass(frozen=True)
class NoticePolicy:
    medium_threshold: float = 0.60
    high_threshold: float = 0.80
    auto_close_on_it_was_me: bool = True
    response_timeout_minutes: int = 10


DEFAULT_POLICY = NoticePolicy()


def risk_band(score: float, policy: NoticePolicy = DEFAULT_POLICY) -> RiskBand:
    if score >= policy.high_threshold:
        return RiskBand.HIGH
    if score >= policy.medium_threshold:
        return RiskBand.MEDIUM
    return RiskBand.LOW


def initial_handling(score: float, policy: NoticePolicy = DEFAULT_POLICY) -> InitialHandling:
    band = risk_band(score, policy)
    if band is RiskBand.HIGH:
        return InitialHandling.ROUTE_TO_ANALYST
    if band is RiskBand.MEDIUM:
        return InitialHandling.AUTO_SEND_NOTICE
    return InitialHandling.NO_ACTION


def outcome_for_response(
    response: MemberResponse,
    *,
    biometrics_ok: bool,
    recent_device: bool,
    policy: NoticePolicy = DEFAULT_POLICY,
) -> ResponseOutcome:
    # Só "Fui eu" com biometria em aparelho conhecido fecha sem a analista, e só se a política permitir.
    trusted = response is MemberResponse.IT_WAS_ME and biometrics_ok and not recent_device
    if trusted and policy.auto_close_on_it_was_me:
        return ResponseOutcome.RELEASE_PURCHASE
    return ResponseOutcome.ROUTE_TO_ANALYST


def response_deadline(sent_at: datetime, policy: NoticePolicy = DEFAULT_POLICY) -> datetime:
    return sent_at + timedelta(minutes=policy.response_timeout_minutes)


def is_expired(sent_at: datetime, now: datetime, policy: NoticePolicy = DEFAULT_POLICY) -> bool:
    # Sem resposta no prazo vira exceção para a analista; nunca autorização presumida.
    return now >= response_deadline(sent_at, policy)
