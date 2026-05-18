"""Render LaTeX-like formulas as PNG via matplotlib mathtext for embedding in Word."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def render_equation_png(
    latex: str,
    dest: Path,
    *,
    fontsize: float = 13.5,
    height_in: float = 1.0,
    dpi: int = 220,
) -> Path:
    """
    latex: mathtext fragment WITHOUT outer $...$.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig_w = min(14.5, max(4.8, 0.09 * max(len(latex), 20)))
    fig = plt.figure(figsize=(fig_w, height_in))
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, ha="center", va="center")
    fig.savefig(dest, dpi=dpi, bbox_inches="tight", transparent=True, pad_inches=0.04)
    plt.close(fig)
    return dest
