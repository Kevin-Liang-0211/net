"""Q4: PageRank on signed weighted Bitcoin OTC trust network (SNAP)."""
import gzip
import json
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import DATA_DIR, ROOT, ensure_dirs, download, savefig

BITCOIN_OTC_URL = "https://snap.stanford.edu/data/soc-sign-bitcoinotc.csv.gz"


def load_bitcoin_otc():
    """Directed weighted graph; weight uses absolute trust rating."""
    ensure_dirs()
    gz_path = DATA_DIR / "soc-sign-bitcoinotc.csv.gz"
    download(BITCOIN_OTC_URL, gz_path)

    with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as raw:
        df = pd.read_csv(raw, header=None, names=["source", "target", "rating", "time"])

    G = nx.DiGraph()
    eps = 1e-6
    for _, row in df.iterrows():
        u, v = int(row["source"]), int(row["target"])
        w = float(abs(row["rating"]))
        if w < eps:
            w = eps
        if G.has_edge(u, v):
            G[u][v]["weight"] += w
        else:
            G.add_edge(u, v, weight=w)
    return G


def main():
    ensure_dirs()
    G = load_bitcoin_otc()

    t0 = time.perf_counter()
    pr = nx.pagerank(G, alpha=0.85, weight="weight")
    t1 = time.perf_counter()

    in_deg = dict(G.in_degree(weight="weight"))
    pr_sorted = sorted(pr.items(), key=lambda x: -x[1])[:20]

    xs = np.array([pr[n] for n in G.nodes()])
    ys = np.array([in_deg.get(n, 0) for n in G.nodes()])
    corr = float(np.corrcoef(xs, ys)[0, 1]) if len(xs) > 1 else float("nan")

    plt.figure(figsize=(7, 5))
    plt.scatter(ys, xs, s=8, alpha=0.35)
    plt.xlabel("Weighted in-degree")
    plt.ylabel("PageRank")
    plt.title("Bitcoin OTC — PageRank vs weighted in-degree")
    fig_path = savefig("q4_pagerank_scatter.png")

    out = {
        "dataset": "SNAP soc-sign-bitcoinotc (directed, weighted trust ratings)",
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "pagerank_runtime_sec": float(t1 - t0),
        "corr_pr_vs_weighted_indegree": corr,
        "top20_pagerank": [{"node": int(n), "pagerank": float(v)} for n, v in pr_sorted],
        "figure": str(fig_path.relative_to(ROOT)),
    }
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
