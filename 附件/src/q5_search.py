"""Question 5: BFS shortest path length, max-degree greedy walk, random walk search."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import ROOT, ensure_dirs, savefig

# 与课件示意图一致的拓扑（15 个顶点）：s—N1—…—t，左侧 hub H1 连接三片叶与主干；右侧经 N5/N7 连向 t。
# 顶点编号：s=0，N1=1，H1=2，叶 L1–L3 = 3–5，N2–N9 = 6–13，t=14。
OFFICIAL_EDGE_LIST = [
    (0, 1),
    (1, 2),
    (1, 10),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (2, 8),
    (6, 7),
    (7, 8),
    (7, 9),
    (8, 9),
    (8, 10),
    (9, 10),
    (9, 11),
    (9, 14),
    (10, 11),
    (10, 12),
    (11, 12),
    (11, 14),
    (12, 13),
]

REFERENCE_PNG_CANDIDATES = [
    ROOT / "figures" / "q5_reference.png",
    Path.home()
    / ".cursor/projects/Users-xiaotaiyang-Downloads/assets/__1-bd5ccb65-3fdd-4393-b749-2578ef6b0364.png",
]


def build_assignment_graph() -> tuple[nx.Graph, dict[int, str]]:
    G = nx.Graph()
    G.add_edges_from(OFFICIAL_EDGE_LIST)
    labels = {0: "s", 14: "t"}
    return G, labels


def copy_official_diagram_to_figures() -> Path | None:
    """若存在课件原图 PNG，则复制为 figures/q5_graph.png 供 Word 引用。"""
    ensure_dirs()
    dst = ROOT / "figures" / "q5_graph.png"
    for src in REFERENCE_PNG_CANDIDATES:
        if src.is_file():
            shutil.copy2(src, dst)
            return dst
    return None


def draw_fallback_graph(G: nx.Graph, labels: dict[int, str]) -> Path:
    pos = nx.spring_layout(G, seed=42, k=0.45 / np.sqrt(G.number_of_nodes()))
    plt.figure(figsize=(8, 5))
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels={n: labels.get(n, str(n)) for n in G.nodes()},
        node_size=520,
        font_size=9,
    )
    plt.title("题5：网络拓扑（自动布局，备用）")
    return savefig("q5_graph.png")


def bfs_shortest_hops(G: nx.Graph, s: int, t: int) -> int:
    return nx.shortest_path_length(G, s, t)


def max_degree_walk(G: nx.Graph, s: int, t: int, max_steps: int = 5000) -> tuple[int, bool]:
    steps = 0
    v = s
    prev = None
    while v != t and steps < max_steps:
        nbrs = list(G.neighbors(v))
        if not nbrs:
            break
        cand = [u for u in nbrs if u != prev]
        pool = cand if cand else nbrs
        nxt = max(pool, key=lambda u: (G.degree(u), -nx.shortest_path_length(G, u, t)))
        prev, v = v, nxt
        steps += 1
    return steps, v == t


def random_walk_mean_steps(G: nx.Graph, s: int, t: int, trials: int = 800, max_steps: int = 200000, seed: int = 21):
    rng = np.random.default_rng(seed)
    lengths = []
    hits = 0
    for _ in range(trials):
        steps = 0
        v = s
        while v != t and steps < max_steps:
            nbrs = list(G.neighbors(v))
            v = int(rng.choice(nbrs))
            steps += 1
        if v == t:
            lengths.append(steps)
            hits += 1
    return float(np.mean(lengths)) if lengths else float("nan"), hits / trials


def main():
    ensure_dirs()
    G, labels = build_assignment_graph()
    s, t = 0, 14

    fig_src = copy_official_diagram_to_figures()
    if fig_src is None:
        fig_src = draw_fallback_graph(G, labels)

    bfs_len = bfs_shortest_hops(G, s, t)
    md_steps, md_ok = max_degree_walk(G, s, t)
    rw_mean, rw_hit_rate = random_walk_mean_steps(G, s, t)

    out = {
        "note": "拓扑与教材插图一致（15 点）；插图优先使用 figures/q5_reference.png 或 Cursor 资源副本生成 figures/q5_graph.png。",
        "nodes": list(G.nodes()),
        "edges": [list(e) for e in G.edges()],
        "s": s,
        "t": t,
        "bfs_shortest_path_length_edges": int(bfs_len),
        "max_degree_walk_steps": int(md_steps),
        "max_degree_walk_success": bool(md_ok),
        "random_walk_mean_steps_est": float(rw_mean),
        "random_walk_hit_rate": float(rw_hit_rate),
        "figure": str(fig_src.relative_to(ROOT)),
    }

    out_path = ROOT / "output" / "q5_search.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
