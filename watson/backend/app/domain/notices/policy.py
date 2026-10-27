"""Política do aviso de compra (decisão do Leo em 27/10/2026).

Risco médio: o agente envia o aviso sozinho. A analista só entra nas exceções:
risco alto, sem resposta, "Não reconheço", pedido de atendimento ou "Fui eu" vindo de aparelho trocado.
Os limiares vêm da versão do modelo (modelo_versao); os valores padrão são provisórios.
"""

from dataclasses import dataclass
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
class Thresholds:
    medium: float = 0.60
    high: float = 0.80


def risk_band(score: float, thresholds: Thresholds = Thresholds()) -> RiskBand:
    if score >= thresholds.high:
        return RiskBand.HIGH
    if score >= thresholds.medium:
        return RiskBand.MEDIUM
    return RiskBand.LOW


def initial_handling(score: float, thresholds: Thresholds = Thresholds()) -> InitialHandling:
    band = risk_band(score, thresholds)
    if band is RiskBand.HIGH:
        return InitialHandling.ROUTE_TO_ANALYST
    if band is RiskBand.MEDIUM:
        return InitialHandling.AUTO_SEND_NOTICE
    return InitialHandling.NO_ACTION


def outcome_for_response(response: MemberResponse, *, biometrics_ok: bool, recent_device: bool) -> ResponseOutcome:
    # Só "Fui eu" com biometria em aparelho conhecido fecha sem a analista; o resto é exceção.
    if response is MemberResponse.IT_WAS_ME and biometrics_ok and not recent_device:
        return ResponseOutcome.RELEASE_PURCHASE
    return ResponseOutcome.ROUTE_TO_ANALYST
