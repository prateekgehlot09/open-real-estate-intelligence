class YieldValidator:
    def __init__(self, purchase_price, annual_rent):
        if purchase_price <= 0:
            raise ValueError("Purchase price must be greater than zero")
        if annual_rent < 0:
            raise ValueError("Annual rent cannot be negative")
        self.purchase_price = purchase_price
        self.annual_rent = annual_rent

    def calculate_yield(self):
        return round((self.annual_rent / self.purchase_price) * 100, 2)

    def projection_gap(self, projected_yield):
        actual = self.calculate_yield()
        return round(actual - projected_yield, 2)
