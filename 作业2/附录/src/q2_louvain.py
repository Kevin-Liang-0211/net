"""Q2: Louvain community detection on Zachary Karate Club."""
import json
import sys
import time
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import ROOT, ensure_dirs, savefig

from community import community_louvain


def main():
    ensure_dirs()
    G = nx.karate_club_graph()

    t0 = time.perf_counter()
    partition = community_louvain.best_partition(G)
    t1 = time.perf_counter()

    communities = {}
    for node, cid in partition.items():
        communities.setdefault(cid, set()).add(node)
    comm_sets = list(communities.values())

    mod = nx.community.modularity(G, comm_sets)

    pos = nx.spring_layout(G, seed=42, weight=None)
    cmap = plt.cm.tab10
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_edges(G, pos, alpha=0.35)
    for cid, nodes in communities.items():
        color = cmap(cid % 10)
        nx.draw_networkx_nodes(G, pos, nodelist=list(nodes), node_color=[color], label=f"C{cid}")
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title(f"Karate Club — Louvain ({len(comm_sets)} communities), Q={mod:.4f}")
    plt.axis("off")
    fig_path = savefig("q2_karate_louvain.png")

    out = {
        "algorithm": "Louvain (multilevel modularity optimization)",
        "dataset": "Zachary Karate Club",
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "num_communities": len(comm_sets),
        "modularity": float(mod),
        "runtime_sec": float(t1 - t0),
        "figure": str(fig_path.relative_to(ROOT)),
        "partition": {str(k): int(v) for k, v in partition.items()},
    }
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
