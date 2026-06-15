"""Question 3 (numerical): ER giant component emergence vs p."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import ROOT, ensure_dirs, savefig


def giant_fraction(G: nx.Graph) -> float:
    if G.number_of_nodes() == 0:
        return 0.0
    comps = nx.connected_components(G)
    giant = max(comps, key=len)
    return len(giant) / G.number_of_nodes()


def simulate(n: int, ps: np.ndarray, repeats: int = 40, seed: int = 0):
    rng = np.random.default_rng(seed)
    rows = []
    for p in ps:
        fracs = []
        for _ in range(repeats):
            G = nx.erdos_renyi_graph(n, float(p), seed=int(rng.integers(1 << 30)))
            fracs.append(giant_fraction(G))
        rows.append({"p": float(p), "mean_frac": float(np.mean(fracs)), "std_frac": float(np.std(fracs))})
    return rows


def theoretical_curve(n: int, ps: np.ndarray):
    """Large-n heuristic: solve S = 1 - exp(-c S), c = (n-1)p ~ np."""
    ys = []
    for p in ps:
        c = (n - 1) * float(p)
        if c <= 1:
            ys.append(0.0)
            continue
        S = 0.75
        for _ in range(200):
            S_new = 1 - np.exp(-c * S)
            if abs(S_new - S) < 1e-8:
                break
            S = S_new
        ys.append(float(max(0.0, S)))
    return ys


def main():
    ensure_dirs()
    n = 400
    ps = np.linspace(0.0005, 0.02, 35)
    rows = simulate(n, ps, repeats=30, seed=3)
    theory = theoretical_curve(n, ps)

    plt.figure(figsize=(7, 5))
    plt.errorbar(
        [r["p"] for r in rows],
        [r["mean_frac"] for r in rows],
        yerr=[r["std_frac"] for r in rows],
        fmt="-o",
        ms=3,
        capsize=2,
        label="仿真：巨连通分量节点占比（均值±std）",
    )
    plt.plot(ps, theory, "--", label="平均场近似：S≈1-exp(-cS), c=(n-1)p")
    plt.axvline(1 / (n - 1), color="gray", linestyle=":", label=f"临界点 p≈1/(n-1)≈{1/(n-1):.5f}")
    plt.xlabel("连边概率 p")
    plt.ylabel("最大连通分量占比")
    plt.title(f"ER G(n,p) 巨片涌现（n={n}）")
    plt.legend(fontsize=9)
    fig_path = savefig("q3_giant_component.png")

    out = {
        "n": n,
        "note": "数值演示巨片随 p 增大突然出现；教材极限理论给出阈值为 np→1。",
        "critical_p_approx": float(1 / (n - 1)),
        "curve_csv": "\n".join([",".join(["p", "mean_frac", "std_frac"])] + [f'{r["p"]:.8f},{r["mean_frac"]:.6f},{r["std_frac"]:.6f}' for r in rows]),
        "figure": str(fig_path.relative_to(ROOT)),
    }
    out_path = ROOT / "output" / "q3_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
