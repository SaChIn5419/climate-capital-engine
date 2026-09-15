"""Bank CET1 stress: NGFS sample → PD shock → EL → CET1 depletion + reverse stress."""
import polars as pl, pathlib, duckdb

# Load NGFS sample (will be replaced by real when user drops CSV)
ngfs = pl.scan_parquet("data/curated/ngfs_sample.parquet").collect()
print("NGFS sample", ngfs.head(3))

# Load exposures enriched
expos = pl.scan_parquet("data/curated/exposures_enriched.parquet").collect()
print(f"exposures {len(expos)}")

# Simple PD shock: carbon price 90 (Net Zero) vs 12 (Current Policies) → +25% carbon intensity stress
# Use pd_lgd logic: leverage + carbon → PD
import sys
sys.path.append("src/transition")
from pd_lgd import fit_pd, predict_pd

clf = fit_pd(expos)
# Baseline PD
pd_base = predict_pd(clf, expos, carbon_shock=0.0)
pd_stress = predict_pd(clf, expos, carbon_shock=0.25)  # +25% carbon price

# Join to exposures
df = expos.join(pd_base.rename({"PD":"PD_base"}), on="id").join(pd_stress.rename({"PD":"PD_stress"}), on="id")
df = df.with_columns([
    (pl.col("PD_stress")-pl.col("PD_base")).alias("dPD"),
    (pl.col("PD_base")*pl.col("EAD_cr")).alias("EL_base"),
    (pl.col("PD_stress")*pl.col("EAD_cr")).alias("EL_stress"),
])
print(df.select(["id","sector","PD_base","PD_stress","dPD","EL_base","EL_stress"]).head(5))
# Portfolio
port = df.group_by("sector").agg([
    pl.col("EL_base").sum().alias("EL_base"),
    pl.col("EL_stress").sum().alias("EL_stress"),
    (pl.col("EL_stress").sum()-pl.col("EL_base").sum()).alias("dEL"),
])
print("Portfolio EL by sector (₹ cr)")
print(port.sort("dEL", descending=True))

# Bank CET1 (assume CET1 15%, RWA 1000 cr per sector proxy)
import numpy as np
cet1_base = 15.0
rwa = 8000
loss = port["dEL"].sum()
cet1_stress = (cet1_base/100 * rwa - loss) / rwa * 100
print(f"\nBank: CET1 {cet1_base:.2f}% → {cet1_stress:.2f}% (loss ₹{loss:.1f} cr) Δ {cet1_stress-cet1_base:.2f}pp")
# Reverse stress: what carbon shock makes CET1 < 9%?
for shock in [0.25,0.5,0.75,1.0,1.5,2.0]:
    pd_s = predict_pd(clf, expos, carbon_shock=shock)
    d = expos.join(pd_s.rename({"PD":"P"}), on="id").with_columns((pl.col("P")*pl.col("EAD_cr")).alias("EL"))
    loss_s = d["EL"].sum() - df["EL_base"].sum()
    cet1 = (cet1_base/100*rwa - loss_s)/rwa*100
    print(f" shock +{shock*100:.0f}% → loss {loss_s:.0f} cet1 {cet1:.2f}% {'BREACH' if cet1<9 else ''}")
    if cet1<9:
        break

# Save results
out = pathlib.Path("data/curated/transition_cet1.csv")
port.write_csv(out)
print(f"wrote {out}")
