# Decomposition — Climate-to-Capital + QGIS Platform

**task_id:** 20260915-climate-capital-qgis-a7f3c2  
**contract_version:** v1.0  
**created:** 2026-09-15

## Main Objective

Design and validate feasibility of an integrated Climate-to-Capital Transmission Engine (transition + physical + QGIS) that is credible on open-source data and maps to genuine GCC/India market demand.

```
MAIN OBJECTIVE: Integrated Climate Financial Risk Platform
├── Q1: Literature & Regulatory Frontier
├── Q2: Data Feasibility & Open-Source Registry
├── Q3: Integrated Architecture & QGIS Design
├── Q4: Quantitative Methods & Validation Plan
├── Q5: Novelty & Contribution Assessment
├── Q6: Market Demand Mapping (GCC + India)
└── Q7: Implementation Roadmap & Risk
```

---

## Q1: Literature & Regulatory Frontier

- **Question:** What is the state of RBI, NGFS, BIS, TCFD/ISSB guidance on climate scenario analysis, stress testing, and physical risk? Where is RB-CRIS?
- **Why matters:** Determines regulatory tailwind and credibility anchor.
- **Evidence needed:** RBI Annual Report 2025, NGFS Phase V docs, BIS climate reports, GCC central bank guidelines (SAMA, CBUAE, QCB)
- **Method:** Lit search, source extraction
- **Completion:** Evidence ledger entries with source type, date, quote
- **Owner:** researcher

## Q2: Data Feasibility & Open-Source Registry

- **Question:** For each component (scenarios, macro, weather, cyclone, GIS, corporate, emissions, CCTS, exposures), what exists open-source, at what resolution/license, and what must be synthetic?
- **Why matters:** Core feasibility claim; determines A-D labelling.
- **Evidence needed:**
  - NGFS Phase V download + short-term scenarios
  - RBI DBIE / MOSPI macro series
  - ERA5 (Copernicus CDS) — resolution, latency, license
  - IBTrACS — NIO subset
  - BRSR top-1000, CDP, annual reports
  - CCTS (BEE/Grid Controller) — registry/trading status
  - Geospatial: SRTM 30m, GHSL, OpenStreetMap, GADM, BHUVAN, IMD, Copernicus Land, Global Flood Maps (JRC), WRI Aqueduct
  - QGIS-compatible formats (GeoTIFF, Shapefile, GeoPackage, WMS)
- **Method:** Source verification, license check, coverage table
- **Completion:** Registry table with availability 0-5 + credibility grade + QGIS readiness
- **Owner:** researcher + data-quality-auditor (sequential)

## Q3: Integrated Architecture & QGIS Design

- **Question:** How to fuse transition and physical engines with QGIS without double-counting or breaking causality?
- **Why matters:** This is the platform's differentiator.
- **Subproblems:**
  - Q3a: 7-layer transmission chain (scenario → macro → sector → firm → credit → bank → capital) with physical overlay (hazard × exposure × vulnerability)
  - Q3b: QGIS stack — desktop vs server vs web (QGIS + PostGIS + GeoServer / MapLibre / Leaflet)
  - Q3c: Data model — PostGIS schema, raster vs vector, tiling, performance
  - Q3d: Dashboard provenance layer (scenario lineage, confidence badges)
- **Completion:** Architecture diagrams (Mermaid) + stack decision + schema sketch
- **Owner:** architect

## Q4: Quantitative Methods & Validation

- **Question:** Which estimators are appropriate for each layer, and how to validate without proprietary loss history?
- **Why matters:** Avoids "GARCH as centrepiece" trap; earns statistical credibility.
- **Evidence needed:**
  - Transition: logit PD with climate term, LGD models, VAR/BVAR macro, sector EBITDA sensitivities
  - Physical: Poisson for event frequency, GPD/GEV for extremes, damage functions, Monte Carlo
  - Validation: historical .v. observed, OOS 2010-20→21-25, sensitivity (±25% carbon price, ±50% damage), reverse stress
- **Completion:** Method table with assumptions, alternatives rejected, validation checklist
- **Owner:** researcher (methods) → statistical-analyst (validation)

## Q5: Novelty & Contribution Assessment

- **Question:** What is genuinely new vs established vs known combination? Can we claim literature contribution?
- **Why matters:** Determines academic framing and portfolio narrative.
- **Method:** Frontier map (search recent papers 2022-2026 on integrated climate stress testing + GIS credit risk + India/GCC)
- **Completion:** Novelty scoring per idea, with disproof attempts
- **Owner:** researcher

## Q6: Market Demand Mapping

- **Question:** Which GCC banks / Indian banks / corporates / regulators / carbon market participants actually need this?
- **Why matters:** Determines monetization and CV story (climate loans, carbon credits, stress testing).
- **Evidence needed:**
  - GCC: CBUAE, SAMA, QCB, CBK, CBO, CBB climate/ESG guidance; major banks (FAB, Emirates NBD, ADCB, ADIB, SNB, Al Rajhi, QNB, KFH, NBK) — sustainable finance frameworks, TCFD reports
  - India: SBI, HDFC Bank, ICICI, Axis, RBI-regulated entities — climate risk disclosures
  - Corporates: power, steel, cement, aviation, O&G (top emitters, BRSR, CDP)
  - Carbon: CCTS, GCC carbon exchanges (ADGM, PIF, etc.)
- **Completion:** Tiered market map with need-score, use-case, buyer, entry difficulty
- **Owner:** researcher

## Q7: Implementation Roadmap & Risk

- **Question:** Phased build plan with budgets, risks, and credibility guardrails.
- **Why matters:** Prevents 5-year science project; delivers shippable phases.
- **Completion:** Phase 0-3 roadmap, cost (compute/storage), risk register, credibility layer spec
- **Owner:** architect + Intent Director

---

## Dependencies

```
Q1 → Q2 → Q3 → Q4 → Q5
          ↓          ↘
          Q6 ─────────→ Q7
```

Q1 and Q2 can parallelize; Q6 is semi-independent.

## Validation Requirements

- Every claim in Q2 needs source + license + resolution + confidence
- Q3 must pass "would a risk manager understand this?" test
- Q4 must include WHY NOT alternatives
- Q6 must cite primary sources (bank ESG report, regulator guideline), not generic market size
