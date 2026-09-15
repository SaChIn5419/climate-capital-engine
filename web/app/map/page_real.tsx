"use client";
import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import * as pmtiles from "pmtiles";
export default function MapReal() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const protocol = new pmtiles.Protocol({ metadata: true });
    maplibregl.addProtocol("pmtiles", protocol.tile);
    const map = new maplibregl.Map({
      container: ref.current!,
      style: {
        version: 8,
        sources: {
          basemap: { type: "raster", tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"], tileSize: 256, attribution: "© OpenStreetMap | IBTrACS NI 1842-2023 473 storms | ERA5 2023-01-01" },
          lossReal: { type: "vector", url: "pmtiles://" + location.origin + "/data/loss_real.pmtiles" },
          flood: { type: "raster", tiles: [location.origin + "/data/flood_mumbai_cog.tif"], tileSize: 256 }, // fallback to COG via leafmap/titiler in prod
        },
        layers: [
          { id: "basemap", type: "raster", source: "basemap" },
          { id: "lossReal", type: "circle", source: "lossReal", "source-layer": "loss", paint: { "circle-radius": 4, "circle-color": ["match", ["get","sector"], "Power","#e11d48","Steel","#f59e0b","Real Estate","#0ea5e9","Cement","#84cc16", "#9333ea"], "circle-opacity": 0.7 } },
        ]
      },
      center: [71, 20], zoom: 5
    });
    map.addControl(new maplibregl.NavigationControl(), "top-right");
    return () => map.remove();
  }, []);
  return <div ref={ref} style={{height:"100vh"}} />;
}
