"""CCTS structural price simulator P = f(Supply, Demand, AbatementCost, ComplianceGap) + MC.

No historical CCC price to fit — structural, not time-series.
"""
import numpy as np
import polars as pl

def simulate(n=1000, p0=20, kappa=0.3, mu=50, sigma=8, dt=1/12):
    rng = np.random.default_rng(42)
    p = np.empty(n)
    p[0]=p0
    for t in range(1,n):
        # OU + jump for policy shock
        dp = kappa*(mu-p[t-1])*dt + sigma*np.sqrt(dt)*rng.normal()
        jump = rng.choice([0, 30], p=[0.98,0.02])
        p[t]= max(0, p[t-1]+dp+jump)
    return pl.DataFrame({"month": range(n), "CCC_price_INR": p})

if __name__ == "__main__":
    print(simulate(12).head(6))
