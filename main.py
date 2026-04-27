from core.yield_validator import YieldValidator
from core.risk_scoring import RiskScorer
from models.report_generator import generate_report

validator = YieldValidator(1500000, 105000)
yield_value = validator.calculate_yield()

scorer = RiskScorer(4, 4, 3)
risk = scorer.risk_category()

gap = validator.projection_gap(9.5)

data = {
    "location": "Business Bay",
    "type": "1BR Apartment",
    "price": 1500000,
    "yield": yield_value,
    "risk": risk,
    "projection_gap": gap,
    "conclusion": "Income-stable asset",
}

print(generate_report(data))
