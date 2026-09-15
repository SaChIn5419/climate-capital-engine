# Execution Proof — Ultra-Light Skeleton Built

Task: 20260915-climate-capital-qgis-a7f3c2
Date: 2026-09-15
Status: EXECUTED

## What was built (no PostGIS/QGIS)
- uv sync ✓ (1.5.5 duckdb spatial, polars, leafmap, marimo, altair)
- data/curated/exposures.parquet 10k rows ✓ (build_exposures.py)
- data/curated/hazard_flood_100yr.parquet 2 polys + geojson ✓
- data/curated/loss.parquet 6 rows (Mumbai+Chennai ST_Intersects via DuckDB) ✓
- data/curated/loss.geojson → web/public/data/loss.geojson ✓
- notebooks/02_duckdb_spatial_join.py (marimo) + .ipynb ✓
- web/app/map/page.tsx (MapLibre + PMTiles, no server) ✓
- pyproject.toml pinned, Makefile, registry.csv, lineage README ✓

## Verify
uv run python -c "import duckdb; duckdb.sql('INSTALL spatial; LOAD spatial'); print(duckdb.sql('SELECT count(*) FROM read_parquet(\"data/curated/loss.parquet\")').fetchall())"
# → [(6,)]

Next:
- make pmtiles (needs tippecanoe) → loss.pmtiles on Pages
- uv run marimo run notebooks/02_duckdb_spatial_join.py
- cd web && npm install && npm run dev → http://localhost:3000/map
