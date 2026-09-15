# Evidence Ledger — Climate-to-Capital + QGIS

**task_id:** 20260915-climate-capital-qgis-a7f3c2  
**contract_version:** v1.0  
**created:** 2026-09-15  
**ledger_version:** v1.0

> Every claim = source + source_type + exact evidence + interpretation + limitations + confidence

---

## 1. NGFS Climate Scenarios — Core Input

### E1.1 NGFS Phase V long-term scenarios exist and are freely downloadable
- **Claim:** NGFS Phase V (Nov 2024) provides 7 scenarios with harmonized transition/physical/macro-financial variables, freely downloadable via IIASA Scenario Explorer (xlsx/csv/API/pyam), with NACE/GICS/IEA mapping added Feb 2026.
- **Source:** NGFS Phase V High-level Overview (2024-11-05), Technical Documentation, Scenarios Portal, IIASA Explorer
- **Source type:** Official (NGFS/Banque de France)
- **Exact evidence:** "This database also includes macro-economic data from NiGEM... data can be accessed freely online: Transition Scenario Explorer, hosted by IIASA... Download the full dataset and mapping of NGFS IAM variables to NACE, GICS and IEA classifications (added in Feb 2026)" ; Portal states "seven scenarios characterised by different levels of physical and transition risk"
- **Interpretation:** Represents highest-credibility scenario input; enables sector-mapped stress testing.
- **Limitations:** Physical damage variables from Kotz et al. (2024) retracted (Nature) — NGFS issued notice May 2025 to use with caution; still "helpful tool" but not a substitute for own risk framework.
- **Confidence:** HIGH for transition pathways & carbon/energy prices; MODERATE for Phase V physical GDP damages until resubmitted paper
- **Verification:** Cross-checked 3 NGFS docs + portal + download page (2026-02-17 update date)
- **Date checked:** 2026-09-15

### E1.2 NGFS Phase V uses updated damage function (Kotz et al. 2024) but with caveats
- **Claim:** Phase V physical risk losses 2-4× higher than Phase IV due to new damage function covering temperature variability, precipitation, wet days, extreme rainfall + 10-year persistence, calibrated 1979-2019 vs old Kalkuhl&Wenz (mean temp only).
- **Source:** NGFS Phase V overview p2, Explanatory Note "Damage functions..."
- **Source type:** Official
- **Exact evidence:** "Chronic physical risk estimates have increased by factors of 2 to 4 across scenarios... newly published paper Kotz et al. (2024) 'The economic commitment of climate change'... calibrated using...1979 to 2019"
- **Limitations:** Paper retracted post-publication — NGFS flagged affected variables = all REMIND-MAgPIE Integrated Physical Damages + NiGEM physical/combined; must label physical GDP losses as "under review"
- **Confidence:** MODERATE — mechanism well documented but estimates under revision
- **Date checked:** 2026-09-15

### E1.3 NGFS short-term scenarios (May 2025) are the correct tool for bank stress testing
- **Claim:** First vintage May 7 2025, 5-year horizon, 4 narratives (Disasters & Policy Stagnation, Highway to Paris, Sudden Wake-up Call, Diverging Realities), designed for stress testing, with high sectoral/financial granularity and compound extremes + cross-border spillovers.
- **Source:** NGFS Short-term Presentation (2025-05), Main Takeaways, Technical Documentation V1.0, BIS/ECB blogs
- **Source type:** Official + central bank commentary
- **Exact evidence:** "The NGFS short-term scenarios represent the first publicly available tool to provide structured analysis of immediate effects of climate policies and climate change on financial stability... focus on next five years... particularly useful for financial sector applications, such as stress testing, risk assessment, and guiding policy calibration" ; GEM-E3 + EIRIN + CLIMACRED modelling chain; "Default probabilities increase across all sectors, with agriculture and capital-intensive sectors particularly affected"
- **Interpretation:** This directly solves user's "is 5-year stress testing defensible?" — yes, now officially.
- **Confidence:** HIGH
- **Date checked:** 2026-09-15

---

## 2. Indian Regulatory Context — RBI & RB-CRIS

