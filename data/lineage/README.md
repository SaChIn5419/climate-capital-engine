# data/lineage — per-variable provenance

Each variable gets a YAML/JSON with:

```yaml
variable: borrower_emissions_tco2e
source: BRSR FY24-25 Top 1000 (982 valid) + sector GLM
date: 2026-09-15
unit: tCO2e
transformation: log Revenue + Industry FE → CO2_hat ± CI (±28%)
method: polars OLS + 1000 MC draws
missingness: 57.1% Scope3 missing → estimated
estimation: OBSERVED where disclosed else ESTIMATED
confidence: MEDIUM
provenance: https://www.iimb.ac.in/.../ESG_BR-2026.pdf
model_risk: sector FE may miss firm tech heterogeneity → sensitivity ±30%
```

See `evidence-ledger.md` for ledger template.
