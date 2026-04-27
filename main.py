import argparse
import csv
from core.yield_validator import YieldValidator
from core.risk_scoring import RiskScorer
from models.report_generator import generate_report

DEFAULT_DATA_FILE = "data/sample_dubai_transactions.csv"
DEFAULT_PROJECTED_YIELD = 9.5
DEFAULT_RISK_SCORES = {"liquidity": 4, "demand": 4, "pricing": 3}

def process_property(row, projected_yield, risk_scores):
    validator = YieldValidator(
        purchase_price=float(row["price"]),
        annual_rent=float(row["rent"])
    )
    scorer = RiskScorer(
        liquidity=risk_scores["liquidity"],
        demand=risk_scores["demand"],
        pricing=risk_scores["pricing"]
    )
    data = {
        "location": row["location"],
        "type": row["type"],
        "price": int(row["price"]),
        "yield": validator.calculate_yield(),
        "risk": scorer.risk_category(),
        "projection_gap": validator.projection_gap(projected_yield),
        "conclusion": "Income-stable asset",
    }
    return generate_report(data)

def main():
    parser = argparse.ArgumentParser(description="OREIL Investment Intelligence")
    parser.add_argument("--file", default=DEFAULT_DATA_FILE, help="Path to CSV data file")
    parser.add_argument("--projected-yield", type=float, default=DEFAULT_PROJECTED_YIELD,
                        help="Projected yield benchmark (%)")
    args = parser.parse_args()

    with open(args.file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(process_property(row, args.projected_yield, DEFAULT_RISK_SCORES))

if __name__ == "__main__":
    main()
