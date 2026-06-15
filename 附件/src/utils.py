"""Paths and matplotlib defaults."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "output"


def configure_matplotlib():
    import matplotlib

    matplotlib.rcParams["font.sans-serif"] = [
        "PingFang SC",
        "Arial Unicode MS",
        "Heiti TC",
        "SimHei",
        "DejaVu Sans",
    ]
    matplotlib.rcParams["axes.unicode_minus"] = False


def ensure_dirs():
    configure_matplotlib()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def savefig(name: str):
    import matplotlib.pyplot as plt

    ensure_dirs()
    path = FIG_DIR / name
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path
