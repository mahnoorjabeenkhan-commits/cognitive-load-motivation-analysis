"""
01_prepare.py
Load the raw questionnaire export, score the three scales from their items,
and save a clean analysis-ready file.

Scale scoring follows the published instruments and matches the
pre-computed means already present in the SPSS export.
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Look for the Excel in a few common places so the script runs easily
CANDIDATES = [
    ROOT.parent / "Thesis Data File.xlsx",
    ROOT / "Thesis Data File.xlsx",
    Path("Thesis Data File.xlsx"),
]
RAW = next((p for p in CANDIDATES if p.exists()), None)
if RAW is None:
    raise FileNotFoundError(
        "Could not find 'Thesis Data File.xlsx'. "
        "Place it in the parent folder of this repo or edit the path."
    )
OUT = ROOT / "results" / "clean_data.csv"

def main():
    df = pd.read_excel(RAW)
    print(f"Loaded {len(df)} rows, {df.shape[1]} columns")

    # --- Academic Self-Efficacy (CASES, Owen & Froman, 1988) ---
    # 33 items, higher = higher self-efficacy. Scale range typically 1-5.
    ase_cols = [f"ASE{i}" for i in range(1, 34)]
    df["ASE"] = df[ase_cols].mean(axis=1)

    # --- Cognitive Load (Leppink et al., 2014) ---
    # 10 items on a 1-10 (or 1-9) scale.
    # Items 1-3 = intrinsic, 4-6 = extraneous, 7-10 = germane
    cl_cols = [f"CL{i}" for i in range(1, 11)]
    df["CL"] = df[cl_cols].mean(axis=1)
    df["CL_intrinsic"] = df[["CL1", "CL2", "CL3"]].mean(axis=1)
    df["CL_extraneous"] = df[["CL4", "CL5", "CL6"]].mean(axis=1)
    df["CL_germane"] = df[["CL7", "CL8", "CL9", "CL10"]].mean(axis=1)

    # --- Intrinsic Motivation (AMS, Vallerand et al., 1992) ---
    # Only the 12 intrinsic items are used (To Know, To Accomplish, Stimulation).
    # Column order in the file: IM1-IM6 then AM7-AM28  (= items 1 to 28 of AMS)
    ams = ["IM1", "IM2", "IM3", "IM4", "IM5", "IM6"] + [f"AM{i}" for i in range(7, 29)]
    # 1-based item numbers for the three intrinsic subscales
    imtk = [ams[i - 1] for i in [2, 9, 16, 23]]   # To Know
    imta = [ams[i - 1] for i in [6, 11, 18, 25]]  # To Accomplish
    imtes = [ams[i - 1] for i in [4, 13, 20, 27]] # Stimulation
    im_cols = imtk + imta + imtes
    df["IM"] = df[im_cols].mean(axis=1)

    # Keep demographics and the scored scales
    keep = [
        "Age", "Gender", "Education", "SES", "Birth", "FT", "AgeGroup",
        "ASE", "IM", "CL", "CL_intrinsic", "CL_extraneous", "CL_germane"
    ]
    # Some columns may be missing or named slightly differently; be tolerant
    available = [c for c in keep if c in df.columns]
    clean = df[available].copy()

    # Drop rows with missing scale scores
    clean = clean.dropna(subset=["ASE", "IM", "CL"])
    print(f"After dropping missing scale scores: N = {len(clean)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(OUT, index=False)
    print(f"Saved {OUT}")
    print(clean[["ASE", "IM", "CL"]].describe().round(3))

if __name__ == "__main__":
    main()
