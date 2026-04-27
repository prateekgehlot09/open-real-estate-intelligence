# Open Real Estate Intelligence Layer (OREIL)

**A working prototype of an open real estate intelligence system that validates yield, identifies projection gaps, scores investment risk, and generates structured AI-powered investment decisions.**

Built for investors, analysts, and developers who need a structured intelligence layer — not another dashboard.

> Built and open-sourced by [Titan Crest Real Estate](https://github.com/prateekgehlot09)

---

## Sample Output

```
============================================================
       OREIL Investment Intelligence Report
============================================================
Asset         : Business Bay
Type          : 1BR Apartment
Purchase Price: AED 1,500,000
------------------------------------------------------------
Validated Yield  : 7.0%
Yield Grade      : Good
Projection Gap   : -2.5%
Risk Category    : Low Risk
------------------------------------------------------------
Conclusion    : Income-stable asset
------------------------------------------------------------

AI Insight (Claude):
Business Bay's 7.0% yield reflects a stable income profile in a
liquid, high-demand submarket. The -2.5% projection gap confirms
investors underwriting at 9.5% are mispricing expectations — the
validated yield is the ceiling, not the floor. Low Risk classification
supports a capital-preservation allocation. Recommendation: underwrite
at 7.0-7.5% with no rent growth assumption for 24 months.
============================================================
```

---

## Use Cases

- **Investor underwriting** — validate yield assumptions before committing capital
- **Broker advisory** — generate structured, defensible investment summaries
- **Market benchmarking** — compare assets across locations against yield targets
- **AI-driven analysis** — layer Claude's reasoning on top of validated financial data
- **Open data standard** — a reusable framework for real estate intelligence tooling

---

## What This Does

- Validates gross rental yield from transaction data
- Grades yield quality (Excellent / Good / Fair / Poor)
- Scores investment risk across liquidity, demand, and pricing factors
- Calculates projection gap against a yield benchmark
- Generates structured investment reports
- Calls Claude to produce AI-powered investment insight on each asset

---

## Run Locally

Requires Python 3.8+.

```bash
# Clone the repo
git clone https://github.com/prateekgehlot09/open-real-estate-intelligence.git
cd open-real-estate-intelligence

# Install dependencies
pip install -r requirements.txt

# Run with AI analysis (requires Anthropic API key)
export ANTHROPIC_API_KEY=your_key_here
python main.py

# Run without AI (no API key needed)
python main.py --no-ai

# Run against a custom dataset with a custom yield benchmark
python main.py --file data/sample_dubai_transactions.csv --projected-yield 8.5
```

---

## Repository Structure

- `core/` — yield validation and risk scoring models
- `models/` — report generation and Claude AI analysis layer
- `data/` — sample transaction datasets (OREIL Data Standard v0.1)
- `docs/` — architecture, data standard, and Claude prompt documentation
- `examples/` — sample outputs across multiple assets and markets
- `tests/` — unit tests for core validation and risk models

---

## Why This Matters for AI

Real estate investment decisions are made on assumptions. Most tools validate nothing — they display data. OREIL is different: it validates assumptions, scores risk, and layers AI reasoning on top of structured financial outputs.

OREIL aims to become:

- A structured dataset layer for real estate AI
- A decision intelligence engine for investor underwriting
- A foundation for AI-driven real estate analysis at scale

---

## Limitations

OREIL v0.1 is a prototype. Current limitations:

- Uses sample datasets only — does not connect to live government transaction registries
- Risk scores (liquidity, demand, pricing) are manually assigned — not yet derived from market data
- Does not provide financial advice — all outputs are informational only
- AI insights are interpretive and depend entirely on validated structured inputs
- Single-market focus (Dubai) — multi-market expansion is Phase 2

---

## Status

Version 0.1 prototype — active development.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Roadmap

See [roadmap.md](roadmap.md).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
