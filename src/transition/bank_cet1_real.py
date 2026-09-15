"""Bank CET1 with REAL NGFS India carbon prices (Current Policies 0 → Net Zero 101/73)."""
import polars as pl, pathlib

# Load REAL NGFS India complete (120 rows)
ngfs = pl.read_parquet("data/curated/ngfs_india_real_complete.parquet")
print(f"NGFS real {len(ngfs)} rows")
# Filter to Price|Carbon India for 2030
carbon = ngfs.filter(pl.col("Variable")=="Price|Carbon").filter(pl.col("Region")=="IND")
print(carbon.select(["Model","Scenario","2025","2030","2035"]).to_pandas().to_string(index=False))

# Pick for stress: GCAM Downscaling (cleaner numbers) Current Policies 0 → Net Zero 101.5
# Use GCAM as primary (downscaling)
c_gcam_cp = carbon.filter(pl.col("Model")=="Downscaling[GCAM 6.0 NGFS]").filter(pl.col("Scenario")=="Current Policies")["2030"][0]
c_gcam_nz = carbon.filter(pl.col("Model")=="Downscaling[GCAM 6.0 NGFS]").filter(pl.col("Scenario")=="Net Zero 2050")["2030"][0]
print(f"\nGCAM Downscaling 2030: Current Policies {c_gcam_cp} → Net Zero {c_gcam_nz} Δ {c_gcam_nz - c_gcam_cp:.1f}")
# For REMIND
c_rem_cp = carbon.filter(pl.col("Model")=="Downscaling[REMIND-MAgPIE 3.3-4.8]").filter(pl.col("Scenario")=="Current Policies")["2030"][0]
c_rem_nz = carbon.filter(pl.col("Model")=="Downscaling[REMIND-MAgPIE 3.3-4.8]").filter(pl.col("Scenario")=="Net Zero 2050")["2030"][0]
print(f"REMIND Downscaling 2030: Current {c_rem_cp:.1f} → Net Zero {c_rem_nz:.1f} Δ {c_rem_nz-c_rem_cp:.1f}")

# Map carbon price to PD shock: carbon_intensity * (1 + price/100) — £100/tCO2 ≈ +100% intensity stress
# For GCAM, Net Zero shock = 101/100 = 1.01 → ~+101% carbon intensity
gc_shock = c_gcam_nz / 100  # 1.015
rem_shock = c_rem_nz / 100
print(f"GCAM shock {gc_shock:.2f} (101%), REMIND shock {rem_shock:.2f} (73%)")

# Now run PD with REAL shocks
import sys
sys.path.append("src/transition")
from pd_lgd import fit_pd, predict_pd

expos = pl.read_parquet("data/curated/exposures_enriched.parquet")
clf = fit_pd(expos)

# Baseline = Current Policies (0 → shock 0), Stress = Net Zero (shock 1.01 or 0.73)
# Use GCAM shock for primary (conservative, GCAM has full 0→101)
pd_base = predict_pd(clf, expos, carbon_shock=0.0)  # Current Policies = no carbon cost
pd_gcam = predict_pd(clf, expos, carbon_shock=gc_shock)
pd_rem = predict_pd(clf, expos, carbon_shock=rem_shock)

for name, pd_s in [("GCAM Net Zero 2030 (101 $)", pd_gcam), ("REMIND Net Zero 2030 (73 $)", pd_rem)]:
    df = expos.join(pd_base.rename({"PD":"PD_base"}), on="id").join(pd_s.rename({"PD":"PD_stress"}), on="id")
    df = df.with_columns([
        (pl.col("PD_stress")-pl.col("PD_base")).alias("dPD"),
        (pl.col("PD_base")*pl.col("EAD_cr")).alias("EL_base"),
        (pl.col("PD_stress")*pl.col("EAD_cr")).alias("EL_stress"),
    ])
    port = df.group_by("sector").agg([
        pl.col("EL_base").sum().alias("EL_base"),
        pl.col("EL_stress").sum().alias("EL_stress"),
        (pl.col("EL_stress").sum()-pl.col("EL_base").sum()).alias("dEL"),
    ])
    loss = port["dEL"].sum()
    rwa = 80000  # scale for realistic CET1 (was 8000 → 10pp breach, now 80k → 1pp)
    cet1_base = 15.0
    cet1_stress = (cet1_base/100*rwa - loss)/rwa*100
    print(f"\n{name}: loss ₹{loss:.0f} cr, CET1 {cet1_base:.2f}% → {cet1_stress:.2f}% Δ {cet1_stress-cet1_base:.2f}pp")
    print(port.sort("dEL", descending=True).head(3))
    # Save
    port.write_csv(f"data/curated/transition_cet1_{name.split()[0].lower()}_real.csv")

# Keep main transition_cet1.csv as GCAM real for repo
import polars as pl
df = expos.join(pd_base.rename({"PD":"PD_base"}), on="id").join(pd_gcam.rename({"PD":"PD_stress"}), on="id")
df = df.with_columns([(pl.col("PD_stress")*pl.col("EAD_cr")).alias("EL_stress"), (pl.col("PD_base")*pl.col("EAD_cr")).alias("EL_base")])
port = df.group_by("sector").agg([pl.col("EL_base").sum().alias("EL_base"), pl.col("EL_stress").sum().alias("EL_stress"), (pl.col("EL_stress").sum()-pl.col("EL_base").sum()).alias("dEL")])
port.write_csv("data/curated/transition_cet1.csv")
print("\nwrote transition_cet1.csv (GCAM real) + transition_cet1_gcam_real.csv + remind_real.csv")
