"""Network metrics with formulas documented in docstrings (Chinese labels for export)."""
from __future__ import annotations

import math

import networkx as nx


def edge_count(G: nx.Graph) -> int:
    return int(G.number_of_edges())


def average_degree(G: nx.Graph) -> float:
    """bar k = 2m/n for undirected simple graph."""
    n = G.number_of_nodes()
    if n == 0:
        return 0.0
    return 2.0 * G.number_of_edges() / n


def density(G: nx.Graph) -> float:
    """rho = 2m/(n(n-1)) for simple undirected."""
    return float(nx.density(G))


def diameter_and_avg_path(G: nx.Graph):
    """Diameter & average shortest path on largest connected component."""
    if G.number_of_nodes() == 0:
        return math.nan, math.nan
    if nx.is_connected(G):
        H = G
    else:
        nodes = max(nx.connected_components(G), key=len)
        H = G.subgraph(nodes).copy()
    diam = nx.diameter(H)
    apl = nx.average_shortest_path_length(H)
    return int(diam), float(apl)


def clustering_average(G: nx.Graph) -> float:
    """Average clustering coefficient (triadic closure)."""
    return float(nx.average_clustering(G))


def degree_distribution(G: nx.Graph) -> dict[int, int]:
    deg = dict(G.degree())
    hist: dict[int, int] = {}
    for _, d in deg.items():
        hist[d] = hist.get(d, 0) + 1
    return dict(sorted(hist.items()))
