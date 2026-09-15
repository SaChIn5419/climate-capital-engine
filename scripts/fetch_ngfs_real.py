"""NGFS real fetch — IIASA Scenario Explorer requires browser login, so provide manual + pyam stub.
Free, no key beyond IIASA email registration. Data stays in data/raw/ngfs/ (ignored).
See: https://data.ene.iiasa.ac.at/ngfs/#/workspaces
"""
import pathlib, polars as pl, httpx
RAW = pathlib.Path("data/raw/ngfs")
CUR = pathlib.Path("data/curated")
RAW.mkdir(parents=True, exist_ok=True)

def fetch_ngfs_sample_real():
    """Create realistic NGFS structure from public NGFS Scenario Explorer export (manual).
    User: go to https://data.ene.iiasa.ac.at/ngfs → Download → CSV → place in data/raw/ngfs/
    This stub converts it to parquet via Polars lazy.
    """
    import pathlib
    raws = list(RAW.glob("*.csv")) + list(RAW.glob("*.xlsx"))
    if not raws:
        print("No NGFS CSV in data/raw/ngfs/ — using sample + instructions")
        print("→ Go to https://data.ene.iiasa.ac.at/ngfs/#/workspaces → Select: Model=REMIND-MAgPIE, Scenario=Net Zero 2050|Current Policies, Region=India, Variables=Carbon Price|GDP|Primary Energy → Download CSV → move to data/raw/ngfs/")
        # Keep existing sample
        return pathlib.Path("data/curated/ngfs_sample.parquet")
    for f in raws:
        print(f"Converting {f}")
        df = pl.read_csv(f, infer_schema_length=10000) if f.suffix==".csv" else pl.read_excel(f)
        out = CUR / f"ngfs_{f.stem}.parquet"
        df.write_parquet(out)
        print(f"✓ {out} {len(df)} rows")
        return out
    return None

if __name__ == "__main__":
    fetch_ngfs_sample_real()
    print("NGFS ready — see data/curated/ngfs_sample.parquet (replace with real export when downloaded)")
