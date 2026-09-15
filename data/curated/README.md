# data/curated — single-file, git-lfs or S3

- `exposures.parquet` — 10k synthetic loans + GHSL/OSM geom (GeoParquet)
- `hazard_flood_100yr.parquet` — vectorized WRI/NRSC hazard polygons
- `hazard_flood_100yr_cog.tif` — raster COG fallback
- `era5_temp_anomaly_cog.tif` — ERA5 anomaly COG
- `loss.parquet` — DuckDB ST_Intersects result
- `loss.geojson` → `loss.pmtiles` (via tippecanoe)

Do not commit >50MB directly; use `git lfs` or upload to S3/R2 and reference by URL in `registry.csv`.
