"""
04_regression.py
Multiple regression predicting academic self-efficacy from cognitive load
and intrinsic motivation, plus the load × motivation interaction.
Uses HC3 robust standard errors.
Also reports simple slopes of load at low / mean / high motivation.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "clean_data.csv"
OUT_COEF = ROOT / "results" / "regression_coefficients.csv"
OUT_SUM = ROOT / "results" / "regression_summary.csv"
OUT_SLOPES = ROOT / "results" / "simple_slopes.csv"

def main():
    df = pd.read_csv(DATA).dropna(subset=["ASE", "IM", "CL"])
    n = len(df)
    print(f"N = {n}")

    # Standardize predictors so coefficients are comparable
    df["zCL"] = (df["CL"] - df["CL"].mean()) / df["CL"].std()
    df["zIM"] = (df["IM"] - df["IM"].mean()) / df["IM"].std()
    df["zCLzIM"] = df["zCL"] * df["zIM"]

    # Model 1: main effects only
    X1 = sm.add_constant(df[["zCL", "zIM"]])
    m1 = sm.OLS(df["ASE"], X1).fit(cov_type="HC3")

    # Model 2: + interaction
    X2 = sm.add_constant(df[["zCL", "zIM", "zCLzIM"]])
    m2 = sm.OLS(df["ASE"], X2).fit(cov_type="HC3")

    # Collect coefficients
    rows = []
    for label, model in [("Model 1 (main effects)", m1), ("Model 2 (+ interaction)", m2)]:
        for term in model.params.index:
            rows.append({
                "model": label,
                "term": term,
                "b": round(model.params[term], 4),
                "se": round(model.bse[term], 4),
                "p": f"{model.pvalues[term]:.3f}" if model.pvalues[term] >= 0.001 else "< .001",
                "95% CI": f"[{model.conf_int().loc[term, 0]:.3f}, {model.conf_int().loc[term, 1]:.3f}]",
            })
    pd.DataFrame(rows).to_csv(OUT_COEF, index=False)

    # Model summaries
    summary = pd.DataFrame([
        {
            "model": "Model 1 (main effects)",
            "R2": round(m1.rsquared, 3),
            "adj_R2": round(m1.rsquared_adj, 3),
            "F": round(m1.fvalue, 2),
            "p(F)": f"{m1.f_pvalue:.3f}",
        },
        {
            "model": "Model 2 (+ interaction)",
            "R2": round(m2.rsquared, 3),
            "adj_R2": round(m2.rsquared_adj, 3),
            "F": round(m2.fvalue, 2),
            "p(F)": f"{m2.f_pvalue:.3f}",
        },
    ])
    summary.to_csv(OUT_SUM, index=False)
    print(summary)

    # Simple slopes of CL at low (-1 SD), mean, high (+1 SD) IM
    # From Model 2: ASE = b0 + b1*zCL + b2*zIM + b3*zCL*zIM
    # Slope of zCL = b1 + b3 * zIM
    b1 = m2.params["zCL"]
    b3 = m2.params["zCLzIM"]
    # Approximate SE for simple slopes (Aiken & West style)
    # Using the variance-covariance matrix
    cov = m2.cov_params()
    def slope_se(zim):
        # var(b1 + b3*zim) = var(b1) + zim^2 * var(b3) + 2*zim*cov(b1,b3)
        return np.sqrt(cov.loc["zCL", "zCL"] + zim**2 * cov.loc["zCLzIM", "zCLzIM"]
                       + 2 * zim * cov.loc["zCL", "zCLzIM"])

    slopes = []
    for label, zim in [("low motivation (-1 SD)", -1.0),
                       ("average motivation", 0.0),
                       ("high motivation (+1 SD)", 1.0)]:
        slope = b1 + b3 * zim
        se = slope_se(zim)
        t = slope / se
        from scipy import stats
        p = 2 * (1 - stats.t.cdf(abs(t), df=m2.df_resid))
        slopes.append({
            "motivation": label,
            "slope of load": round(slope, 3),
            "se": round(se, 3),
            "p": f"{p:.3f}" if p >= 0.001 else "< .001",
        })
    pd.DataFrame(slopes).to_csv(OUT_SLOPES, index=False)
    print("\nSimple slopes of cognitive load:")
    print(pd.DataFrame(slopes).to_string(index=False))

    print("\n--- Model 2 coefficients ---")
    print(m2.summary().tables[1])

if __name__ == "__main__":
    main()
