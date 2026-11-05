#!/usr/bin/env python3
"""Gera app/fixtures/purchases.json a partir de linhas sintéticas do CSV de teste.

O conjunto persistido tem 15 compras variadas entre Ana e Bruno. Há exemplos
legítimos e fraudulentos conhecidos apenas durante a seleção das fixtures; o
rótulo nunca entra no JSON nem na API. Uma fixture adicional, sem ``case_id``,
é reservada ao endpoint de demonstração de falha do modelo.

Campos excluídos: feedback_label, customer_id, fraud_score, visa_fraud_score,
mc_fraud_score, event_external_id (não são features do modelo nem dados seguros).
O card_id é incluído separadamente (serve para card_last4).
As 28 features ficam como texto exatamente igual ao CSV.
"""
import csv
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
CSV_PATH = REPO_ROOT / "data" / "processed" / "teste_proporcao_real.csv"
OUT_PATH = pathlib.Path(__file__).resolve().parents[1] / "app" / "fixtures" / "purchases.json"

# Campos a NÃO incluir nas features
EXCLUDED = frozenset({
    "event_external_id",
    "customer_id",
    "feedback_label",
    "fraud_score",
    "visa_fraud_score",
    "mc_fraud_score",
    "card_id",  # tratado separadamente
})

FIXTURES = [
    {
        "event_id":    "EVT_SYN_000094500",
        "fixture_id":  "fraude_supermercado_madrugada",
        "case_id":     "T-007",
        "challenge_id": "CH-007",
        "customer_id": "C-ANA",
        "occurred_at": "2026-10-25T06:12:00Z",
    },
    {
        "event_id":    "EVT_SYN_000043320",
        "fixture_id":  "legitima_farmacia",
        "case_id":     "T-003",
        "challenge_id": "CH-003",
        "customer_id": "C-ANA",
        "occurred_at": "2026-10-19T21:40:00Z",
        "seed_review": {
            "reason": "VALOR_DIFERENTE",
            "details": "Revisão fictícia criada para demonstrar a fila da analista.",
            "created_by": "ASSOCIADO",
        },
    },
    {
        "event_id":    "EVT_SYN_000072693",
        "fixture_id":  "compra_do_bruno",
        "case_id":     "T-011",
        "challenge_id": "CH-011",
        "customer_id": "C-BRUNO",
        "occurred_at": "2026-10-22T11:05:00Z",
    },
    {
        "event_id": "EVT_SYN_000154028", "fixture_id": "fraude_transporte_baixo_valor",
        "case_id": "T-012", "challenge_id": "CH-012", "customer_id": "C-ANA",
        "occurred_at": "2026-11-03T04:05:00Z",
        "seed_review": {
            "reason": "NAO_RECONHECE_ESTABELECIMENTO",
            "details": "Compra noturna não reconhecida pelo associado.",
            "created_by": "ASSOCIADO",
        },
    },
    {
        "event_id": "EVT_SYN_000066580", "fixture_id": "legitima_combustivel_valor_minimo",
        "case_id": "T-013", "challenge_id": "CH-013", "customer_id": "C-BRUNO",
        "occurred_at": "2026-11-03T13:00:00Z",
    },
    {
        "event_id": "EVT_SYN_000155401", "fixture_id": "fraude_varejo_madrugada",
        "case_id": "T-014", "challenge_id": "CH-014", "customer_id": "C-BRUNO",
        "occurred_at": "2026-11-02T04:20:00Z",
    },
    {
        "event_id": "EVT_SYN_000034872", "fixture_id": "legitima_supermercado_online",
        "case_id": "T-015", "challenge_id": "CH-015", "customer_id": "C-ANA",
        "occurred_at": "2026-11-02T23:15:00Z",
    },
    {
        "event_id": "EVT_SYN_000147376", "fixture_id": "fraude_farmacia_madrugada",
        "case_id": "T-016", "challenge_id": "CH-016", "customer_id": "C-ANA",
        "occurred_at": "2026-11-01T04:42:00Z",
        "seed_review": {
            "reason": "VALOR_DIFERENTE",
            "details": "Valor informado difere do que o associado esperava.",
            "created_by": "ASSOCIADO",
        },
    },
    {
        "event_id": "EVT_SYN_000094150", "fixture_id": "legitima_servico_digital",
        "case_id": "T-017", "challenge_id": "CH-017", "customer_id": "C-BRUNO",
        "occurred_at": "2026-11-01T21:30:00Z",
    },
    {
        "event_id": "EVT_SYN_000153116", "fixture_id": "fraude_varejo_valor_medio",
        "case_id": "T-018", "challenge_id": "CH-018", "customer_id": "C-BRUNO",
        "occurred_at": "2026-10-31T03:18:00Z",
    },
    {
        "event_id": "EVT_SYN_000107879", "fixture_id": "legitima_combustivel",
        "case_id": "T-019", "challenge_id": "CH-019", "customer_id": "C-ANA",
        "occurred_at": "2026-10-31T17:10:00Z",
    },
    {
        "event_id": "EVT_SYN_000004918", "fixture_id": "fraude_posto_alto_valor",
        "case_id": "T-020", "challenge_id": "CH-020", "customer_id": "C-ANA",
        "occurred_at": "2026-10-30T03:50:00Z",
    },
    {
        "event_id": "EVT_SYN_000020583", "fixture_id": "legitima_comercio_geral",
        "case_id": "T-021", "challenge_id": "CH-021", "customer_id": "C-BRUNO",
        "occurred_at": "2026-10-30T19:25:00Z",
        "seed_review": {
            "reason": "DUVIDA_PROCESSO",
            "details": "Associado pediu ajuda para entender o processo de confirmação.",
            "created_by": "ASSOCIADO",
        },
    },
    {
        "event_id": "EVT_SYN_000019447", "fixture_id": "legitima_varejo",
        "case_id": "T-022", "challenge_id": "CH-022", "customer_id": "C-BRUNO",
        "occurred_at": "2026-10-29T23:05:00Z",
    },
    {
        "event_id": "EVT_SYN_000145092", "fixture_id": "legitima_alto_valor_sem_cartao",
        "case_id": "T-023", "challenge_id": "CH-023", "customer_id": "C-ANA",
        "occurred_at": "2026-10-29T03:12:00Z",
    },
    {
        "event_id": "EVT_SYN_000043320", "fixture_id": "falha_modelo",
        "case_id": None, "challenge_id": None, "customer_id": "C-ANA",
        "occurred_at": "2026-10-27T14:30:00Z",
        "remove_features": ["amount"],
    },
]


