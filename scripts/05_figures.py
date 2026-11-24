"""
05_figures.py
Two figures:
1. Scatter plots of the main bivariate relationships
2. Interaction: predicted self-efficacy by cognitive load at low/mean/high motivation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "clean_data.csv"
FIG1 = ROOT / "figures" / "fig_scatter.png"
FIG2 = ROOT / "figures" / "fig_interaction.png"

def main():
    df = pd.read_csv(DATA).dropna(subset=["ASE", "IM", "CL"])

    # ---------- Figure 1: two scatter plots ----------
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))

    axes[0].scatter(df["IM"], df["ASE"], alpha=0.45, s=22, color="#2c7bb6", edgecolors="none")
    # simple OLS line
    z = np.polyfit(df["IM"], df["ASE"], 1)
    xline = np.linspace(df["IM"].min(), df["IM"].max(), 100)
    axes[0].plot(xline, np.poly1d(z)(xline), color="#d7191c", lw=1.5)
    axes[0].set_xlabel("Intrinsic motivation")
    axes[0].set_ylabel("Academic self-efficacy")
    axes[0].set_title("IM and self-efficacy (r = –.14)")

    axes[1].scatter(df["CL"], df["ASE"], alpha=0.45, s=22, color="#2c7bb6", edgecolors="none")
    z2 = np.polyfit(df["CL"], df["ASE"], 1)
    xline2 = np.linspace(df["CL"].min(), df["CL"].max(), 100)
    axes[1].plot(xline2, np.poly1d(z2)(xline2), color="#d7191c", lw=1.5)
    axes[1].set_xlabel("Cognitive load")
    axes[1].set_ylabel("Academic self-efficacy")
    axes[1].set_title("Cognitive load and self-efficacy (r = .04)")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.tight_layout()
    FIG1.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG1, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {FIG1}")

    # ---------- Figure 2: interaction ----------
    df["zCL"] = (df["CL"] - df["CL"].mean()) / df["CL"].std()
    df["zIM"] = (df["IM"] - df["IM"].mean()) / df["IM"].std()
    df["zCLzIM"] = df["zCL"] * df["zIM"]
    X = sm.add_constant(df[["zCL", "zIM", "zCLzIM"]])
    m = sm.OLS(df["ASE"], X).fit()

    # Predicted values at three levels of IM
    zcl_range = np.linspace(-2, 2, 50)
    fig, ax = plt.subplots(figsize=(5.5, 4))
    colors = ["#4575b4", "#74add1", "#d73027"]
    labels = ["Low motivation (–1 SD)", "Average motivation", "High motivation (+1 SD)"]
    for zim, color, label in zip([-1, 0, 1], colors, labels):
        pred = (m.params["const"]
                + m.params["zCL"] * zcl_range
                + m.params["zIM"] * zim
                + m.params["zCLzIM"] * zcl_range * zim)
        ax.plot(zcl_range, pred, color=color, lw=2, label=label)

    ax.set_xlabel("Cognitive load (z-scored)")
    ax.set_ylabel("Predicted academic self-efficacy")
    ax.set_title("Load × motivation interaction")
    ax.legend(frameon=False, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG2, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {FIG2}")

if __name__ == "__main__":
    main()
