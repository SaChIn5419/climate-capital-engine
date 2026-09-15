"""Fetch NGFS Phase V + Short-term via IIASA pyam → GeoParquet/Parquet via Polars.

Requires: CDS/IIASA access. For MVP without token, falls back to sample CSV.
pip: pyam, polars, httpx
"""
import pathlib
import polars as pl

RAW = pathlib.Path("data/raw/ngfs")
CUR = pathlib.Path("data/curated")
RAW.mkdir(parents=True, exist_ok=True)
CUR.mkdir(parents=True, exist_ok=True)

def fetch_sample():
    # Sample structure mimicking IIASA export (replace with pyam pull when you have access)
    print("→ No NGFS token: writing SAMPLE ngfs_sample.parquet (replace with pyam fetch)")
    df = pl.DataFrame({
        "model": ["REMIND-MAgPIE"]*6,
        "scenario": ["Net Zero 2050","Current Policies","Highway to Paris"]*2,
        "region": ["India"]*6,
        "variable": ["Carbon Price|ETS","GDP|PPP","Primary Energy|Coal"]*2,
        "unit": ["USD2020/tCO2","billion USD2020","EJ/yr"]*2,
        "2025": [10, 4800, 8, 5, 4700, 10],
        "2030": [90, 6800, 5, 12, 6500, 9],
    })
    out = CUR / "ngfs_sample.parquet"
    df.write_parquet(out)
    print(f"wrote {out} — rows {len(df)}")
    # Polars lazy example
    q = pl.scan_parquet(out).filter(pl.col("scenario")=="Net Zero 2050").collect()
    print(q)

if __name__ == "__main__":
    fetch_sample()
    print("Done. For real data: python -m pyam download via IIASA Explorer (see registry.csv)")
