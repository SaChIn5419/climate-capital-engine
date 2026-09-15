"""Build sample hazard layer → GeoParquet + COG placeholder.

In production: WRI Aqueduct 100yr + NRSC Atlas vectorized, ERA5 0.25deg → COG.
Here: synthetic polygons for Mumbai/ Chennai flood demo.
"""
import pathlib
import geopandas as gpd
from shapely.geometry import Polygon
import polars as pl

OUT_PQ = pathlib.Path("data/curated/hazard_flood_100yr.parquet")
OUT_PQ.parent.mkdir(parents=True, exist_ok=True)

# Two demo flood polygons (Mumbai + Chennai)
polys = [
    Polygon([(72.7,18.9),(73.0,18.9),(73.0,19.3),(72.7,19.3)]),
    Polygon([(80.1,12.8),(80.4,12.8),(80.4,13.2),(80.1,13.2)]),
]
gdf = gpd.GeoDataFrame({
    "hazard": ["flood_100yr"]*2,
    "depth_m": [1.2, 0.9],
    "return_period": [100,100],
    "source": ["WRI Aqueduct (sample)"]*2,
}, geometry=polys, crs="EPSG:4326")
gdf.to_parquet(OUT_PQ, compression="zstd")
print(f"wrote {OUT_PQ} — {len(gdf)} polygons")

# Also write GeoJSON for tippecanoe → PMTiles
gdf.to_file("data/curated/hazard_flood_100yr.geojson", driver="GeoJSON")
print("wrote data/curated/hazard_flood_100yr.geojson")

# Polars scan demo
print(pl.scan_parquet(OUT_PQ).collect().head(2))
