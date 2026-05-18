"""Optional Q2 extension: DeepWalk + KMeans communities vs Louvain."""
import json
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from community import community_louvain
from sklearn.cluster import KMeans

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deepwalk_embed import deepwalk_embeddings
from utils import ROOT, ensure_dirs, savefig


def partition_from_labels(nodes, labels):
    buckets = {}
    for n, lb in zip(nodes, labels):
        buckets.setdefault(int(lb), set()).add(n)
    return list(buckets.values())


def main():
    ensure_dirs()
    G = nx.karate_club_graph()

    t0 = time.perf_counter()
    emb = deepwalk_embeddings(G, dimensions=64, walk_length=30, num_walks=15, seed=7)
    t_emb = time.perf_counter()

    X = np.stack([emb[n] for n in sorted(G.nodes())])
    nodes_ord = sorted(G.nodes())

    louvain_partition = community_louvain.best_partition(G)
    k = len(set(louvain_partition.values()))

    t1 = time.perf_counter()
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    t2 = time.perf_counter()

    comm_sets_dw = partition_from_labels(nodes_ord, labels)
    mod_dw = nx.community.modularity(G, comm_sets_dw)

    louvain_sets = {}
    for n, cid in louvain_partition.items():
        louvain_sets.setdefault(cid, set()).add(n)
    mod_lv = nx.community.modularity(G, list(louvain_sets.values()))

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    cmap = plt.cm.tab10
    for lb in range(k):
        ns = [nodes_ord[i] for i in range(len(nodes_ord)) if labels[i] == lb]
        nx.draw_networkx_nodes(G, pos, nodelist=ns, node_color=[cmap(lb % 10)], label=str(lb))
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title(f"Karate — DeepWalk+KMeans (k={k}), Q={mod_dw:.4f}")
    plt.axis("off")
    fig_path = savefig("q2_deepwalk_kmeans.png")

    out = {
        "deepwalk_embed_sec": float(t_emb - t0),
        "kmeans_sec": float(t2 - t1),
        "modularity_deepwalk_kmeans": float(mod_dw),
        "modularity_louvain": float(mod_lv),
        "num_communities": int(k),
        "figure": str(fig_path.relative_to(ROOT)),
    }
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
