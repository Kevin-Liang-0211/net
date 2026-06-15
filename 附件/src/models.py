"""Deterministic / random network constructors (Ring lattice, ER, WS, BA)."""
from __future__ import annotations

import networkx as nx


def ring_lattice_graph(n: int, k: int) -> nx.Graph:
    """Undirected ring lattice: each node connects to k/2 nearest neighbors on each side (k even)."""
    if k % 2 != 0:
        raise ValueError("k must be even for symmetric ring lattice")
    return nx.watts_strogatz_graph(n, k, p=0.0, seed=None)


def er_graph_gnm(n: int, m: int, seed: int | None = None) -> nx.Graph:
    """ER random graph with exactly M edges (G(n,m))."""
    return nx.gnm_random_graph(n, m, seed=seed)


def er_graph_gnp(n: int, p: float, seed: int | None = None) -> nx.Graph:
    """ER random graph G(n,p)."""
    return nx.erdos_renyi_graph(n, p, seed=seed)


def ws_graph(n: int, k: int, p: float, seed: int | None = None) -> nx.Graph:
    """Watts–Strogatz small-world (starts from ring lattice)."""
    return nx.watts_strogatz_graph(n, k, p=p, seed=seed)


def ba_graph(n: int, m: int, seed: int | None = None) -> nx.Graph:
    """Barabási–Albert preferential attachment."""
    return nx.barabasi_albert_graph(n, m, seed=seed)
