#!/usr/bin/env python3
"""Run all experiments for homework 3."""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))


def safe(fn):
    try:
        return fn()
    except Exception:
        return {"error": traceback.format_exc()}


def main():
    from q1_one_model import main as q1
    from q2_four_models import main as q2
    from q3_er_giant import main as q3
    from q5_search import main as q5

    bundle = {"q1": safe(q1), "q2": safe(q2), "q3": safe(q3), "q5": safe(q5)}
    out = ROOT / "output" / "run_summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    import json

    out.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out}")
    return bundle


if __name__ == "__main__":
    main()
