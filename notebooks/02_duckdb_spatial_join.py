# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo","polars","duckdb","leafmap[maplibre]","altair"]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")

@app.cell
def __():
    import marimo as mo
    import polars as pl
    import duckdb
    import leafmap.maplibregl as leafmap
    import altair as alt
    duckdb.sql("INSTALL spatial; LOAD spatial")
    mo.md("# 02 — DuckDB Spatial Join (replaces PostGIS)\n`exposures.parquet × hazard_flood_100yr.parquet → loss.parquet` — zero server, bbox pruning")
    return mo, pl, duckdb, leafmap, alt

@app.cell
def __(duckdb):
    # Build sample data if not exists
    import pathlib, subprocess, sys
    if not pathlib.Path("data/curated/exposures.parquet").exists():
        subprocess.run([sys.executable, "scripts/build_exposures.py"])
    if not pathlib.Path("data/curated/hazard_flood_100yr.parquet").exists():
        subprocess.run([sys.executable, "scripts/build_hazard.py"])
    duckdb.sql("SELECT count(*) AS exposures FROM read_parquet('data/curated/exposures.parquet')").show()
    duckdb.sql("SELECT * FROM read_parquet('data/curated/hazard_flood_100yr.parquet')").show()
    return

@app.cell
def __(duckdb, pl):
    # Core: Hazard × Exposure → Loss (replaces PostGIS ST_Intersects)
    # vulnerability factor by sector (sample)
    duckdb.sql("""
      CREATE OR REPLACE TABLE loss AS
      SELECT 
        e.id, e.sector, e.value_cr, e.EAD_cr, e.leverage, e.icr, e.carbon_intensity,
        e.lon, e.lat, e.geometry,
        h.depth_m,
        -- simple vulnerability: depth * sector multiplier
        CASE e.sector WHEN 'Real Estate' THEN 0.35 WHEN 'Power' THEN 0.28 ELSE 0.22 END * h.depth_m * e.value_cr AS loss_cr
      FROM read_parquet('data/curated/exposures.parquet') e
      JOIN read_parquet('data/curated/hazard_flood_100yr.parquet') h
        ON ST_Intersects(e.geometry, h.geometry)
    """)
    duckdb.sql("COPY (SELECT * FROM loss) TO 'data/curated/loss.parquet' (FORMAT PARQUET, COMPRESSION ZSTD)")
    duckdb.sql("SELECT sector, count(*) AS n, round(sum(loss_cr),1) AS total_loss_cr FROM loss GROUP BY sector ORDER BY total_loss_cr DESC").show()
    return

@app.cell
def __(pl):
    # Polars: same loss aggregated for Altair CET1 waterfall
    df = pl.scan_parquet("data/curated/loss.parquet").collect()
    df.head(3)
    return df,

@app.cell
def __(alt, duckdb):
    # Altair: CET1 depletion by sector (sample: loss / capital)
    import polars as pl
    agg = duckdb.sql("SELECT sector, sum(loss_cr) AS loss FROM loss GROUP BY sector").pl()
    chart = alt.Chart(agg).mark_bar().encode(
        x=alt.X("sector:N", sort="-y"),
        y="loss:Q",
        color="sector:N",
        tooltip=["sector","loss"]
    ).properties(title="Sample Loss by Sector (Mumbai+Chennai 100yr flood) — pro forma CET1 depletion")
    chart
    return

@app.cell
def __(leafmap):
    m = leafmap.Map(center=[19.1,72.9], zoom=9, style="positron")
    m.add_vector("data/curated/hazard_flood_100yr.geojson", layer_type="fill", fill_color="blue", fill_opacity=0.2)
    m.add_vector("data/curated/loss.geojson", layer_type="circle", color_column="loss_cr") if __import__("pathlib").Path("data/curated/loss.geojson").exists() else None
    # COG overlay example (when you have flood_cog.tif): m.add_cog_layer("https://your.r2.dev/flood_cog.tif", name="Flood depth")
    m
    return

if __name__ == "__main__":
    app.run()
