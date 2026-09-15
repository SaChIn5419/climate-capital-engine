.PHONY: sync data parquet pmtiles cog map deploy clean

# Ultra-light: no Docker needed. Requires: uv (https://astral.sh/uv/install.sh), gdal, tippecanoe (optional)
UV := uv

sync:
	$(UV) sync

data: parquet cog
	@echo "→ data done (parquet + cog)"

parquet:
	@echo "→ NGFS/GHSL/IBTrACS → GeoParquet (polars + geopandas)"
	$(UV) run python scripts/fetch_ngfs.py || echo "fetch_ngfs skipped (needs CDS token)"
	$(UV) run python scripts/fetch_ghsl_osm.py || echo "fetch_ghsl skipped"
	$(UV) run python scripts/build_exposures.py
	$(UV) run python scripts/build_hazard.py

cog:
	@echo "→ flood/ERA5 → COG"
	$(UV) run python -c "import rio_cogeo; print(rio_cogeo.__version__)"
	# example: gdal_translate data/raw/flood.tif data/curated/flood_cog.tif -of COG -co COMPRESS=LZW
	# xarray ERA5 → rioxarray.to_raster(..., driver='COG')

pmtiles: data/curated/loss.geojson
	@echo "→ GeoJSON → PMTiles (no tile server)"
	@which tippecanoe >/dev/null && tippecanoe -o web/public/data/loss.pmtiles data/curated/loss.geojson --drop-densest-as-needed --force || echo "tippecanoe not found — install via brew/apt, or use planetiler"

data/curated/loss.geojson: data/curated/loss.parquet
	$(UV) run python scripts/parquet_to_geojson.py

map:
	@echo "→ open notebooks/02_duckdb_spatial_join.ipynb or marimo"
	$(UV) run marimo edit notebooks/02_duckdb_spatial_join.py --host 0.0.0.0 --port 2718 || $(UV) run jupyter lab

web:
	cd web && npm install && npm run dev

deploy:
	@echo "→ static deploy to GitHub Pages / Cloudflare Pages"
	@echo "Upload web/public/data/*.pmtiles + data/curated/*_cog.tif to R2/S3 with CORS * and range-request support"

clean:
	rm -rf data/curated/*.pmtiles data/curated/*.geojson
