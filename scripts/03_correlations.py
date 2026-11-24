"""
03_correlations.py
Pearson correlations among the three main variables (and the CL subscales).
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "clean_data.csv"
OUT = ROOT / "results" / "correlations.csv"

def pearson_row(x, y, name):
    r, p = stats.pearsonr(x, y)
    n = len(x.dropna())
    # simple Fisher CI
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    lo, hi = np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)
    return {
        "pair": name,
        "r": round(r, 3),
        "95% CI": f"[{lo:.3f}, {hi:.3f}]",
        "p": f"{p:.3f}" if p >= 0.001 else "< .001",
        "n": n,
    }

def main():
    df = pd.read_csv(DATA)
    rows = []
    rows.append(pearson_row(df["ASE"], df["IM"], "ASE × IM"))
    rows.append(pearson_row(df["ASE"], df["CL"], "ASE × CL (total)"))
    rows.append(pearson_row(df["IM"], df["CL"], "IM × CL (total)"))
    rows.append(pearson_row(df["ASE"], df["CL_intrinsic"], "ASE × Intrinsic load"))
    rows.append(pearson_row(df["ASE"], df["CL_extraneous"], "ASE × Extraneous load"))
    rows.append(pearson_row(df["ASE"], df["CL_germane"], "ASE × Germane load"))
    rows.append(pearson_row(df["IM"], df["CL_intrinsic"], "IM × Intrinsic load"))
    rows.append(pearson_row(df["IM"], df["CL_extraneous"], "IM × Extraneous load"))
    rows.append(pearson_row(df["IM"], df["CL_germane"], "IM × Germane load"))

    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)
    print(out.to_string(index=False))

if __name__ == "__main__":
    main()