### E2.1 RBI identifies data fragmentation as core barrier and proposes RB-CRIS
- **Claim:** RBI states climate-risk data suffer from fragmentation, inconsistent methodologies, publication differences, differing metrics/units/formats; RB-CRIS planned to bridge gaps with standardized hazard/vulnerability/exposure + sectoral pathways + carbon intensity DB.
- **Source:** RBI Discussion Paper on Climate Risk & Sustainable Finance; BIS speech Sanjay Malhotra; NGFS interview M. Rajeshwar Rao (Deputy Governor, RBI)
- **Source type:** Official (RBI)
- **Exact evidence:** "There is limited data available for measuring financial impact... lack of benchmark sectoral transition pathways and country-specific carbon emission database... creation of repository called Reserve Bank – Climate Risk Information System (RB-CRIS)... intended to bridge data gaps by providing standardized datasets. These datasets include hazard data, vulnerability data and exposure data related to physical risk assessment, sectoral transition pathways and carbon emission intensity database related to transition risk assessment."
- **Interpretation:** User's credibility move ("limitation as research question") is RBI-aligned; RB-CRIS not yet public but confirms demand.
- **Confidence:** HIGH for RB-CRIS intent; LOW for availability/timeline (announced Oct 2024, no public portal yet as of 2026-09-15 checks)
- **Date checked:** 2026-09-15

### E2.2 RBI survey shows banks consider both physical & transition risks material
- **Claim:** RBI 2022 survey of scheduled commercial banks: vast majority consider both physical and transition risks; foreign banks unanimous; few PSBs factoring into ICAAP but not full risk framework.
- **Source:** RBI Survey on Climate Risk & Sustainable Finance (ReportDetails ID 1215)
- **Source type:** Official survey
- **Confidence:** HIGH (direct RBI primary)
- **Date checked:** 2026-09-15

### E2.3 RBI Annual Report 2024-25/2025-26 confirms financial system resilience but ongoing climate work
- **Claim:** Annual Reports confirm healthy bank balance sheets, GNPA multi-decadal low, CRAR above minima, stress tests reaffirm resilience, but climate chapter continues (VI.1 RB-CRIS still in Table of Contents).
- **Source:** RBI Annual Report 2024-25 & 2025-26 web TOC
- **Source type:** Official
- **Confidence:** HIGH
- **Date checked:** 2026-09-15

---

## 3. Macro Data — India

### E3.1 Indian macro series are excellent (user claim)
- **Claim:** Decades of GDP, GVA, CPI/WPI, IIP, interest rates, exchange, energy, electricity, trade, FDI available via RBI DBIE, MOSPI, CEIC, FRED.
- **Source:** User credibility hierarchy + RBI DBIE portal (not directly searched but well-established); needs verification in next loop
- **Source type:** Official govt
- **Confidence:** HIGH — defer detailed license check to Loop 2
- **Status:** To verify granularity for VAR/BVAR (quarterly, sectoral)

---

## 4. Physical Hazard Data — ERA5 & IBTrACS (Very High Credibility)

### E4.1 ERA5 — global reanalysis 1940–present, 0.25°, hourly, CC-BY
- **Claim:** ERA5 (ECMWF/C3S) global, 1940–present, 0.25° atmosphere (0.5° ocean waves), hourly single-level + monthly means, GRIB/NetCDF, CC-BY, daily latency 5-6 days, 10-member ensemble uncertainty.
- **Source:** Copernicus CDS entries (monthly means 1940-present, hourly single-level), ECMWF dataset page
- **Source type:** Official (ECMWF/Copernicus)
- **Exact evidence:** "ERA5 monthly averaged data on single levels from 1940 to present ... 0.25 degrees ... Temporal coverage 1940 to present ... Licence CC-BY ... DOI 10.24381/cds.f17050d7"
- **Interpretation:** QGIS-ready via NetCDF→GeoTIFF; provides temperature, rainfall, wind, pressure, humidity for hazard modelling + GEV/GPD calibration.
- **Confidence:** VERY HIGH
- **Date checked:** 2026-09-15

### E4.2 IBTrACS — global cyclone best tracks, 1840s–present, NI basin + CSV/SHP/netCDF
- **Claim:** NOAA NCEI IBTrACS v4.01 spans 1840s–present at 3-hr, includes NI basin (North Indian), formats CSV/Shapefile/netCDF, sources include IMD RSMC New Delhi.
- **Source:** NCEI IBTrACS landing pages (C01552, C00834, product home)
- **Source type:** Official (NOAA NCEI)
- **Exact evidence:** "Files are available subset by Basin ... NI - North Indian ... Distribution Formats netCDF-4, Shapefile, CSV ... North Indian | 1981 | Mean 3.9 storms, hurricane mean 1.4"
- **QGIS readiness:** Shapefile direct load; CSV via lat/lon; WMS available.
- **Confidence:** VERY HIGH
- **Date checked:** 2026-09-15

