"use client";
import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import * as pmtiles from "pmtiles";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from "recharts";

// Data copied from curated CSVs (so dashboard works without extra fetch)
const waterfall = [
  { step: "Base", cet1: 15.0, loss: 0, label: "CET1 15.00%" },
  { step: "Transition", cet1: 11.04, loss: 3957, label: "NGFS GCAM 101$ -3.96pp" },
  { step: "Physical", cet1: 8.52, loss: 2526, label: "IBTrACS 5% -2.53pp" },
];

const perSector = [
  { sector: "Power", total: 1471, dEL: 899, phys: 573 },
  { sector: "Steel", total: 1182, dEL: 733, phys: 449 },
  { sector: "Real Estate", total: 890, dEL: 520, phys: 370 },
  { sector: "Cement", total: 875, dEL: 526, phys: 349 },
  { sector: "Transport", total: 839, dEL: 516, phys: 323 },
  { sector: "Oil & Gas", total: 606, dEL: 369, phys: 237 },
  { sector: "Other", total: 618, dEL: 394, phys: 225 },
];

const wriCurve = [
  { rp: "1.5yr", cells: 429, depth: 4.06 },
  { rp: "2yr", cells: 430, depth: 4.09 },
  { rp: "5yr", cells: 436, depth: 4.14 },
  { rp: "10yr", cells: 438, depth: 4.18 },
  { rp: "25yr", cells: 443, depth: 4.22 },
  { rp: "50yr", cells: 446, depth: 4.25 },
  { rp: "100yr", cells: 449, depth: 4.29 },
  { rp: "250yr", cells: 454, depth: 4.33 },
  { rp: "500yr", cells: 460, depth: 4.36 },
  { rp: "1000yr", cells: 463, depth: 4.4 },
];

const colors: Record<string, string> = {
  Power: "#e11d48",
  Steel: "#f59e0b",
  Cement: "#84cc16",
  Transport: "#0ea5e9",
  "Real Estate": "#6366f1",
  "Oil & Gas": "#14b8a6",
  Other: "#a78bfa",
};

