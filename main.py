import argparse
import csv
import os
from core.yield_validator import YieldValidator
from core.risk_scoring import RiskScorer
from models.report_generator import generate_report
from models.ai_analysis import get_ai_insight

DEFAULT_DATA_FILE = "data/sample_dubai_transactions.csv"
DEFAULT_PROJECTED_YIELD = 9.5


def process_property(row: dict, projected_yield: float, use_ai: bool) -> str:
    validator = YieldValidator(
        purchase_price=float(row["price"]),
        annual_rent=float(row["rent"])
    )
    scorer = RiskScorer(
        liquidity=int(row["liquidity"]),
        demand=int(row["demand"]),
        pricing=int(row["pricing"])
    )

    yield_value = validator.calculate_yield()
    yield_grade = validator.yield_grade()
    risk = scorer.risk_category()
    gap = validator.projection_gap(projected_yield)

    data = {
        "location": row["location"],
        "type": row["type"],
        "price": int(row["price"]),
        "yield": yield_value,
        "yield_grade": yield_grade,
        "risk": risk,
        "projection_gap": gap,
        "conclusion": validator.investment_conclusion(risk),
    }

    report = generate_report(data)

    if use_ai:
        ai_insight = get_ai_insight(
            location=row["location"],
            asset_type=row["type"],
            price=int(row["price"]),
            yield_value=yield_value,
            yield_grade=yield_grade,
            projection_gap=gap,
            risk=risk,
        )
        report += f"\nAI Insight (Claude):\n{ai_insight}\n"
        report += "=" * 60 + "\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="OREIL Investment Intelligence")
    parser.add_argument(
        "--file",
        default=DEFAULT_DATA_FILE,
        help="Path to CSV data file (default: data/sample_dubai_transactions.csv)"
    )
    parser.add_argument(
        "--projected-yield",
        type=float,
        default=DEFAULT_PROJECTED_YIELD,
        help="Projected yield benchmark %% (default: 9.5)"
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Skip AI analysis (runs without ANTHROPIC_API_KEY)"
    )
    args = parser.parse_args()

    use_ai = not args.no_ai
    if use_ai and not os.environ.get("ANTHROPIC_API_KEY"):
        print("Warning: ANTHROPIC_API_KEY not set. Running with --no-ai.\n")
        use_ai = False

    with open(args.file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(process_property(row, args.projected_yield, use_ai))


if __name__ == "__main__":
    main()
