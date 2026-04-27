# OREIL Data Standard v0.1

This document defines the required data format for OREIL-compatible datasets.
Any dataset conforming to this standard can be processed by OREIL without modification.

---

## Purpose

The OREIL Data Standard allows real estate assets to be compared consistently
across markets, asset types, and time periods. It is designed to be:

- **Minimal** — only fields that directly affect yield and risk calculation
- **Extensible** — optional fields can be added without breaking core models
- **Market-agnostic** — works for any currency and geography

---

## Required Fields

| Field | Type | Constraints | Description |
|---|---|---|---|
| `property_id` | integer | unique, > 0 | Unique asset identifier |
| `location` | string | non-empty | Sub-market or neighbourhood name |
| `type` | string | non-empty | Asset type (e.g. "1BR Apartment", "Studio", "Villa") |
| `price` | number | > 0 | Purchase price in local currency |
| `rent` | number | >= 0 | Annual rental income in local currency |
| `liquidity` | integer | 1–5 | Market liquidity score (5 = most liquid) |
| `demand` | integer | 1–5 | Rental/buyer demand score (5 = highest demand) |
| `pricing` | integer | 1–5 | Pricing attractiveness score (5 = most attractive) |

---

## Risk Score Definitions

All three risk scores use the same 1–5 scale where **5 = most favourable**.

**Liquidity (1–5)**
How easily the asset can be sold without significant price discount.
- 5: Highly liquid market, assets sell within 30 days
- 3: Average liquidity, typical 60–90 day sale cycle
- 1: Illiquid, distressed or niche asset class

**Demand (1–5)**
Current rental and buyer demand in the sub-market.
- 5: Strong oversupply of buyers/tenants, sub-1% vacancy
- 3: Balanced market, normal vacancy rates
- 1: Weak demand, high vacancy, incentivised rents

**Pricing (1–5)**
Current pricing attractiveness relative to intrinsic value.
- 5: Asset is undervalued relative to comparable transactions
- 3: Fairly priced at market rate
- 1: Overpriced relative to rental yield and comparables

---

## CSV Format

Files must be UTF-8 encoded CSV with a header row.

```csv
property_id,location,type,price,rent,liquidity,demand,pricing
1,Business Bay,1BR Apartment,1500000,105000,4,4,3
```

---

## Optional Fields (v0.2+)

The following fields are reserved for future versions:

| Field | Type | Description |
|---|---|---|
| `country` | string | ISO 3166-1 alpha-2 country code |
| `currency` | string | ISO 4217 currency code |
| `transaction_date` | date | YYYY-MM-DD format |
| `source` | string | Data source identifier |

---

## Validation

All required fields are validated at runtime by OREIL's core models:
- `price > 0` enforced by `YieldValidator`
- `rent >= 0` enforced by `YieldValidator`
- `1 <= liquidity, demand, pricing <= 5` enforced by `RiskScorer`

Invalid rows will raise a `ValueError` with a descriptive message.

---

## Reference Implementation

See `data/sample_dubai_transactions.csv` for a conforming example dataset.
