# OREIL API

REST API layer for the OREIL intelligence framework.
Built with FastAPI. Returns JSON for all analysis endpoints.

---

## Run the API

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

API will be available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

---

## Analyse a Property

```bash
curl -X POST http://localhost:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Business Bay",
    "asset_type": "1BR Apartment",
    "price": 1500000,
    "rent": 105000,
    "liquidity": 4,
    "demand": 4,
    "pricing": 3,
    "projected_yield": 9.5,
    "include_ai": false
  }'
```

## With AI Analysis

```bash
export ANTHROPIC_API_KEY=your_key_here

curl -X POST http://localhost:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Business Bay",
    "asset_type": "1BR Apartment",
    "price": 1500000,
    "rent": 105000,
    "liquidity": 4,
    "demand": 4,
    "pricing": 3,
    "projected_yield": 9.5,
    "include_ai": true
  }'
```

## Sample Response

```json
{
  "location": "Business Bay",
  "asset_type": "1BR Apartment",
  "price": 1500000,
  "validated_yield": 7.0,
  "yield_grade": "Good",
  "projection_gap": -2.5,
  "risk_score": 1.4,
  "risk_category": "Low Risk",
  "conclusion": "Income-stable asset. Defensive income play.",
  "ai_insight": null,
  "report": "\n============================================================\n..."
}
```
