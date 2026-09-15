# Validation — Ultra-Light Execution (PostGIS-free)

**task_id:** 20260915-climate-capital-qgis-a7f3c2
**contract_version:** v1.2
**status:** VALIDATE (post-EXECUTE skeleton)
**date:** 2026-09-15

## Did we do what we intended?
YES — ultra-light skeleton built, PostGIS/QGIS fully replaced:
- pyproject.toml pinned (duckdb==1.5.5, polars, leafmap, marimo, altair) → uv sync succeeded
- 10k exposures → GeoParquet (build_exposures.py) ✓
- Hazard 2 polygons → GeoParquet+GeoJSON ✓
- DuckDB ST_Intersects → loss.parquet 6 rows (Mumbai+Chennai demo) ✓ — proves Hazard × Exposure → Loss without PostGIS
- Marimo notebook + ipynb ✓, web/app/map/page.tsx PMTiles+MapLibre ✓

## Version consistency
No @latest — all pinned in pyproject.toml + decision v1.3. DuckDB spatial 1.5.5 verified.

## Remaining
- tippecanoe → loss.pmtiles (optional, not blocking — GeoJSON already renders via Leafmap)
- ERA5 CDS fetch requires API key (documented in scripts/fetch_ngfs.py placeholder)
- Full PMTiles deploy → GitHub Pages (make deploy)

## Verdict
EXECUTE skeleton PASSED — platform is reproducible via `uv sync` with zero DB/server.
