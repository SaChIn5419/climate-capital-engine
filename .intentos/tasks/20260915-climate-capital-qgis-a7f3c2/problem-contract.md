# Problem Contract — Climate-to-Capital Platform (Project 1+2 + MODERN MAP STACK)

**task_id:** `20260915-climate-capital-qgis-a7f3c2`
**task_root:** `.intentos/tasks/20260915-climate-capital-qgis-a7f3c2/`
**contract_version:** v1.1  — AMENDMENT (stack modernization)
**contract_hash:** sha256:amended-v1.1-modern-stack
**status:** DECIDE → CONVERGE (amended)
**created:** 2026-09-15
**last_updated:** 2026-09-15
**amendment_reason:** User reports problem with PostGIS/QGIS — requires modern FOSS alternative that is lighter, serverless-first, and portfolio-friendly. No scope creep beyond stack swap.
**impacted_nodes:** Q3 (architecture), Q7 (roadmap), evidence-ledger O1-O5

---

## Amendment Delta

| Before | After | Reason |
|---|---|---|
| QGIS Desktop LTR + PostGIS + GeoServer/QGIS Server | **DuckDB Spatial + GeoParquet + PMTiles + MapLibre GL JS** with optional COG/TiTiler, Leafmap/Deck.gl for Python | User pain: PostGIS needs server/ops, QGIS is desktop-heavy, not "modern web" portfolio signal |
| Heavy install, DB ops | Zero-DB: `pip install duckdb` + single `.parquet` / `.pmtiles` file, static hosting (GitHub Pages / S3) | Modern data-lake pattern; reproducible in Colab |
| WMS/GeoServer tiles | PMTiles single-file vector tiles + COG raster via HTTP range requests | No tile server to run |

**Preserved:** All open-source data sources (NGFS, ERA5, IBTrACS, GHSL, OSM, WRI Aqueduct, NRSC, BRSR, CCTS), 7-layer transmission `Climate→Economy→Firm→Credit→Bank→Capital`, credibility hierarchy A-D, validation trilogy, GCC market mapping.

## 1. Objective (unchanged + stack clause)

Combine Project 1+2 into flagship with **modern, serverless, fully FOSS geospatial stack** — maximized open-source feasibility, research novelty, GCC/India market mapping. Stack must be install-free for reviewers (static web map), runnable in Jupyter, and deployable without DB admin.

## 2-8. Scope / Unit / Data / Constraints / Success — unchanged from v1.0

Add constraint: **No mandatory PostGIS or QGIS Desktop install for MVP**; any DB must be embedded (DuckDB/Spatialite) and any map must be viewable as static HTML/PMTiles.

## 9. Assumptions (updated)

- DuckDB Spatial is MIT, `INSTALL spatial; LOAD spatial` works in 1.5.x (builtin GEOMETRY in v1.5) — replaces PostGIS for spatial joins/filters
- GeoParquet is OGC standard, readable by GeoPandas/GDAL/DuckDB/QGIS — single-file dataset portability
- PMTiles is single-file archive, range-request served, MapLibre protocol `pmtiles://` — replaces tile server
- MapLibre GL JS is BSD, fork of Mapbox GL, supports MLT (MapLibre Tile) successor to MVT — future-proof
- COG (Cloud-Optimized GeoTIFF) remains OGC standard — flood/ERA5 rasters streamable via TiTiler/Leafmap without server
- Bhuvan WMS still usable as fallback but not required for reproducibility

## 10. Open Questions (updated)

1. Same geography question — India + Dubai demo remains default
2. Output target — now defaults to **Next.js + MapLibre + PMTiles static deploy** + Streamlit/Leafmap notebook for analysis
3. QGIS depth → **MapLibre depth: deck.gl choropleth + COG raster overlay vs Kepler.gl exploratory**
4-5 unchanged

## 11. Decision Status (amended)

- Approved: **Modern stack** as primary (see `decision.md` v1.2)
- PostGIS/QGIS retained as *optional comparison* in appendix only, not required for reproduction

## 12. Traceability

- Amendment requested: user 2026-09-15 "problem with PostGIS/QGIS, can you do more modern free opensource"
- Verified sources: DuckDB Spatial docs, GeoParquet org, PMTiles spec, MapLibre 2025-2026 MLT announcement, COG spec, Leafmap