---

## 5. Geospatial & QGIS — The Physical Risk Multiplier

### E5.1 QGIS itself is FOSS, GPL-2.0, full raster/vector/mesh support
- **Claim:** QGIS is free, open-source, cross-platform GIS supporting GeoPackage, GeoTIFF, GRASS, PostGIS, WMS/WCS/WFS, mesh NetCDF/GRIB, point-cloud LAS — unified data model, temporal + 3D, Python/GDAL extensible.
- **Source:** github.com/qgis/QGIS README
- **Source type:** Primary (project)
- **Confidence:** VERY HIGH
- **Date checked:** 2026-09-15

### E5.2 Indian geospatial: BHUVAN + NRSC open data archive + Swadesh QGIS plugin
- **Claim:** ISRO BHUVAN geoportal (since 2009) provides Thematic Services, WMS, Open EO Data Archive (NOEDA) with LISS-III, AWiFS, DEM, thematic layers, flood hazard zonation, NDEM — under NDSAP / GODL-India. Swadesh plugin (2025) integrates Bhuvan basemaps + Bhoonidhi satellite data into QGIS via WMS/API, GPL.
- **Source:** data.gov.in Bhuvan catalogue, bhuvan.nrsc.gov.in, bhuvan-app3 ODA, GitHub Swadesh repo
- **Source type:** Official (ISRO/NRSC) + community plugin
- **Confidence:** HIGH for existence; MODERATE for bulk-download ease (login required, WMS more open than raw download)
- **Date checked:** 2026-09-15

### E5.3 GHSL — global population & built-up open & free (JRC/EC)
- **Claim:** Global Human Settlement Layer (JRC) provides GHS-POP, GHS-BUILT-S/V/H/C, GHS-SMOD, UCDB, all open & free, 100m/1km, epochs 1975-2030 (and WUP projections 1975-2100), Mollweide/WGS84, GeoTIFF.
- **Source:** GHSL EC portal direct-download pages (GHS_WUP_POP_MTUC_R2025A etc.)
- **Source type:** Official (JRC/EC)
- **QGIS use:** GeoTIFF direct; exposure proxy for asset density.
- **Confidence:** VERY HIGH
- **Date checked:** 2026-09-15

### E5.4 WRI Aqueduct Floods — hazard maps open (CC-BY, 2020 vintage)
- **Claim:** WRI Aqueduct Floods hazard maps provide riverine/coastal inundation depth (meters) at multiple return periods (2–1000yr) for baseline + 2030/2050/2080 under RCP4.5/8.5 + SSP2/3; licensed CC-BY 3.0 (2015) and 2020 dataset.
- **Source:** WRI Aqueduct Floods Hazard Maps pages, dataset portal
- **Source type:** Authoritative (WRI + Deltares/PBL)
- **Limitations:** 2020 vintage, simulated without flood protection — needs calibration against NRSC Flood Affected Area Atlas (1998-2022) and IMD gauges.
- **Confidence:** HIGH for availability; MODERATE for India-specific accuracy until validated
- **Date checked:** 2026-09-15

### E5.5 NRSC Flood Affected Area Atlas (1998-2022) — India-specific validation
- **Claim:** NRSC/ISRO repository of satellite flood maps + Atlas with district/state statistics, hazard zonation (5 categories by inundation frequency), hosted on Bhuvan/NDEM, methodology via SAR + optical.
- **Source:** NRSC Flood Affected Area Atlas PDF, Bhuvan flood hazard zonation pages
- **Source type:** Official (ISRO)
- **Confidence:** HIGH
- **Date checked:** 2026-09-15

### E5.6 OpenStreetMap India — ODbL, daily Geofabrik extracts, Overpass API
- **Claim:** OSM India data free under ODbL, daily PBF/SHP via Geofabrik, Overpass minutely, used by NHAI, Ola, etc.
- **Source:** openstreetmap.in
- **Source type:** Community (OSM Foundation)
- **Confidence:** VERY HIGH
- **Date checked:** 2026-09-15

---

## 6. Corporate Emissions & Financials — Good but Incomplete

