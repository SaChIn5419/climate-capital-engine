"""Hazard: ERA5 NetCDF → COG + EVT (GPD/GEV) via xarray.

Modern: stream via kerchunk+zarr ref to avoid 100GB download; write COG for map.
"""
import xarray as xr
import rioxarray  # noqa
import pathlib

def era5_to_cog(nc_path: str, out_cog: str, var: str = "t2m"):
    ds = xr.open_dataset(nc_path, chunks="auto")
    da = ds[var]
    # example: monthly anomaly
    anom = da - da.mean("time")
    anom.rio.to_raster(out_cog, driver="COG", compress="LZW")
    print(f"wrote COG {out_cog}")

if __name__ == "__main__":
    print("placeholder — fetch ERA5 via CDS API then call era5_to_cog('data/raw/era5.nc','data/curated/era5_anom_cog.tif')")
