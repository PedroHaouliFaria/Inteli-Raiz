#!/usr/bin/env python3
"""Gera app/fixtures/purchases.json a partir das linhas do CSV de teste.

As três fixtures são:
  - T-007 / fraude_supermercado_madrugada → EVT_SYN_000094500 (Ana, C-ANA)
  - T-003 / legitima_farmacia             → EVT_SYN_000043320 (Ana, C-ANA)
  - T-011 / compra_do_bruno               → EVT_SYN_000072693 (Bruno, C-BRUNO)

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
    },
    {
        "event_id":    "EVT_SYN_000072693",
        "fixture_id":  "compra_do_bruno",
        "case_id":     "T-011",
        "challenge_id": "CH-011",
        "customer_id": "C-BRUNO",
        "occurred_at": "2026-10-22T11:05:00Z",
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
    return {
        "fixture_id":   meta["fixture_id"],
        "case_id":      meta["case_id"],
        "challenge_id": meta["challenge_id"],
        "owner":        meta["customer_id"],
        "occurred_at":  meta["occurred_at"],
        "card_id":      card_id,
        "features":     features,
    }


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
