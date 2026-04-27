class RiskScorer:
    """
    Scores investment risk from three market factors on a 1–5 scale.
    Higher input values = more favourable conditions = lower risk.

    Weights:
        liquidity: 30% — ease of selling the asset
        demand:    30% — rental/buyer demand in the area
        pricing:   40% — current pricing attractiveness
    """

    WEIGHTS = {"liquidity": 0.3, "demand": 0.3, "pricing": 0.4}

    def __init__(self, liquidity: int, demand: int, pricing: int):
        """
        Args:
            liquidity, demand, pricing: Integer scores from 1 (worst) to 5 (best).
        Raises:
            ValueError: If any score is outside the 1–5 range.
        """
        for name, val in [("liquidity", liquidity), ("demand", demand), ("pricing", pricing)]:
            if not (1 <= val <= 5):
                raise ValueError(f"{name} must be between 1 and 5, got {val}")
        self.liquidity = liquidity
        self.demand = demand
        self.pricing = pricing

    def calculate_score(self) -> float:
        """Returns a risk score from 0 (no risk) to 4 (maximum risk)."""
        score = (
            (5 - self.liquidity) * self.WEIGHTS["liquidity"] +
            (5 - self.demand)    * self.WEIGHTS["demand"] +
            (5 - self.pricing)   * self.WEIGHTS["pricing"]
        )
        return round(score, 2)

    def risk_category(self) -> str:
        """Returns Low / Moderate / High Risk based on calculated score."""
        score = self.calculate_score()
        if score <= 2:
            return "Low Risk"
        elif score <= 3.5:
            return "Moderate Risk"
        return "High Risk"