export default function Dashboard() {
  const mapRef = useRef<HTMLDivElement>(null);
  const [activeSector, setActiveSector] = useState<string>("Power");

  useEffect(() => {
    if (!mapRef.current) return;
    const protocol = new pmtiles.Protocol({ metadata: true });
    maplibregl.addProtocol("pmtiles", protocol.tile);

    const map = new maplibregl.Map({
      container: mapRef.current,
      style: {
        version: 8,
        sources: {
          basemap: {
            type: "raster",
            tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution:
              "© OSM | WRI Aqueduct 10-period Mumbai 1.5→1000yr | IBTrACS NI 473 storms 1842-2023 | ERA5 2023-01-01",
          },
          lossReal: {
            type: "vector",
            url: "pmtiles://" + window.location.origin + "/data/loss_real.pmtiles",
            attribution: "© IBTrACS buffer 50km → 7275 exposures → PMTiles 1973 tiles",
          },
        },
        layers: [
          { id: "basemap", type: "raster", source: "basemap" },
          {
            id: "lossReal",
            type: "circle",
            source: "lossReal",
            "source-layer": "loss",
            paint: {
              "circle-radius": ["interpolate", ["linear"], ["zoom"], 5, 2, 10, 6],
              "circle-color": [
                "match",
                ["get", "sector"],
                "Power",
                "#e11d48",
                "Steel",
                "#f59e0b",
                "Real Estate",
                "#6366f1",
                "Cement",
                "#84cc16",
                "Transport",
                "#0ea5e9",
                "#14b8a6",
                /*default*/ "#a78bfa",
              ],
              "circle-opacity": 0.75,
              "circle-stroke-width": 1,
              "circle-stroke-color": "#fff",
            },
          },
        ],
      },
      center: [71, 20],
      zoom: 5.2,
    });
    map.addControl(new maplibregl.NavigationControl(), "top-right");
    map.on("click", "lossReal", (e) => {
      const f = e.features?.[0];
      if (!f) return;
      new maplibregl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(
          `<b>${f.properties.sector}</b><br>loss ₹${Number(f.properties.loss_cr).toFixed(1)} cr`
        )
        .addTo(map);
      setActiveSector(f.properties.sector);
    });
    return () => map.remove();
  }, []);

  return (
    <div style={{ fontFamily: "ui-sans-serif, system-ui, -apple-system", background: "#fafafa", minHeight: "100vh" }}>
      {/* Header + Provenance */}
      <header style={{ background: "#0f172a", color: "#fff", padding: "20px 24px", position: "sticky", top: 0, zIndex: 10 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
          <div>
            <div style={{ fontSize: 22, fontWeight: 800 }}>Climate-to-Capital Engine</div>
            <div style={{ opacity: 0.8, fontSize: 13 }}>
              NGFS Phase 5 India (Current Policies 0 → Net Zero 101 $/t 2030, 120 rows) + ERA5 CDS 5×5 COG + WRI 10-period 1.5→1000yr + IBTrACS NI 473 storms → 7275 loss → PMTiles
            </div>
          </div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {[
              ["NGFS GCAM 101$ 2030", "HIGH", "OBSERVED → PROJECTED"],
              ["ERA5 t2m 2023-01-01", "HIGH", "OBSERVED"],
              ["WRI 100yr 4.29m", "HIGH", "MODELLED"],
              ["IBTrACS NI buffer", "HIGH", "OBSERVED"],
              ["BRSR → exposures 10k", "MEDIUM", "ESTIMATED ±CI"],
              ["Loan book", "N/A", "SYNTHETIC"],
            ].map(([k, lvl, type]) => (
              <span key={k} style={{ background: lvl==="HIGH"?"#16a34a":lvl==="MEDIUM"?"#f59e0b":"#475569", padding: "4px 8px", borderRadius: 6, fontSize: 11 }}>
                {k} <b>{lvl}</b> <span style={{opacity:0.8}}>{type}</span>
              </span>
            ))}
          </div>
        </div>
      </header>

      {/* Map + Waterfall side by side */}
      <section style={{ display: "grid", gridTemplateColumns: "1.7fr 1fr", gap: 16, padding: 16 }}>
        <div style={{ background: "#fff", borderRadius: 12, overflow: "hidden", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
          <div style={{ padding: "12px 16px", borderBottom: "1px solid #eee", display: "flex", justifyContent: "space-between" }}>
            <b>Map — Hazard × Exposure = Loss (PMTiles 1973 tiles, 1MB)</b>
            <span style={{ fontSize: 12, background: "#fef3c7", padding: "2px 8px", borderRadius: 4 }}>Click a dot → sector</span>
          </div>
          <div ref={mapRef} style={{ height: 520 }} />
          <div style={{ padding: 10, fontSize: 12, color: "#475569", display: "flex", gap: 8, flexWrap: "wrap" }}>
            <span style={{ background: "#fee2e2", padding: "2px 6px", borderRadius: 4 }}>Power 1471cr</span>
            <span style={{ background: "#fef3c7", padding: "2px 6px", borderRadius: 4 }}>Steel 1182cr</span>
            <span>Real Estate 890cr</span> <span>Cement 875cr</span> <span>Transport 839cr</span>
            <span style={{ marginLeft: "auto" }}>COGs: <code>wri_coast_rp0100_0_mumbai_cog.tif 4.6KB</code> + <code>era5_mumbai_t2m_20230101_cog.tif 3.2KB</code> via TiTiler</span>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ background: "#fff", borderRadius: 12, padding: 16, boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
            <b>CET1 Waterfall — RWA 100k, Base 15.00% (cap 15k cr)</b>
            <div style={{ fontSize: 12, color: "#64748b" }}>Transition GCAM Net Zero 101$ + Physical IBTrACS 5% gross → Combined 8.52% (Δ -6.48pp)</div>
            <div style={{ height: 220, marginTop: 8 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={waterfall}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="step" tick={{ fontSize: 11 }} />
                  <YAxis domain={[0, 16]} tick={{ fontSize: 11 }} unit="%" />
                  <Tooltip />
                  <Bar dataKey="cet1" radius={[6, 6, 0, 0]}>
                    {waterfall.map((d, i) => (
                      <Cell key={i} fill={i === 0 ? "#0f172a" : i === 2 ? "#dc2626" : "#f59e0b"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{ fontSize: 12, background: "#f1f5f9", padding: 8, borderRadius: 8, marginTop: 8 }}>
              <b>Reverse stress:</b> CET1 breaches 9% at <b>~1.3× GCAM shock</b> (carbon ~132 $/t, between 2030 101$ and 2035 175$) — `min ||θ|| s.t. CET1&lt;9%`
            </div>
          </div>

          <div style={{ background: "#fff", borderRadius: 12, padding: 16, boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
            <b>Concentration — Total EL = dEL (transition) + phys_EL (5%)</b>
            <div style={{ height: 220, marginTop: 8 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={perSector} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" unit=" cr" tick={{ fontSize: 11 }} />
                  <YAxis dataKey="sector" type="category" width={90} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="total" radius={[0, 6, 6, 0]}>
                    {perSector.map((d) => (
                      <Cell key={d.sector} fill={colors[d.sector]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{ fontSize: 11, color: "#64748b" }}>Active: <b>{activeSector}</b> — click map dot to highlight. Power/Steel = 2.6k of 6.4k total.</div>
          </div>
        </div>
      </section>

      {/* Borrower card + Hazard curve + Lineage */}
      <section style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, padding: "0 16px 16px" }}>
        <div style={{ background: "#fff", borderRadius: 12, padding: 16, boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
          <b>Borrower explainability — PD=Λ(Xβ+γC)</b>
          <div style={{ fontSize: 12, color: "#475569" }}>Leverage 1.61, ICR -0.58, Carbon 0.03 — intercept -5.17</div>
          <div style={{ marginTop: 10, border: "1px solid #e2e8f0", borderRadius: 8, padding: 12 }}>
            <div style={{ fontWeight: 700 }}>Indian Steel Manufacturer — {activeSector}</div>
            <div style={{ fontSize: 12, color: "#475569" }}>Base PD 2.31% → Stress (GCAM 101$) 5.07% <span style={{ color: "#dc2626" }}>+2.76pp</span></div>
            <div style={{ marginTop: 8, fontSize: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}><span>Carbon price</span><span>+1.02%</span></div>
              <div style={{ background: "#fee2e2", height: 6, borderRadius: 3, margin: "4px 0" }}><div style={{ width: "42%", background: "#dc2626", height: 6, borderRadius: 3 }} /></div>
              <div style={{ display: "flex", justifyContent: "space-between" }}><span>Leverage</span><span>+0.58%</span></div>
              <div style={{ background: "#fef3c7", height: 6, borderRadius: 3, margin: "4px 0" }}><div style={{ width: "24%", background: "#f59e0b", height: 6, borderRadius: 3 }} /></div>
              <div style={{ display: "flex", justifyContent: "space-between" }}><span>Energy intensity</span><span>+0.42%</span></div>
            </div>
            <div style={{ marginTop: 8, fontSize: 11, background: "#0f172a", color: "#fff", padding: 8, borderRadius: 6 }}>
              Transition Score: <b>BB</b> (High) — Carbon 68, Energy 55, Leverage 42 — <span style={{ opacity: 0.8 }}>Watch</span>
            </div>
          </div>
        </div>

        <div style={{ background: "#fff", borderRadius: 12, padding: 16, boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
          <b>WRI Hazard Curve — Mumbai coastal 1.5→1000yr</b>
          <div style={{ fontSize: 12, color: "#64748b" }}>Monotone 429→463 cells, 4.06→4.40m — validates EVT</div>
          <div style={{ height: 200, marginTop: 8 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={wriCurve}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="rp" tick={{ fontSize: 10 }} />
                <YAxis yAxisId="left" tick={{ fontSize: 10 }} />
                <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 10 }} />
                <Tooltip />
                <Bar yAxisId="left" dataKey="cells" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                <Bar yAxisId="right" dataKey="depth" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div style={{ fontSize: 11, color: "#475569" }}>10 COGs 4.6KB ea → `wri_coast_hazard_curve.csv` → DuckDB `Hazard×Exposure` per return period.</div>
        </div>

        <div style={{ background: "#fff", borderRadius: 12, padding: 16, boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
          <b>Data lineage — every variable tagged</b>
          <div style={{ fontSize: 12, color: "#475569", maxHeight: 220, overflow: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 11 }}>
              <thead><tr style={{ textAlign: "left", borderBottom: "1px solid #e2e8f0" }}><th>Var</th><th>Source</th><th>Conf</th></tr></thead>
              <tbody>
                <tr><td>Carbon price</td><td>NGFS GCAM India 120 rows</td><td><span style={{ background: "#16a34a", color: "#fff", padding: "1px 6px", borderRadius: 4 }}>HIGH</span></td></tr>
                <tr><td>t2m</td><td>ERA5 CDS 5×5 COG 3.2KB</td><td><span style={{ background: "#16a34a", color: "#fff", padding: "1px 6px", borderRadius: 4 }}>HIGH</span></td></tr>
                <tr><td>Flood depth</td><td>WRI Aqueduct 10-period</td><td><span style={{ background: "#16a34a", color: "#fff", padding: "1px 6px", borderRadius: 4 }}>HIGH</span></td></tr>
                <tr><td>Cyclone</td><td>IBTrACS NI 473 storms</td><td><span style={{ background: "#16a34a", color: "#fff", padding: "1px 6px", borderRadius: 4 }}>HIGH</span></td></tr>
                <tr><td>Borrower emissions</td><td>BRSR → sector GLM ±28% CI</td><td><span style={{ background: "#f59e0b", color: "#fff", padding: "1px 6px", borderRadius: 4 }}>MEDIUM</span></td></tr>
                <tr><td>Loan exposure</td><td>Synthetic 10k, calibrated to RBI + GHSL proxy</td><td><span style={{ background: "#475569", color: "#fff", padding: "1px 6px", borderRadius: 4 }}>N/A</span></td></tr>
              </tbody>
            </table>
            <div style={{ marginTop: 8, fontSize: 11, background: "#f8fafc", padding: 8, borderRadius: 6 }}>
              <b>CCTS simulator</b> `P=f(S,D,Abatement)` + OU + jumps → `Price 0→101 $` → Monte Carlo — <i>structural, not time-series</i> (no price history per BEE).
            </div>
            <div style={{ marginTop: 8, fontSize: 11 }}>
              <b>GCC buyers:</b> FAB/ENBD/ADCB/ADIB/Mashreq/DIB (AED190bn earmarked), ADGM, PIF, QNB, SNB — `CBUAE ICAAP` scenario analysis + `Climate Change Law 2024`.
            </div>
          </div>
        </div>
      </section>

      <footer style={{ padding: 16, textAlign: "center", fontSize: 12, color: "#64748b" }}>
        Built with Polars + DuckDB Spatial (no PostGIS) + GeoParquet + PMTiles + MapLibre + COG + Leafmap + Marimo + uv — data local (26MB IBTrACS raw ignored), results online (PMTiles 1MB + COGs 4.6KB) • RBI RB-CRIS gap as feature
      </footer>
    </div>
  );
}
