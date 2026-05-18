"""Q3: Classical centrality metrics on a small undirected network."""
import json
import sys
from pathlib import Path

import networkx as nx
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))


def build_demo_graph():
    """Small undirected graph (labels 0..6)."""
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


def rank_series(s):
    return s.rank(ascending=False, method="min").astype(int)


def main():
    G = build_demo_graph()
    nodes = sorted(G.nodes())

    deg = nx.degree_centrality(G)
    bet = nx.betweenness_centrality(G)
    clo = nx.closeness_centrality(G)
    eig = nx.eigenvector_centrality_numpy(G)

    df = pd.DataFrame(
        {
            "degree": [deg[n] for n in nodes],
            "betweenness": [bet[n] for n in nodes],
            "closeness": [clo[n] for n in nodes],
            "eigenvector": [eig[n] for n in nodes],
        },
        index=[str(n) for n in nodes],
    )
    ranks = pd.DataFrame(
        {
            "rank_degree": rank_series(df["degree"]),
            "rank_betweenness": rank_series(df["betweenness"]),
            "rank_closeness": rank_series(df["closeness"]),
            "rank_eigenvector": rank_series(df["eigenvector"]),
        },
        index=df.index,
    )
    table = pd.concat([df.round(6), ranks], axis=1)

    out = {
        "edges": list(G.edges()),
        "nodes": nodes,
        "table_csv": table.to_csv(),
    }
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