def load_csv_rows(csv_path: pathlib.Path) -> dict[str, dict]:
    """Retorna dict {event_external_id: row_dict} para as linhas relevantes."""
    target_ids = {f["event_id"] for f in FIXTURES}
    rows: dict[str, dict] = {}
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row["event_external_id"] in target_ids:
                rows[row["event_external_id"]] = row
    return rows


def build_fixture(meta: dict, row: dict) -> dict:
    """Monta um objeto de fixture sem campos proibidos."""
    card_id = row["card_id"]
    features = {k: v for k, v in row.items() if k not in EXCLUDED}
    for name in meta.get("remove_features", []):
        features.pop(name, None)
    fixture = {
        "fixture_id":   meta["fixture_id"],
        "case_id":      meta["case_id"],
        "challenge_id": meta["challenge_id"],
        "owner":        meta["customer_id"],
        "occurred_at":  meta["occurred_at"],
        "card_id":      card_id,
        "features":     features,
    }
    if "seed_review" in meta:
        fixture["seed_review"] = meta["seed_review"]
    return fixture


def main() -> None:
    if not CSV_PATH.exists():
        print(f"ERRO: CSV não encontrado em {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    csv_rows = load_csv_rows(CSV_PATH)
    result = []
    for meta in FIXTURES:
        if meta["event_id"] not in csv_rows:
            print(f"ERRO: {meta['event_id']} não encontrado no CSV", file=sys.stderr)
            sys.exit(1)
        result.append(build_fixture(meta, csv_rows[meta["event_id"]]))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    print(f"Gerado: {OUT_PATH} ({len(result)} fixtures)")


if __name__ == "__main__":
    main()
