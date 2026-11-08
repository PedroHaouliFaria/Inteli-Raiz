"""Sinais de risco por regra (§5 do contrato).

Os três códigos fixos são: CARTAO_NAO_PRESENTE, MADRUGADA e PRIMEIRA_COMPRA_CARTAO.
Só vira sinal a feature com significado documentado (features de velocidade ficam de fora).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Signal:
    code: str
    label: str
    source: str = "regra"


# Mapa de MCC → rótulo para o associado
_MCC_LABELS: dict[str, str] = {
    "5411": "Supermercado",
    "5912": "Farmácia",
    "5812": "Restaurante",
}


def mcc_label(mcc: str) -> str:
    """Retorna o rótulo do MCC ou 'Categoria {mcc}' para códigos desconhecidos."""
    return _MCC_LABELS.get(str(mcc), f"Categoria {mcc}")


def amount_to_cents(amount: float | str) -> int:
    """Converte valor decimal para centavos inteiros sem perda de precisão."""
    from decimal import Decimal, ROUND_HALF_UP
    return int(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)


def card_last4(card_id: str) -> str:
    """Extrai os 4 últimos dígitos numéricos do card_id sintético (ex: 'CARD_SYN_0042938' → '2938')."""
    digits = "".join(c for c in card_id if c.isdigit())
    return digits[-4:] if len(digits) >= 4 else digits.zfill(4)


def compute_signals(features: dict) -> list[Signal]:
    """Aplica as três regras documentadas e retorna os sinais disparados, em ordem."""
    signals: list[Signal] = []

    # CARTAO_NAO_PRESENTE: usa modalidade_transacao == "cartao_nao_presente"
    # (card_presence_flag="N" com modalidade "cartao_presente" é inconsistência nos dados — ignorar)
    if str(features.get("modalidade_transacao", "")).lower() == "cartao_nao_presente":
        signals.append(
            Signal(
                code="CARTAO_NAO_PRESENTE",
                label="Feita sem o cartão físico (online ou por telefone).",
            )
        )

    # MADRUGADA: usa exclusivamente a coluna madrugada == "1"
    # (hora=5 com madrugada=0 não dispara; hora vazia não quebra)
    madrugada_flag = str(features.get("madrugada", "0"))
    if madrugada_flag == "1":
        hora = features.get("hora")
        hora_str = str(hora).strip() if hora is not None else ""
        if hora_str and hora_str.lstrip("-").isdigit():
            label = f"Feita de madrugada, às {int(hora_str)}h."
        else:
            label = "Feita de madrugada."
        signals.append(Signal(code="MADRUGADA", label=label))

    # PRIMEIRA_COMPRA_CARTAO: coluna primeira_compra_cartao = 1
    if str(features.get("primeira_compra_cartao", "0")) == "1":
        signals.append(
            Signal(
                code="PRIMEIRA_COMPRA_CARTAO",
                label="Primeira compra registrada com este cartão.",
            )
        )

    return signals
