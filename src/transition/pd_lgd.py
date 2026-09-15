"""PD = Λ(Xβ+γC) — polars + sklearn logit, auditable.

Keep sklearn for regulator-readable coefficients; feed polars DataFrame → to_pandas() at last mile.
"""
import polars as pl
import numpy as np
from sklearn.linear_model import LogisticRegression

def fit_pd(df: pl.DataFrame):
    """Fit PD on synthetic labels (replace with real default flag when available)."""
    X = df.select(["leverage","icr","carbon_intensity"]).to_pandas()
    # synthetic default proxy: high lev + low icr + high carbon → higher p
    y = ((df["leverage"] > 2.5) & (df["icr"] < 2.0)).to_numpy().astype(int)
    # add carbon tilt
    y = np.where((df["carbon_intensity"] > 20) & (np.random.default_rng(0).random(len(y)) < 0.15), 1, y)
    clf = LogisticRegression().fit(X, y)
    print("coef", dict(zip(X.columns, clf.coef_[0].round(3))), "intercept", round(clf.intercept_[0],3))
    return clf

def predict_pd(clf, df: pl.DataFrame, carbon_shock=0.0):
    X = df.select(["leverage","icr","carbon_intensity"]).to_pandas()
    X["carbon_intensity"] = X["carbon_intensity"] * (1+carbon_shock)
    p = clf.predict_proba(X)[:,1]
    return pl.DataFrame({"id": df["id"], "PD": p})

if __name__ == "__main__":
    df = pl.scan_parquet("data/curated/exposures.parquet").collect()
    clf = fit_pd(df)
    print(predict_pd(clf, df.head(5), carbon_shock=0.25).head(5))
