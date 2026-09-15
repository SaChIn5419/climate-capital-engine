"""Integrated waterfall: Transition (NGFS real) + Physical (WRI 10yr + IBTrACS) → CET1."""
import polars as pl, pathlib, duckdb

# Load real
trans = pl.read_csv("data/curated/transition_cet1.csv")  # GCAM real dEL per sector
phys = pl.read_parquet("data/curated/loss_real.parquet").group_by("sector").agg(pl.col("loss_cr").sum().alias("phys_gross"))
# Scale physical gross to EL-like (LGD 45% * PD impact 10% ≈ 0.05)
phys = phys.with_columns((pl.col("phys_gross")*0.05).alias("phys_EL"))
integ = trans.join(phys, on="sector", how="left").with_columns(pl.col("phys_EL").fill_null(0))
integ = integ.with_columns((pl.col("dEL")+pl.col("phys_EL")).alias("total_EL"))
print("Integrated per sector (₹ cr) — transition dEL + phys_EL (5% of gross)")
print(integ.sort("total_EL", descending=True))

# Bank waterfall: RWA 100k, CET1 15% = 15k capital
rwa=100000
cet1_base=15.0
cap_base=cet1_base/100*rwa
trans_loss=integ["dEL"].sum()
phys_loss=integ["phys_EL"].sum()
total=trans_loss+phys_loss
cet1_trans=(cap_base-trans_loss)/rwa*100
cet1_both=(cap_base-total)/rwa*100

print(f"\nWaterfall RWA {rwa} CET1 base {cet1_base}% cap {cap_base:.0f}")
print(f"  Transition GCAM 101$ dEL {trans_loss:.0f} → CET1 {cet1_trans:.2f}% Δ {cet1_trans-cet1_base:.2f}pp")
print(f"  Physical 5% gross {phys_loss:.0f} (IBTrACS 50km buffer) → CET1 both {cet1_both:.2f}% Δ {cet1_both-cet1_base:.2f}pp")
print(f"  Total {total:.0f}")

# Save waterfall CSV for Altair/web
import csv
with open("data/curated/integrated_waterfall.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["step","loss_cr","cet1","label"])
    w.writerow(["Base",0,cet1_base,"CET1 15.00%"])
    w.writerow(["Transition (NGFS GCAM 101$)",round(trans_loss,1),round(cet1_trans,2),f"Transition -{cet1_base-cet1_trans:.2f}pp"])
    w.writerow(["Physical (IBTrACS 5% gross)",round(phys_loss,1),round(cet1_both,2),f"Physical -{cet1_trans-cet1_both:.2f}pp"])
    w.writerow(["Combined",round(total,1),round(cet1_both,2),f"Combined {cet1_both:.2f}%"])

# Also save per-sector integrated for map concentration
integ.write_csv("data/curated/integrated_per_sector.csv")
print("\nwrote integrated_waterfall.csv + integrated_per_sector.csv")
print(integ.head(7))
# Copy to web
import shutil
shutil.copy("data/curated/integrated_waterfall.csv","web/public/data/integrated_waterfall.csv")
shutil.copy("data/curated/integrated_per_sector.csv","web/public/data/integrated_per_sector.csv")
print("copied to web/public/data")
