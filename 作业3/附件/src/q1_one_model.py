"""Question 1: pick one model with N in [10,20], M in [10,100], report metrics."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metrics import (
    average_degree,
    clustering_average,
    degree_distribution,
    density,
    diameter_and_avg_path,
    edge_count,
)
from models import ba_graph
from utils import ROOT, ensure_dirs, savefig


def summarize(G: nx.Graph, name: str):
    n = G.number_of_nodes()
    m = edge_count(G)
    diam, apl = diameter_and_avg_path(G)
    dd = degree_distribution(G)
    return {
        "model": name,
        "nodes": n,
        "edges": m,
        "average_degree": average_degree(G),
        "density": density(G),
        "diameter_giant": diam,
        "average_shortest_path_giant": apl,
        "average_clustering": clustering_average(G),
        "degree_distribution": {str(k): v for k, v in dd.items()},
    }


def main():
    ensure_dirs()
    # BA model: choose N=15, m=3 → edges ∈ [10,100] typically
    N, m = 15, 3
    seed = 7
    G = ba_graph(N, m, seed=seed)

    rep = summarize(G, "BA 无标度网络 (Barabási–Albert)")
    rep["construction"] = (
        f"从 m={m} 个节点的完全图出发，每次加入 1 个新节点并向已有节点连 m 条边，"
        "连边概率与节点度成正比（优先连接）。参数：N={N}, m={m}, seed={seed}。"
    )
    rep["formulas"] = {
        "average_degree": r"\bar{k}=2m/N",
        "density": r"\rho=2m/(N(N-1))",
        "clustering": r"C_i=2T_i/(k_i(k_i-1)), \bar{C}=\frac1N\sum C_i",
        "apl_diameter": "在最大连通分量上由最短路径算法计算",
    }

    degs = sorted(dict(G.degree()).values())
    plt.figure(figsize=(6, 4))
    plt.hist(degs, bins=range(min(degs), max(degs) + 2), align="left", rwidth=0.8)
    plt.xlabel("度 k")
    plt.ylabel("频数")
    plt.title("题1：BA 网络度分布直方图")
    fig = savefig("q1_degree_hist.png")
    rep["figure_degree_hist"] = str(fig.relative_to(ROOT))

    pos = nx.spring_layout(G, seed=seed)
    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, node_size=260, with_labels=True, font_size=9)
    plt.title(f"题1：BA 示例网络 (N={N}, M={G.number_of_edges()})")
    fig2 = savefig("q1_layout.png")
    rep["figure_layout"] = str(fig2.relative_to(ROOT))

    out_path = ROOT / "output" / "q1_report.json"
    out_path.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    return rep


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