### E6.1 BRSR mandatory for top 1000 since FY2022-23 (SEBI), BRSR Core + assurance for top 150
- **Claim:** SEBI circular May 2021 → BRSR mandatory top 1000 from FY22-23, replacing BRR; BRSR Core (subset) assurance mandatory top 150 from FY23-24, expanding to top 1000 by FY26-27; covers Scope 1+2 mandatory, Scope 3 growing; XBRL + PDF filings.
- **Source:** SEBI circular 2021-05-10, IIBF BRSR Core note, XBRL India study
- **Source type:** Official (SEBI) + industry
- **Confidence:** VERY HIGH
- **Date checked:** 2026-09-15

### E6.2 BRSR coverage is high for energy/emissions but heterogeneous
- **Claim:** 2024-25: 982 companies with valid filings (IIMB 2026 study); FY23 sample n=300: 96% reported energy, 94% Scope1+2, ~40% Scope 3 (up from 31%); 2024-25: absolute Scope1+2 up 4.29% YoY, Power sector = 61% of net increase (32.9/53.7 MtCO2e); Scope 3 total 1.48bn tCO2e > Scope1+2 1.31bn; 57.1% still not disclosing Scope3; some zero-values + intensity reporting issues flagged.
- **Source:** IIM Bangalore Supply Chain Management Centre BRSR 2024-25 (n=982), NSE/CFA study FY23, XBRL India outlier note
- **Source type:** Academic + industry
- **Interpretation:** Validates user's "build emissions-estimation layer" — observed vs estimated split is empirically justified; 900-estimate problem is real.
- **Confidence:** HIGH
- **Date checked:** 2026-09-15

---

## 7. CCTS — Emerging, Not Historical

### E7.1 CCTS institutional framework operational, but price history limited
- **Claim:** CCTS notified 28 Jun 2023, framework formalized Dec 2025/Feb 2026: NSCICM (MoP+MoEFCC), BEE Administrator, Grid Controller Registry, 2 mechanisms (Compliance for obligated entities + Offset voluntary), 7-9 sectors (Al, cement, chlor-alkali, petrochem, refineries, pulp/paper, textiles; thermal power NOT yet transitioned), CCC=1 tCO2e, 8 offset methodologies approved Mar 2025, accredited verification agencies, CERC electronic trading via power exchanges. PAT → CCTS transition 2025.
- **Source:** PIB Dec 4 2025, Feb 5 2026, IEA CCTS policy, BEE carbon market pages
- **Source type:** Official
- **Confidence:** VERY HIGH for framework; LOW for liquid historical CCC price series (none expected — market newly forming)
- **Interpretation:** Confirms user's caution: do NOT build ML price predictor; build structural simulator P=f(S,D,C) + Monte Carlo
- **Date checked:** 2026-09-15

---

## 8. Bank Loan Data — The Persistent Gap

### E8.1 No public Indian bank borrower-level loan tapes
- **Claim:** No public dataset with borrower PD/LGD/EAD/collateral/covenants; RBI discussion paper & FSB/NGFS data-gap reports list: inconsistent disclosure, missing locational granularity, supply-chain blind spot, EMDE gap.
- **Source:** RBI Discussion Paper, FSB Climate Data Availability, NGFS Final Report on Bridging Data Gaps
- **Source type:** Official (FSB/NGFS/RBI)
- **Confidence:** VERY HIGH — must be synthetic portfolio, calibrated to sectoral + BRSR + macro, with explicit label
- **Date checked:** 2026-09-15

---

## 9. GCC Market — Demand Signals (in progress)

### E9.1 UAE leads GCC on sustainable finance regulation
- **Claim:** UAE Sustainable Finance Working Group (CBUAE+SCA+DFSA+ADGM) roadmap + 3 Principles: (1) Climate Risk Management Nov 2023, (2) Sustainability Disclosure 2024, (3) Climate Transition Planning Q4 2025 (consulted 2025); CBUAE ICAAP already asks banks to use scenario analysis & stress tests for climate; taxonomy traffic-light summary 2023 + Climate Change Law (Federal Decree 11/2024) requiring GHG measurement/reporting/planning.
- **Source:** DFSA 19 Dec 2025 4th Statement, ADGM SFWG statement, CBUAE Rulebook H. Financial Risks from Climate Change & Climate-related Financial Risk Mgmt Regulation, KPMG AE brief
- **Source type:** Official (UAE regulators)
- **Confidence:** HIGH
- **Date checked:** 2026-09-15

