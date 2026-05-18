"""Q5 optional: embedding norm influence vs PageRank / centrality on BTC OTC subgraph."""
import json
import sys
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deepwalk_embed import deepwalk_embeddings
from q4_pagerank import load_bitcoin_otc


def largest_weakly_connected_subgraph(G: nx.DiGraph, max_nodes: int = 1200) -> nx.DiGraph:
    comps = sorted(nx.weakly_connected_components(G), key=len, reverse=True)
    nodes = list(comps[0])
    if len(nodes) > max_nodes:
        nodes = nodes[:max_nodes]
        G = G.subgraph(nodes).copy()
        largest = max(nx.weakly_connected_components(G), key=len)
        G = G.subgraph(largest).copy()
    else:
        G = G.subgraph(nodes).copy()
    return G


def main():
    G_full = load_bitcoin_otc()
    G = largest_weakly_connected_subgraph(G_full, max_nodes=900)

    Gu = G.to_undirected()

    pr = nx.pagerank(G, alpha=0.85, weight="weight")
    deg_c = nx.degree_centrality(Gu)
    bet_u = nx.betweenness_centrality(Gu)

    emb = deepwalk_embeddings(G, dimensions=48, walk_length=25, num_walks=12, seed=11)
    influence = {n: float(np.linalg.norm(emb[n], ord=2)) for n in G.nodes()}

    nodes = list(G.nodes())
    s_inf = pd.Series({n: influence[n] for n in nodes})
    s_pr = pd.Series(pr)
    s_deg = pd.Series({n: deg_c[n] for n in nodes})
    s_bet = pd.Series({n: bet_u.get(n, 0.0) for n in nodes})

    rho_pr, _ = spearmanr(s_inf.values, s_pr.values)
    rho_deg, _ = spearmanr(s_inf.values, s_deg.values)
    rho_bet, _ = spearmanr(s_inf.values, s_bet.values)

    top_inf = s_inf.sort_values(ascending=False).head(15)

    out = {
        "note": "DeepWalk embedding L2 norm as shallow neural influence proxy",
        "subgraph_nodes": G.number_of_nodes(),
        "subgraph_edges": G.number_of_edges(),
        "spearman_inf_vs_pagerank": float(rho_pr),
        "spearman_inf_vs_degree_cent": float(rho_deg),
        "spearman_inf_vs_betweenness": float(rho_bet),
        "top15_embedding_influence": [{str(int(k)): float(v)} for k, v in top_inf.items()],
    }
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
