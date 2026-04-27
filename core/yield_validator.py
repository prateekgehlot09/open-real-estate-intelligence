class YieldValidator:
    """Validates rental yield and compares against projected benchmarks."""

    YIELD_GRADES = [
        (8.0, "Excellent"),
        (6.0, "Good"),
        (4.0, "Fair"),
        (0.0, "Poor"),
    ]

    def __init__(self, purchase_price: float, annual_rent: float):
        """
        Args:
            purchase_price: Property purchase price in local currency.
            annual_rent: Annual rental income in local currency.
        Raises:
            ValueError: If purchase_price <= 0 or annual_rent < 0.
        """
        if purchase_price <= 0:
            raise ValueError("Purchase price must be greater than zero")
        if annual_rent < 0:
            raise ValueError("Annual rent cannot be negative")
        self.purchase_price = purchase_price
        self.annual_rent = annual_rent

    def calculate_yield(self) -> float:
        """Returns gross rental yield as a percentage, rounded to 2dp."""
        return round((self.annual_rent / self.purchase_price) * 100, 2)

    def projection_gap(self, projected_yield: float) -> float:
        """Returns actual yield minus projected yield. Negative = underperforming."""
        return round(self.calculate_yield() - projected_yield, 2)

    def yield_grade(self) -> str:
        """Returns a human-readable grade for the calculated yield."""
        y = self.calculate_yield()
        for threshold, grade in self.YIELD_GRADES:
            if y >= threshold:
                return grade
        return "Poor"
