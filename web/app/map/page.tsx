"use client";
import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import * as pmtiles from "pmtiles";

// Static PMTiles — no tile server. Host loss.pmtiles on GitHub Pages / R2 with CORS * and range-request.
const PMTILES_URL = process.env.NEXT_PUBLIC_PMTILES_URL || "/data/loss.pmtiles";
const COG_TILES_URL = process.env.NEXT_PUBLIC_COG_TILES_URL || ""; // e.g. TiTiler endpoint for flood_cog.tif

export default function MapPage() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const protocol = new pmtiles.Protocol({ metadata: true });
    maplibregl.addProtocol("pmtiles", protocol.tile);

    const map = new maplibregl.Map({
      container: ref.current!,
      style: {
        version: 8,
        sources: {
          basemap: {
            type: "raster",
            tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution: "© OpenStreetMap"
          },
          loss: {
            type: "vector",
            url: `pmtiles://${PMTILES_URL}`,
            attribution: "© Synthetic demo — hazard×exposure→loss via DuckDB"
          }
        },
        layers: [
          { id: "basemap", type: "raster", source: "basemap" },
          // sample PMTiles layers — adjust source-layer names to match tippecanoe output (use pmtiles show)
          { id: "loss-fill", type: "fill", source: "loss", "source-layer": "loss", paint: { "fill-color": "#e11d48", "fill-opacity": 0.35 } },
          { id: "loss-line", type: "line", source: "loss", "source-layer": "loss", paint: { "line-color": "#7f1d1d", "line-width": 1 } }
        ]
      },
      center: [72.9, 19.1],
      zoom: 8
    });

    // Optional COG raster overlay via TiTiler (if COG_TILES_URL set)
    if (COG_TILES_URL) {
      map.on("load", () => {
        map.addSource("flood-cog", { type: "raster", tiles: [COG_TILES_URL], tileSize: 256 });
        map.addLayer({ id: "flood-cog", type: "raster", source: "flood-cog", paint: { "raster-opacity": 0.45 } });
      });
    }

    map.addControl(new maplibregl.NavigationControl(), "top-right");
    return () => map.remove();
  }, []);

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <header style={{ padding: 12, borderBottom: "1px solid #eee", fontFamily: "system-ui" }}>
        <strong>Climate-to-Capital</strong> — PMTiles + MapLibre (no server) ·{" "}
        <span style={{ color: "#666" }}>loss.pmtiles via range requests · COG via TiTiler</span>
        <span style={{ float: "right", fontSize: 12, background: "#fef3c7", padding: "2px 6px", borderRadius: 4 }}>SYNTHETIC demo — HIGH/MEDIUM badges in dashboard</span>
      </header>
      <div ref={ref} style={{ flex: 1 }} />
    </div>
  );
}
