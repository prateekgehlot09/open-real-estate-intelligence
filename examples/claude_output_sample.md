# Claude Output Sample — OREIL AI Layer

This document shows a real input/output pair from the OREIL AI analysis layer.
Claude receives structured, pre-validated data and returns investment reasoning.

---

## Input

```
Location       : Business Bay
Asset Type     : 1BR Apartment
Purchase Price : AED 1,500,000
Validated Yield: 7.0%
Yield Grade    : Good
Projection Gap : -2.5%
Risk Category  : Low Risk
```

---

## Claude Prompt Sent

```
You are a senior real estate investment analyst reviewing a validated property report.

Property Details:
- Location: Business Bay
- Type: 1BR Apartment
- Purchase Price: AED 1,500,000
- Validated Gross Yield: 7.0% (Good)
- Projection Gap: -2.5% (actual minus projected benchmark of 9.5%)
- Risk Category: Low Risk

Provide a concise 3-4 sentence investment insight covering:
1. What the validated yield indicates about this asset's income performance
2. What the projection gap reveals about underwriting accuracy
3. What the risk category implies for portfolio positioning
4. One specific actionable recommendation

Be direct and specific. Do not use generic phrases.
Base your analysis strictly on the numbers provided.
```

---

## Claude Response

```
Business Bay's 7.0% yield reflects a stable income profile in a liquid,
high-demand submarket where rental demand is structurally supported by
business district employment. The -2.5% projection gap confirms that
investors underwriting this asset against a 9.5% income return are
mispricing expectations — the validated yield is the ceiling, not the
floor. Low Risk classification supports this as a capital-preservation
holding rather than a high-income generator. Recommendation: underwrite
at 7.0-7.5% yield with no rent growth assumption for the first 24 months;
exit strategy should target capital appreciation, not yield compression.
```

---

## How This Works

1. `main.py` reads property data from CSV
2. `core/yield_validator.py` calculates and grades the yield
3. `core/risk_scoring.py` scores and categorises risk
4. `models/ai_analysis.py` passes the validated outputs to Claude
5. Claude returns reasoning grounded in the structured data
6. `models/report_generator.py` assembles the final report

The AI layer never receives raw transaction data — it only receives
validated, structured outputs from the deterministic models.

---

## Note on AI Output

Claude's insight is interpretive, not financial advice.
All figures in the insight are sourced directly from OREIL's
validated calculations. Claude does not introduce new numbers.
