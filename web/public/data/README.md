# web/public/data — static hosting for PMTiles + COG

Place:
- `loss.pmtiles` (from `make pmtiles`)
- `flood_cog.tif` (COG) if you want direct COG streaming

Deploy:
- GitHub Pages: push `web/public/data/*` → auto-serves with range requests + CORS
- Cloudflare R2 / S3: upload with `Access-Control-Allow-Origin: *` and `Accept-Ranges: bytes`

Verify COG: `python -m rio_cogeo.cog_validate flood_cog.tif` or `validate_cloud_optimized_geotiff.py`

Next.js env:
```
NEXT_PUBLIC_PMTILES_URL=https://your.github.io/climate-capital/data/loss.pmtiles
NEXT_PUBLIC_COG_TILES_URL=https://titiler.example.com/cog/tiles/{z}/{x}/{y}?url=https://your.r2.dev/flood_cog.tif&colormap=Blues
```
