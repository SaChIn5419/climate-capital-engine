"""Loss.parquet → loss.geojson for PMTiles builder.

Expects data/curated/loss.parquet (from DuckDB ST_Intersects). Falls back to exposures sample.
"""
import pathlib
import geopandas as gpd

LOSS = pathlib.Path("data/curated/loss.parquet")
OUT = pathlib.Path("data/curated/loss.geojson")
FALLBACK = pathlib.Path("data/curated/exposures.parquet")

src = LOSS if LOSS.exists() else FALLBACK
if not src.exists():
    print(f"no {src} — run build_exposures.py first")
    raise SystemExit(1)
gdf = gpd.read_parquet(src)
# keep <5000 features for pmtiles demo (tippecanoe sample)
if len(gdf) > 5000:
    gdf = gdf.sample(5000, random_state=42)
gdf.to_file(OUT, driver="GeoJSON")
print(f"wrote {OUT} — {len(gdf)} features from {src}")
