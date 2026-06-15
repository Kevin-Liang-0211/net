"""Question 2: sweep parameters for four models; tables + figures."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metrics import average_degree, clustering_average, diameter_and_avg_path, edge_count
from models import ba_graph, er_graph_gnm, er_graph_gnp, ring_lattice_graph, ws_graph
from utils import ROOT, ensure_dirs, savefig


def safe_metrics(G: nx.Graph):
    diam, apl = diameter_and_avg_path(G)
    return {
        "m": edge_count(G),
        "avg_deg": average_degree(G),
        "C": clustering_average(G),
        "diam": diam,
        "apl": apl,
    }


def sweep_ring():
    rows = []
    k = 4
    for n in range(20, 121, 20):
        G = ring_lattice_graph(n, k)
        row = {"model": "ring", "n": n, "k": k, **safe_metrics(G)}
        rows.append(row)
    return pd.DataFrame(rows)


def sweep_er():
    rows = []
    n = 80
    for p in [0.02, 0.05, 0.08, 0.12, 0.2]:
        G = er_graph_gnp(n, p, seed=42)
        row = {"model": "ER_Gnp", "n": n, "p": p, **safe_metrics(G)}
        rows.append(row)
    return pd.DataFrame(rows)


def sweep_ws():
    rows = []
    n, k = 100, 6
    for p in [0.0, 0.05, 0.1, 0.2, 0.4, 0.8]:
        G = ws_graph(n, k, p, seed=123)
        row = {"model": "WS", "n": n, "k": k, "beta": p, **safe_metrics(G)}
        rows.append(row)
    return pd.DataFrame(rows)


def sweep_ba():
    rows = []
    m = 3
    for n in range(40, 241, 40):
        G = ba_graph(n, m, seed=99)
        row = {"model": "BA", "n": n, "m": m, **safe_metrics(G)}
        rows.append(row)
    return pd.DataFrame(rows)


def plot_degree_samples():
    ensure_dirs()
    seed = 5
    n = 120
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    G1 = ring_lattice_graph(n, 6)
    axes[0, 0].hist(dict(G1.degree()).values(), bins=15, color="#4477AA")
    axes[0, 0].set_title("规则网络度序列（WS,p=0）")

    G2 = er_graph_gnm(n, 400, seed=seed)
    axes[0, 1].hist(dict(G2.degree()).values(), bins=15, color="#AA7744")
    axes[0, 1].set_title("ER G(n,m) 度分布示意")

    G3 = ws_graph(n, 6, 0.15, seed=seed)
    axes[1, 0].hist(dict(G3.degree()).values(), bins=15, color="#669944")
    axes[1, 0].set_title("WS 小世界度分布")

    G4 = ba_graph(n, 3, seed=seed)
    axes[1, 1].hist(dict(G4.degree()).values(), bins=15, color="#8844AA")
    axes[1, 1].set_title("BA 无标度度分布（长尾）")

    for ax in axes.flat:
        ax.set_xlabel("度")
        ax.set_ylabel("频数")
    plt.tight_layout()
    savefig("q2_degree_grid.png")


def plot_scaling_metrics():
    ensure_dirs()
    n_list = list(range(30, 201, 10))
    er_apl, er_c = [], []
    ba_apl, ba_c = [], []
    for n in n_list:
        Ge = er_graph_gnp(n, 6 / max(n - 1, 1), seed=11)
        er_apl.append(diameter_and_avg_path(Ge)[1])
        er_c.append(clustering_average(Ge))
        Gb = ba_graph(n, 3, seed=11)
        ba_apl.append(diameter_and_avg_path(Gb)[1])
        ba_c.append(clustering_average(Gb))

    plt.figure(figsize=(7, 5))
    plt.plot(n_list, er_apl, label="ER ~稀疏(p=c/(n-1), c=6)")
    plt.plot(n_list, ba_apl, label="BA (m=3)")
    plt.xlabel("N")
    plt.ylabel("平均路径长度（巨连通分量）")
    plt.title("不同规模下随机网络 vs BA 的平均路径长度")
    plt.legend()
    savefig("q2_apl_scaling.png")

    plt.figure(figsize=(7, 5))
    plt.plot(n_list, er_c, label="ER (c=6)")
    plt.plot(n_list, ba_c, label="BA (m=3)")
    plt.xlabel("N")
    plt.ylabel("平均聚类系数")
    plt.title("聚类系数随规模变化（示意）")
    plt.legend()
    savefig("q2_clustering_scaling.png")


def main():
    ensure_dirs()
    ring_df = sweep_ring()
    er_df = sweep_er()
    ws_df = sweep_ws()
    ba_df = sweep_ba()

    OUT = ROOT / "output"
    OUT.mkdir(parents=True, exist_ok=True)
    ring_df.to_csv(OUT / "q2_ring.csv", index=False)
    er_df.to_csv(OUT / "q2_er.csv", index=False)
    ws_df.to_csv(OUT / "q2_ws.csv", index=False)
    ba_df.to_csv(OUT / "q2_ba.csv", index=False)

    plot_degree_samples()
    plot_scaling_metrics()

    bundle = {
        "tables": {
            "ring": ring_df.to_csv(index=False),
            "er": er_df.to_csv(index=False),
            "ws": ws_df.to_csv(index=False),
            "ba": ba_df.to_csv(index=False),
        },
        "figures": [
            "figures/q2_degree_grid.png",
            "figures/q2_apl_scaling.png",
            "figures/q2_clustering_scaling.png",
        ],
    }
    (OUT / "q2_bundle.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    return bundle


if __name__ == "__main__":
    main()
