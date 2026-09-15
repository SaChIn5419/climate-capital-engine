"""Build 10k synthetic loan exposures → GeoParquet (no PostGIS).

Polars + DuckDB Spatial + Shapely.
Each exposure: id, sector, geom (WKB), value, leverage, icr, carbon_intensity, EAD, maturity
Calibrated to RBI sector credit + BRSR assets/geography (transparent synthetic).
"""
import pathlib
import polars as pl
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

OUT = pathlib.Path("data/curated/exposures.parquet")
OUT.parent.mkdir(parents=True, exist_ok=True)
N = 10000
SECTORS = ["Power","Steel","Cement","Transport","Oil & Gas","Real Estate","Other"]
W = [0.22,0.18,0.14,0.12,0.10,0.14,0.10]  # plausible concentration

rng = np.random.default_rng(42)
sectors = rng.choice(SECTORS, size=N, p=W)
# India bbox approx: lon 68-97, lat 8-35; concentrate around Mumbai/Chennai/Delhi corridors
lons = rng.normal(72.8, 5, N).clip(68,97)
lats = rng.normal(20, 5, N).clip(8,35)

df = pl.DataFrame({
    "id": range(N),
    "sector": sectors,
    "lon": lons,
    "lat": lats,
    "value_cr": rng.lognormal(3, 0.8, N).round(1),  # property/loan value
    "leverage": rng.normal(1.8, 0.6, N).clip(0.5,4.5).round(2),
    "icr": rng.normal(3.5, 1.5, N).clip(0.8,12).round(2),
    "carbon_intensity": rng.lognormal(2, 1.0, N).round(1),  # tCO2e/cr
    "EAD_cr": rng.lognormal(2.5, 0.7, N).round(1),
    "maturity_y": rng.choice([1,3,5,7,10], N, p=[0.2,0.25,0.25,0.2,0.1]),
})

# GeoPandas for GeoParquet geometry column
gdf = gpd.GeoDataFrame(df.to_pandas(), geometry=[Point(xy) for xy in zip(df["lon"], df["lat"])], crs="EPSG:4326")
gdf.to_parquet(OUT, compression="zstd", index=False)
print(f"wrote {OUT} — {len(gdf)} exposures")
print(gdf.head(3).to_string())
print("\nDuckDB preview (bbox Mumbai):")
import duckdb
duckdb.sql("INSTALL spatial; LOAD spatial")
print(duckdb.sql(f"SELECT sector, count(*) FROM read_parquet('{OUT}') WHERE lon BETWEEN 72 AND 73 AND lat BETWEEN 18 AND 20 GROUP BY sector").fetchall())
