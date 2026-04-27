# OREIL Architecture (v0.1)

## Overview

OREIL is a modular, layered intelligence system for real estate investment analysis.
Each layer has a single responsibility and communicates through well-defined interfaces.
CSV Data → [Data Layer] → [Validation Layer] → [Risk Layer] → [Intelligence Layer] → Report + AI Insight
---

## Layer 1: Data Layer

**Location:** `data/`
**Standard:** OREIL Data Standard v0.1 (see `docs/data_standard.md`)

Accepts CSV files conforming to the OREIL Data Standard. Each row represents
one property. The data layer is stateless — OREIL reads but never writes to
source data.

**Current dataset:** `data/sample_dubai_transactions.csv` (5 properties, Dubai market)

---

## Layer 2: Validation Layer

**Location:** `core/yield_validator.py`
**Class:** `YieldValidator`

Responsibilities:
- Calculate gross rental yield: `(annual_rent / purchase_price) × 100`
- Grade the yield: Excellent (≥8%) / Good (≥6%) / Fair (≥4%) / Poor (<4%)
- Calculate projection gap: `actual_yield - projected_benchmark`

The validation layer is purely deterministic. Given the same inputs it always
produces the same outputs. No randomness, no external calls.

---

## Layer 3: Risk Layer

**Location:** `core/risk_scoring.py`
**Class:** `RiskScorer`

Responsibilities:
- Accept three factor scores (liquidity, demand, pricing) on a 1–5 scale
- Calculate a weighted composite risk score:
  - Liquidity: 30%
  - Demand: 30%
  - Pricing: 40%
- Classify into: Low Risk (≤2.0) / Moderate Risk (≤3.5) / High Risk (>3.5)

Higher input scores = more favourable = lower risk contribution.
The inversion `(5 - score)` converts "favourability" to "risk contribution."

---

## Layer 4: Intelligence Layer

**Location:** `models/`

### 4a. Report Generator (`models/report_generator.py`)

Accepts a validated data dict and formats it into a structured ASCII report.
Purely presentational — no calculation logic.

### 4b. AI Analysis (`models/ai_analysis.py`)

Accepts validated outputs from Layers 2 and 3 and passes them to Claude
via the Anthropic API. Claude reasons over the structured data and returns
a 3–4 sentence investment insight.

**Critical design principle:** Claude receives only validated outputs,
never raw data. The AI layer interprets — it does not calculate.

---

## Entry Point

**Location:** `main.py`

Orchestrates all four layers:
1. Reads CSV via `argparse`-driven CLI
2. Instantiates `YieldValidator` and `RiskScorer` per row
3. Calls `generate_report()` to format structured output
4. Optionally calls `get_ai_insight()` if `ANTHROPIC_API_KEY` is set
5. Prints the final report to stdout

---

## Dependency Graph

main.py
├── core/yield_validator.py     (no dependencies)
├── core/risk_scoring.py        (no dependencies)
├── models/report_generator.py  (no dependencies)
└── models/ai_analysis.py       (depends: anthropic SDK)

Core models have zero external dependencies — they can run offline.
Only the AI layer requires network access and an API key.

---

## Future Architecture (Phase 2+)

- **API layer** — FastAPI wrapper around core models, JSON output
- **Multi-market support** — currency-normalised yield comparison
- **Live data ingestion** — connect to government transaction registries
- **Web interface** — React frontend consuming the API layer
