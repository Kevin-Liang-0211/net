#!/usr/bin/env python3
"""Run all homework computations and save results_summary.json."""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))


def safe_run(fn):
    try:
        return fn()
    except Exception:
        return {"error": traceback.format_exc()}


def main():
    from q2_deepwalk_compare import main as q2_dw
    from q2_louvain import main as q2_lv
    from q3_centrality import main as q3
    from q4_pagerank import main as q4
    from q5_embedding_influence import main as q5
    from q6_analysis import main as q6

    q2_res = safe_run(q2_lv)
    q3_res = safe_run(q3)
    q4_res = safe_run(q4)
    q2dw_res = safe_run(q2_dw)
    q5_res = safe_run(q5)
    q6_res = safe_run(q6)

    bundle = {
        "q2_louvain": q2_res,
        "q2_deepwalk_compare": q2dw_res,
        "q3_centrality": q3_res,
        "q4_pagerank": q4_res,
        "q5_embedding_influence": q5_res,
        "q6_large_network": q6_res,
    }
    out_dir = ROOT / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "results_summary.json"
    out_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    return bundle


if __name__ == "__main__":
    main()
