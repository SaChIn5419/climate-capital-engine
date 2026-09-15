"""ERA5 → COG via CDS API (requires ~/.cdsapirc).

Usage:
  uv run python scripts/fetch_era5.py --var 2m_temperature --year 2023 --bbox 72,19,73,20
Keeps raw NetCDF in data/raw/era5/ (ignored), writes COG to data/curated/ + web/public/data/
"""
import argparse, pathlib, shutil, cdsapi, xarray as xr, rioxarray

def fetch(var="2m_temperature", year="2023", month="01", day="01", bbox=(20,72,19,73)):
    c = cdsapi.Client()
    north, west, south, east = bbox  # N,W,S,E
    raw = pathlib.Path(f"data/raw/era5/era5_{var}_{year}{month}{day}.nc")
    raw.parent.mkdir(parents=True, exist_ok=True)
    print(f"→ CDS retrieve {var} {year}-{month}-{day} bbox {bbox}")
    c.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": [var],
            "year": year,
            "month": month,
            "day": [day],
            "time": ["00:00"],
            "area": [north, west, south, east],
            "format": "netcdf",
        },
        str(raw)
    )
    print(f"raw {raw} {raw.stat().st_size} bytes")
    ds = xr.open_dataset(raw)
    # pick var key (cds names differ: 2m_temperature → t2m)
    v = list(ds.data_vars)[0]
    da = ds[v].isel(valid_time=0) if "valid_time" in ds[v].dims else ds[v].isel(time=0)
    # handle coords
    x_dim = "longitude" if "longitude" in da.coords else "lon"
    y_dim = "latitude" if "latitude" in da.coords else "lat"
    da.rio.set_spatial_dims(x_dim=x_dim, y_dim=y_dim, inplace=True)
    da.rio.write_crs("EPSG:4326", inplace=True)
    out = pathlib.Path(f"data/curated/era5_mumbai_{v}_{year}{month}{day}_cog.tif")
    web = pathlib.Path(f"web/public/data/era5_mumbai_{v}_{year}{month}{day}_cog.tif")
    da.rio.to_raster(str(out), driver="COG", compress="LZW", blocksize=256, overview="auto")
    shutil.copy(out, web)
    print(f"✓ COG {out} + {web}")
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--var", default="2m_temperature")
    ap.add_argument("--year", default="2023")
    ap.add_argument("--bbox", default="20,72,19,73", help="N,W,S,E")
    args = ap.parse_args()
    bbox = tuple(map(float, args.bbox.split(",")))
    fetch(args.var, args.year, bbox=bbox)
