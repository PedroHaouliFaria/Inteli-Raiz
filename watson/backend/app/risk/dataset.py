"""Bases do modelo em data/processed: o conjunto de teste (para escolher transações) e o treino (valores típicos)."""

import math
import random
from dataclasses import dataclass, field
from pathlib import Path

from app.risk.features import FEATURES, FeatureKind, normalize

TEST_FILE = "teste_proporcao_real.csv"
TRAIN_FILE = "treino_balanceado.csv"
ID_COLUMN = "event_external_id"
LABEL_COLUMN = "feedback_label"


@dataclass(frozen=True)
class Sample:
    id: str
    is_fraud: bool
    features: dict


@dataclass
class ReferenceData:
    samples: dict[str, Sample]
    # Valor típico de uma compra legítima no treino: mediana (numéricos e binários) ou moda (categóricos).
    baseline: dict
    # Valores que cada categórico assume nas bases, para a tela oferecer uma lista.
    options: dict[str, list[str]] = field(default_factory=dict)

    def find(self, sample_id: str) -> Sample | None:
        return self.samples.get(sample_id)

    def search(self, query: str = "", is_fraud: bool | None = None, limit: int = 20) -> list[Sample]:
        query = query.strip().upper()
        found = []
        for sample in self.samples.values():
            if is_fraud is not None and sample.is_fraud != is_fraud:
                continue
            if query and query not in sample.id:
                continue
            found.append(sample)
            if len(found) >= limit:
                break
        return found

    def pick_random(self, is_fraud: bool | None = None, rng: random.Random | None = None) -> Sample:
        pool = self.search(is_fraud=is_fraud, limit=len(self.samples))
        return (rng or random).choice(pool)


def _read(path: Path):
    import pandas as pd

    categorical = [f.name for f in FEATURES if f.kind is FeatureKind.CATEGORICAL]
    return pd.read_csv(path, dtype={name: str for name in categorical})


def _clean(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return value.item() if hasattr(value, "item") else value


def load_reference_data(data_dir: Path) -> ReferenceData:
    test = _read(data_dir / TEST_FILE)
    train = _read(data_dir / TRAIN_FILE)
    names = [f.name for f in FEATURES]

    samples = {}
    for record in test[[ID_COLUMN, LABEL_COLUMN, *names]].to_dict("records"):
        features = normalize({name: _clean(record[name]) for name in names})
        samples[record[ID_COLUMN]] = Sample(record[ID_COLUMN], bool(record[LABEL_COLUMN]), features)

    legit = train[train[LABEL_COLUMN] == 0]
    baseline = {}
    options = {}
    for f in FEATURES:
        if f.kind is FeatureKind.CATEGORICAL:
            baseline[f.name] = str(legit[f.name].mode().iloc[0])
            values = set(test[f.name].dropna()) | set(train[f.name].dropna())
            options[f.name] = sorted(values)
        else:
            baseline[f.name] = float(legit[f.name].median())
    return ReferenceData(samples=samples, baseline=normalize(baseline), options=options)
