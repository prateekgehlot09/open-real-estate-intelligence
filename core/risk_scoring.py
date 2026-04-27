class RiskScorer:
    def __init__(self, liquidity, demand, pricing):
        self.liquidity = liquidity
        self.demand = demand
        self.pricing = pricing

    def calculate_score(self):
        score = (
            (5 - self.liquidity) * 0.3 +
            (5 - self.demand) * 0.3 +
            (self.pricing) * 0.4
        )
        return round(score, 2)

    def risk_category(self):
        score = self.calculate_score()
        if score <= 2:
            return "Low Risk"
        elif score <= 3.5:
            return "Moderate Risk"
        else:
            return "High Risk"
