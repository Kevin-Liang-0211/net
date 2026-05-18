"""Q6: Statistics + community & influence comparison on SNAP Email-Eu-core."""
import gzip
import json
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from community import community_louvain
from scipy.stats import spearmanr
from sklearn.cluster import KMeans

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deepwalk_embed import deepwalk_embeddings
from utils import DATA_DIR, ROOT, ensure_dirs, download, savefig

EMAIL_EU_URL = "https://snap.stanford.edu/data/email-Eu-core.txt.gz"


def load_email_eu():
    ensure_dirs()
    path = DATA_DIR / "email-Eu-core.txt.gz"
    download(EMAIL_EU_URL, path)
    G = nx.DiGraph()
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            u, v = int(parts[0]), int(parts[1])
            G.add_edge(u, v)
    return G


def main():
    ensure_dirs()
    G = load_email_eu()

    stats = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": float(nx.density(G)),
    }

    Gu_all = G.to_undirected()
    deg_seq = [d for _, d in Gu_all.degree()]
    stats["avg_degree_undirected"] = float(sum(deg_seq) / len(deg_seq)) if deg_seq else 0.0

    plt.figure(figsize=(7, 4))
    plt.hist(deg_seq, bins=40, color="#4477AA", edgecolor="white")
    plt.xlabel("Degree (无向化后)")
    plt.ylabel("频数")
    plt.title("Email-Eu-core — 度分布（无向简单图）")
    fig_deg = savefig("q6_degree_hist.png")

    Gu = Gu_all
    if not nx.is_connected(Gu):
        giant_nodes = max(nx.connected_components(Gu), key=len)
        Gu_g = Gu.subgraph(giant_nodes).copy()
        G_g = G.subgraph(giant_nodes).copy()
    else:
        Gu_g = Gu
        G_g = G

    stats["largest_cc_nodes"] = Gu_g.number_of_nodes()
    stats["largest_cc_edges_undirected"] = Gu_g.number_of_edges()

    stats["avg_clustering"] = float(nx.average_clustering(Gu_g))

    apl = float("nan")
    if Gu_g.number_of_nodes() <= 2000:
        try:
            apl = float(nx.average_shortest_path_length(Gu_g))
        except Exception:
            apl = float("nan")
    stats["average_shortest_path_length_giant"] = apl

    t0 = time.perf_counter()
    part_lv = community_louvain.best_partition(Gu_g)
    t1 = time.perf_counter()
    buckets = {}
    for n, c in part_lv.items():
        buckets.setdefault(c, set()).add(n)
    comm_lv = list(buckets.values())
    mod_lv = nx.community.modularity(Gu_g, comm_lv)

    t2 = time.perf_counter()
    emb = deepwalk_embeddings(Gu_g, dimensions=48, walk_length=20, num_walks=8, seed=3)
    nodes_ord = sorted(Gu_g.nodes())
    X = np.stack([emb[n] for n in nodes_ord])
    k = max(2, len(set(part_lv.values())))
    km = KMeans(n_clusters=min(k, 12), random_state=1, n_init=10)
    labels = km.fit_predict(X)
    t3 = time.perf_counter()

    label_buckets = {}
    for n, lb in zip(nodes_ord, labels):
        label_buckets.setdefault(int(lb), set()).add(n)
    comm_dw = list(label_buckets.values())
    mod_dw = nx.community.modularity(Gu_g, comm_dw)

    pos = nx.spring_layout(Gu_g, seed=0, k=0.15 / np.sqrt(Gu_g.number_of_nodes()))
    plt.figure(figsize=(9, 7))
    cmap = plt.cm.tab20
    for lb in range(labels.max() + 1):
        ns = [nodes_ord[i] for i in range(len(nodes_ord)) if labels[i] == lb]
        if not ns:
            continue
        nx.draw_networkx_nodes(Gu_g, pos, nodelist=ns, node_size=15, node_color=[cmap(lb % 20)], alpha=0.85)
    nx.draw_networkx_edges(Gu_g, pos, width=0.2, alpha=0.08)
    plt.title(f"Email-Eu-core giant CC — DeepWalk+KMeans (k={len(comm_dw)}), Q={mod_dw:.4f}")
    plt.axis("off")
    fig_dw = savefig("q6_deepwalk_layout.png")

    pr = nx.pagerank(G_g, alpha=0.85)
    deg_cent = nx.degree_centrality(Gu_g)
    emb_inf = {n: float(np.linalg.norm(emb[n], ord=2)) for n in nodes_ord}

    s_pr = pd.Series(pr).reindex(nodes_ord).fillna(0)
    s_deg = pd.Series({n: deg_cent[n] for n in nodes_ord})
    s_emb = pd.Series(emb_inf)

    rho_ed_pr, _ = spearmanr(s_deg.values, s_pr.values)
    rho_emb_pr, _ = spearmanr(s_emb.values, s_pr.values)
    rho_emb_deg, _ = spearmanr(s_emb.values, s_deg.values)

    core_pr = s_pr.sort_values(ascending=False).head(12)
    core_emb = s_emb.sort_values(ascending=False).head(12)

    out = {
        "basic_stats": stats,
        "figures": {
            "degree_hist": str(fig_deg.relative_to(ROOT)),
            "deepwalk_layout": str(fig_dw.relative_to(ROOT)),
        },
        "community": {
            "louvain_modularity": float(mod_lv),
            "deepwalk_kmeans_modularity": float(mod_dw),
            "num_communities_louvain": len(comm_lv),
            "num_communities_deepwalk": len(comm_dw),
            "runtime_louvain_sec": float(t1 - t0),
            "runtime_deepwalk_total_sec": float(t3 - t2),
        },
        "influence": {
            "spearman_degree_vs_pagerank": float(rho_ed_pr),
            "spearman_emb_vs_pagerank": float(rho_emb_pr),
            "spearman_emb_vs_degree": float(rho_emb_deg),
            "top_nodes_pagerank": [str(int(k)) for k in core_pr.index],
            "top_nodes_embedding_norm": [str(int(k)) for k in core_emb.index],
        },
    }
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
