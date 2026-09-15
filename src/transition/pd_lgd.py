"""PD = Λ(Xβ+γC) — polars + sklearn logit, auditable."""
import polars as pl
import numpy as np
from sklearn.linear_model import LogisticRegression

def fit_pd(df: pl.DataFrame):
    X = df.select(["leverage","icr","carbon_intensity"]).to_pandas()
    y = ((df["leverage"] > 2.5) & (df["icr"] < 2.0)).to_numpy().astype(int)
    # add carbon tilt: 15% of high-carbon borrowers flip to 1
    rng = np.random.default_rng(0)
    mask = (df["carbon_intensity"] > 20).to_numpy() & (rng.random(len(y)) < 0.15)
    y = np.where(mask, 1, y)
    clf = LogisticRegression(max_iter=500).fit(X, y)
    print("coef", dict(zip(X.columns, clf.coef_[0].round(3))), "intercept", round(clf.intercept_[0],3))
    return clf

def predict_pd(clf, df: pl.DataFrame, carbon_shock=0.0):
    X = df.select(["leverage","icr","carbon_intensity"]).to_pandas()
    X["carbon_intensity"] = X["carbon_intensity"] * (1+carbon_shock)
    p = clf.predict_proba(X)[:,1]
    return pl.DataFrame({"id": df["id"], "PD": p})
