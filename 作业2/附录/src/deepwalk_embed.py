"""DeepWalk-style random-walk embeddings (neural embedding baseline)."""
from __future__ import annotations

import random

import networkx as nx
from gensim.models import Word2Vec


def random_walk_directed(G: nx.DiGraph, start, length: int) -> list:
    walk = [start]
    cur = start
    for _ in range(length - 1):
        nbrs = list(G.successors(cur))
        if not nbrs:
            break
        cur = random.choice(nbrs)
        walk.append(cur)
    return walk


def random_walk_undirected(G: nx.Graph, start, length: int) -> list:
    walk = [start]
    cur = start
    for _ in range(length - 1):
        nbrs = list(G.neighbors(cur))
        if not nbrs:
            break
        cur = random.choice(nbrs)
        walk.append(cur)
    return walk


def deepwalk_embeddings(
    G,
    dimensions: int = 64,
    walk_length: int = 40,
    num_walks: int = 10,
    window: int = 5,
    seed: int = 42,
) -> dict:
    random.seed(seed)
    nodes = list(G.nodes())
    walks = []
    is_dir = G.is_directed()
    for _ in range(num_walks):
        random.shuffle(nodes)
        for start in nodes:
            if is_dir:
                seq = random_walk_directed(G, start, walk_length)
            else:
                seq = random_walk_undirected(G, start, walk_length)
            walks.append([str(x) for x in seq])

    model = Word2Vec(
        sentences=walks,
        vector_size=dimensions,
        window=window,
        min_count=1,
        sg=1,
        epochs=5,
        seed=seed,
        workers=1,
    )
    emb = {}
    for n in nodes:
        emb[n] = model.wv[str(n)].copy()
    return emb
