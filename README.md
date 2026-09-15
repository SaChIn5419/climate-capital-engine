# Climate-to-Capital Transmission Engine
**RBI/NGFS-aligned + ERA5/IBTrACS physical risk + modern FOSS map stack**

> `Polars + DuckDB Spatial + GeoParquet + PMTiles + MapLibre GL JS + COG + Leafmap + Marimo + uv`  
> No PostGIS. No QGIS. No tile server. No Docker. Runs in Colab in 30s.

Task: `20260915-climate-capital-qgis-a7f3c2` → `.intentos/tasks/20260915-climate-capital-qgis-a7f3c2/`

## 30-Second Start (reviewer copy-paste)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync                 # 2-4s (not 90s pip)
uv run marimo run notebooks/02_duckdb_spatial_join.py --host 0.0.0.0
# or: uv run jupyter lab
# → open http://localhost:2718 — Mumbai flood + CET1 map, zero DB
```

Web map (static, $0 hosting):
```bash
cd web && npm install && npm run dev
# open http://localhost:3000/map → MapLibre reads pmtiles:// on GitHub Pages via range requests
```

## What this is

```
NGFS Short-term (5-yr) + Phase V → VAR/BVAR → sector EBITDA → firm → PD=Λ(Xβ+γC) → EL → CET1
ERA5 (1940→) + IBTrACS NI → Poisson+GPD/GEV hazard → damage → property loss → CRE PD
= Hazard × Exposure (GHSL/OSM) × Vulnerability → Loss, mapped as PMTiles + COG overlay
+ CCTS structural simulator P=f(S,D,Abatement) + Monte Carlo
+ Provenance badges HIGH/MEDIUM/SYNTHETIC per variable
```

Every number is **traceable**: `OBSERVED` (NGFS/ERA5), `ESTIMATED` (BRSR emissions ±CI), `PROJECTED` (NGFS pathways), `SYNTHETIC` (10k loan book, transparently generated).

## Structure

```
data/
  registry.csv          # Level A-D with license/resolution/format/confidence
  lineage/              # per-variable {source,date,unit,transform,method,missingness}
  raw/                  # NGFS pyam pulls, ERA5 NetCDF, IBTrACS SHP
  curated/              # *.parquet (GeoParquet), *_cog.tif (COG), *.pmtiles
notebooks/
  01_ngfs_pyam_to_parquet.py/.ipynb   # Polars lazy
  02_duckdb_spatial_join.py/.ipynb    # DuckDB ST_Intersects — replaces PostGIS
  03_era5_xarray_to_cog.py
  04_leafmap_kepler_explore.py        # kepler.gl + deck.gl track
  05_ccts_simulator_mc.py
src/
  transition/var.py  pd_lgd.py  bank.py
  physical/hazard.py  damage.py
  ccts/structural_price.py
web/app/map/page.tsx    # MapLibre + pmtiles:// + COG (TiTiler) + Deck.gl choropleth
scripts/fetch_*.py      # httpx + polars fetchers
```

## Data (all free & open)

| Source | License | Format in repo |
|---|---|---|
| NGFS Phase V + Short-term (IIASA) | Free | `*.parquet` via pyam → polars |
| ERA5 (Copernicus CDS) | CC-BY | `*_cog.tif` via rio-cogeo |
| IBTrACS NI (NOAA NCEI) | Public | `hazard.parquet` GeoParquet |
| GHSL POP/BUILT (JRC) | Free | `*_cog.tif` / parquet |
| OSM India | ODbL | `*.parquet` via Geofabrik |
| WRI Aqueduct + NRSC Atlas | CC-BY / GODL | COG + parquet |
| BRSR Top 1000 (SEBI) | Public filings | `exposures.parquet` |
| CCTS (BEE) | Public | simulator, no price history |

## Why modern lightweight?

| Old (2022 template) | New (2026 ultra-light) | Win |
|---|---|---|
| Pandas | **Polars** 4-22× faster, 8× less energy | speed |
| pip/poetry | **uv** 10-100× faster | DX |
| Jupyter hidden state | **Marimo** reactive | reproducibility |
| PostGIS + GeoServer VM $20/mo | **DuckDB + PMTiles static $0** | cost |
| Docker for everything | **uv sync** — no Docker for MVP | reviewer friction |

Keep: `statsmodels` (VAR), `scikit-learn` logit, `xarray` (ERA5) — rigor over trend.

## Validation

1. Historical: does Poisson+GPD reproduce IBTrACS NI mean 3.9 storms/yr?
2. OOS: train 2010-20 → test 2021-25
3. Sensitivity: carbon +25%, damage ×1.5, emissions ±30% → CET1 distribution + reverse stress `min‖θ-θ0‖ s.t. CET1<min`

## Deploy

```bash
make pmtiles   # GeoJSON → PMTiles
make deploy    # upload loss.pmtiles + *_cog.tif to S3/R2 (CORS *), push web/ to Pages
```

Full design: `.intentos/tasks/20260915-climate-capital-qgis-a7f3c2/decision.md v1.3`
