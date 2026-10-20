"""Gera as figuras usadas em docs/01_analise_exploratoria.md.

Uso (na raiz do repositório):
    python scripts/gerar_figuras_docs.py

Requer data/transacoes.pkl (criado pelo notebooks/01_eda.ipynb),
outputs/triagem_colunas.csv e data/processed/ (criado pelo notebooks/02_base_balanceada.ipynb).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "docs" / "assets"
IMG.mkdir(parents=True, exist_ok=True)

# Paleta validada (dataviz default): azul = legítima, laranja = fraude
LEGIT, FRAUDE, NEUTRO, TEXTO, GRADE = "#2a78d6", "#eb6834", "#b5b5af", "#3d3d3a", "#e6e6e3"
plt.rcParams.update({
    "figure.dpi": 130, "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": NEUTRO,
    "axes.grid": True, "grid.color": GRADE, "axes.axisbelow": True, "text.color": TEXTO,
    "axes.labelcolor": TEXTO, "xtick.color": TEXTO, "ytick.color": TEXTO, "legend.frameon": False,
})


def salvar(fig, nome):
    fig.savefig(IMG / nome, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("ok", nome)


df = pd.read_pickle(ROOT / "data" / "transacoes.pkl")
y = df["feedback_label"].astype(str).str.lower().eq("true")
ts = pd.to_datetime(df["event_occurred_at"], errors="coerce")
hora = ts.dt.hour

# ---------------------------------------------------------------- 1. Painel: retrato da fraude
seg = df.assign(y=y).groupby(["tipo_transacao", "modalidade_transacao"])["y"].agg(["mean", "sum"])
NOMES = {"credito": "Crédito", "debito": "Débito", "cartao_presente": "presente", "cartao_nao_presente": "não presente"}
seg.index = [f"{NOMES[t]} · {NOMES[m]}" for t, m in seg.index]
seg = seg.sort_values("mean")

base_feat = pd.read_csv(ROOT / "data" / "processed" / "teste_proporcao_real.csv")
base_feat = pd.concat([base_feat, pd.read_csv(ROOT / "data" / "processed" / "treino_balanceado.csv")],
                      ignore_index=True)

fig, ax = plt.subplots(2, 2, figsize=(12, 7.5))

a = ax[0, 0]
a.barh(seg.index, seg["mean"] * 100, color=FRAUDE, height=0.55)
for i, (v, n) in enumerate(zip(seg["mean"] * 100, seg["sum"])):
    a.text(v, i, f"  {v:.2f}%  ({int(n)} fraudes)", va="center", fontsize=9)
a.set(title="1 · Onde: crédito sem cartão presente", xlabel="% das transações que são fraude",
      xlim=(0, seg["mean"].max() * 100 * 1.6))
a.grid(axis="y", visible=False)

a = ax[0, 1]
dist = pd.crosstab(hora, y, normalize="columns") * 100
w = 0.42
a.bar(dist.index - w / 2, dist[False], width=w, color=LEGIT, label="Legítima")
a.bar(dist.index + w / 2, dist[True], width=w, color=FRAUDE, label="Fraude")
a.set(title="2 · Quando: 100% das fraudes entre 0h e 4h", xlabel="hora do dia", ylabel="% da classe",
      xticks=range(0, 24, 2))
a.legend(loc="upper right")
a.grid(axis="x", visible=False)


def caixas(a, col, titulo, log=True, rotulo=""):
    dados = []
    for k in (0, 1):
        s = base_feat.loc[base_feat.feedback_label == k, col].dropna()
        dados.append(np.log10(s.clip(lower=1e-3)) if log else s)
    bp = a.boxplot(dados, tick_labels=["Legítima", "Fraude"], patch_artist=True, widths=0.5,
                   medianprops={"color": "white", "lw": 2}, flierprops={"marker": ".", "alpha": 0.3})
    for p, c in zip(bp["boxes"], (LEGIT, FRAUDE)):
        p.set_facecolor(c); p.set_edgecolor(c)
    a.set_title(titulo)
    a.set_ylabel(rotulo)
    a.grid(axis="x", visible=False)


caixas(ax[1, 0], "valor_vs_media_cartao",
       "3 · Quanto: valor muito acima do padrão do cartão", rotulo="valor ÷ média anterior (log10)")
ax[1, 0].axhline(0, color=NEUTRO, ls="--", lw=1)
ax[1, 0].text(0.02, 0.02, "linha tracejada = valor igual à média do cartão", fontsize=8, color="#8a8a85",
              transform=ax[1, 0].transAxes)

a = ax[1, 1]
sinais = {"Distância do\nterminal anterior": "cp_card_prev_term_dist_1h", "Risco do\nestabelecimento": "acceptor_risk",
          "Valor da\ncompra": "amount", "Transações do\ncartão (1m)": "cardid_count_1m"}
razoes = {k: df.loc[y, c].median() / df.loc[~y, c].median() for k, c in sinais.items()}
razoes = pd.Series(razoes).sort_values()
a.barh(razoes.index, razoes.values, color=FRAUDE, height=0.55)
for i, v in enumerate(razoes.values):
    a.text(v, i, f"  {v:.0f}×", va="center", fontsize=9)
a.axvline(1, color=NEUTRO, ls="--", lw=1)
a.set(title="4 · Como: sinais muito acima do normal", xlabel="mediana na fraude ÷ mediana na legítima",
      xlim=(0, razoes.max() * 1.2))
a.grid(axis="y", visible=False)

fig.suptitle("Retrato da fraude em cartões", fontsize=14, fontweight="bold", x=0.01, ha="left", y=1.0)
fig.tight_layout()
salvar(fig, "painel_retrato_fraude.png")

# ---------------------------------------------------------------- 2. Força dos sinais (AUC)
cols = ["cp_card_term_vel_1h", "digitalwallettoken_count_3m", "cardid_count_1m", "fraud_score",
        "mc_fraud_score", "visa_fraud_score", "cp_card_prev_term_dist_1h", "acceptor_risk", "amount",
        "amount_fees", "account_balance", "card_credit_limit", "customer_presumed_income"]
aucs = {}
for c in cols:
    s = pd.to_numeric(df[c], errors="coerce"); m = s.notna()
    r = roc_auc_score(y[m], s[m]); aucs[c] = max(r, 1 - r)
m = hora.notna(); r = roc_auc_score(y[m], hora[m]); aucs["hora"] = max(r, 1 - r)
aucs = pd.Series(aucs).sort_values()

papel = {c: "Score externo (baseline)" for c in ["fraud_score", "mc_fraud_score", "visa_fraud_score"]}
papel.update({c: "Pré-calculada (velocidade)" for c in ["cp_card_term_vel_1h", "digitalwallettoken_count_3m",
                                                        "cardid_count_1m"]})
cor = {"Score externo (baseline)": "#8a8a85", "Pré-calculada (velocidade)": FRAUDE, "Feature do modelo": LEGIT}

fig, a = plt.subplots(figsize=(9, 5.2))
a.barh(aucs.index, aucs.values, color=[cor[papel.get(c, "Feature do modelo")] for c in aucs.index], height=0.65)
a.axvline(0.5, color=NEUTRO, ls="--", lw=1)
a.text(0.505, -0.9, "0,5 = sem sinal", fontsize=8, color="#8a8a85")
for nome, c in cor.items():
    a.barh([0], [0], color=c, label=nome)
a.legend(loc="lower right")
a.set(xlim=(0.45, 1.02), xlabel="AUC univariada (1,0 = separa perfeitamente)",
      title="Quanto cada variável, sozinha, separa fraude de legítima")
a.grid(axis="y", visible=False)
fig.tight_layout()
salvar(fig, "forca_dos_sinais.png")

# ---------------------------------------------------------------- 3. Triagem de colunas
tri = pd.read_csv(ROOT / "outputs" / "triagem_colunas.csv")
rot = {"remover_ruido": "Ruído (muito vazio, sem sinal)", "remover_pii": "Dados pessoais",
       "manter": "Manter (candidatas)", "remover_vazamento": "Vazamento", "id_agregacao": "Identificadores",
       "remover_constante": "Constantes", "nivel_B_pre_calculada": "Velocidade/distância prontas",
       "baseline_externo": "Scores externos (baseline)", "alvo": "Alvo"}
cont = tri.decisao.map(rot).value_counts().sort_values()
cores = [LEGIT if k in ("Manter (candidatas)", "Velocidade/distância prontas") else
         "#8a8a85" if k in ("Scores externos (baseline)", "Alvo", "Identificadores") else NEUTRO for k in cont.index]

fig, a = plt.subplots(figsize=(9, 4.2))
a.barh(cont.index, cont.values, color=cores, height=0.6)
for i, v in enumerate(cont.values):
    a.text(v, i, f"  {v}", va="center", fontsize=9)
a.set(title=f"Triagem das {len(tri)} colunas: o que entra no modelo (azul) e o que sai (cinza)",
      xlabel="nº de colunas", xlim=(0, cont.max() * 1.12))
a.grid(axis="y", visible=False)
fig.tight_layout()
salvar(fig, "triagem_colunas.png")

# ---------------------------------------------------------------- 4. Nulos: três blocos
pct = df.isna().mean()
blocos = pd.cut(pct, [-0.01, 0.05, 0.30, 1],
                labels=["Quase completas\n(0–5% vazio)", "~8% vazio\n(variáveis relevantes)",
                        "~76% vazio\n(campos secundários)"]).value_counts().sort_index()
fig, a = plt.subplots(figsize=(8, 3.4))
a.bar(blocos.index.astype(str), blocos.values, color=[LEGIT, LEGIT, NEUTRO], width=0.55)
for i, v in enumerate(blocos.values):
    a.text(i, v, f"{v} colunas", ha="center", va="bottom", fontsize=10)
a.set(title="Qualidade: as 297 colunas se dividem em três blocos de dados vazios", ylabel="nº de colunas",
      ylim=(0, blocos.max() * 1.15))
a.grid(axis="x", visible=False)
fig.tight_layout()
salvar(fig, "nulos_por_coluna.png")