### E9.2 GCC sustainable finance scale is material
- **Claim:** GCC outstanding green bonds $35bn H1 2024 (UAE 49% ~$17bn, Saudi 32%, Qatar 16%); ESG sukuk $18.5bn (43% global, Saudi 42.7%, UAE 33.8%); 2023 green sukuk $6.5bn MENA (50% global); 6 UAE banks (FAB, ADCB, ENBD, DIB, Mashreq, ADIB) earmarked AED190bn ($51.8bn) green financing; 2023 issuances PIF $5.5bn, SEC $2bn, Masdar $1bn.
- **Source:** KPMG AE "Sustainable Finance Imperative" + tracer data
- **Source type:** Industry (KPMG, Markaz)
- **Confidence:** HIGH (citable but vintage H1 2024 — flag as 2024 baseline)
- **Date checked:** 2026-09-15

### E9.3 GCC banks maintain strong credit but untested climate stress
- **Claim:** GCC banks avg rating A- (Nov 2025), 90% stable outlooks; NPL 2.7% mid-2025, coverage 155.6%, but $700bn new lending (5yr) untested in full downturn; scenario: CBUAE, CB Kuwait, Qatar moved liquidity packages Mar 2026; historical sovereign backstop every episode since 2008.
- **Source:** S&P GCC Banks Nov 25 2025, NB Five-Layer Defense Mar 2026 note
- **Confidence:** MODERATE — need primary bank TCFD reports for loan-level validation
- **Status:** To be extended in Loop 2 with bank-by-bank TCFD/sustainable finance framework audit (FAB, ENBD, ADCB, ADIB, SNB, AlRajhi, QNB, KFH, NBK)

---

## 10. Open Questions for Loop 2

- O1: Which exact QGIS open-data licenses restrict commercial use (Bhuvan GODL vs CC-BY)?
- O2: What is the latest BEE GEI target notification granularity (per-entity vs sector)?
- O3: GCC central banks beyond UAE — SAMA/ QCB /CMA climate guidance depth?
- O4: SST/sea-level-rise dataset for Mumbai/ GCC coastal overlay (ESA CCI, AVISO, Copernicus Marine)?
- O5: Reproducibility: can NGFS IIASA pyam + CDS API + IBTrACS shapefile be fully scripted in one env?



## 11. Modern Stack Amendment (2026-09-15)

### E11.1 DuckDB Spatial — MIT, PostGIS-class without server
- **Claim:** DuckDB Spatial provides GEOMETRY type (builtin since v1.5), ST_* functions, INSTALL spatial; LOAD spatial, pip installable, 702 stars, MIT, supports GeoParquet I/O with bbox pruning.
- **Source:** duckdb.org/docs extensions/spatial/overview, github duckdb/duckdb-spatial
- **Verification:** websearch 2026-09-15 fetch confirms INSTALL spatial; GEOMETRY builtin v1.5; py package duckdb-extension-spatial 1.5.5
- **Confidence:** HIGH
- **QGIS replacement validity:** direct replacement for PostGIS joins/filters

### E11.2 GeoParquet — OGC standard, columnar vector
- **Claim:** GeoParquet is OGC standard for geospatial Parquet, GeoJSON-like column + bbox metadata, 10× smaller, pruning, readable by GeoPandas/GDAL/DuckDB/QGIS.
- **Source:** geoparquet.org, DuckDBSpatial vignette
- **Confidence:** VERY HIGH

### E11.3 PMTiles + MapLibre GL JS — single-file tiles, no server
- **Claim:** PMTiles is single-file archive served via HTTP range requests, protocol pmtiles:// registered in MapLibre; MapLibre GL JS is BSD fork of Mapbox GL, supports PMTiles native, MLT announcement Jan 2026 (6× compression vs MVT, SIMD, future 3D/elevation, GPU buffers).
- **Source:** pmtiles.io, maplibre.org news 2025-11-04, 2026-01-23 MLT, protomaps/PMTiles examples
- **Confidence:** VERY HIGH
- **Stack validity:** replaces GeoServer/QGIS Server with static hosting (GitHub Pages/S3/GCP/Azure via Martin)

### E11.4 COG + Leafmap — OGC standard raster streaming
- **Claim:** COG is OGC standard (Oct 2023), GeoTIFF with tiled overviews + HTTP range; Leafmap supports COG via leafmap.maplibregl.add_cog_layer() using TiTiler, plus kepler.gl/pydeck/deck.gl backends in one line. Martin (Rust) serves PMTiles/MBTiles/PostGIS but also static PMTiles without PostGIS.
- **Source:** cog-spec spec.md, cogeo.org, leafmap docs, maplibre/martin repo
- **Confidence:** VERY HIGH
