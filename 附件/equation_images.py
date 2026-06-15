"""
将公式渲染为 PNG 嵌入 Word（Matplotlib mathtext）。

编写约定（避免解析失败）：
- 比较符使用 \\leq \\geq，不要用 \\le \\ge
- 范数使用 \\Vert ... \\Vert，少用 \\| \\|
- 复杂多式可用 \\begin{array}{l} ... \\end{array}
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.rcParams["mathtext.fontset"] = "dejavusans"

import matplotlib.pyplot as plt


def render_equation_png(
    latex: str,
    dest: Path,
    *,
    fontsize: float = 13.5,
    height_in: float = 1.05,
    dpi: int = 220,
) -> Path:
    """latex 为 mathtext 片段，勿自带外层 $。"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig_w = min(14.8, max(4.8, 0.085 * max(len(latex), 22)))
    fig = plt.figure(figsize=(fig_w, height_in))
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    try:
        ax.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, ha="center", va="center")
        fig.savefig(dest, dpi=dpi, bbox_inches="tight", transparent=True, pad_inches=0.05)
    except Exception as e:
        plt.close(fig)
        raise RuntimeError(f"公式 mathtext 解析失败，请检查 LaTeX 片段：{latex!r}") from e
    plt.close(fig)
    return dest
