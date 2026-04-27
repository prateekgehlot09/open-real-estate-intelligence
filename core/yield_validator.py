class YieldValidator:
    def __init__(self, purchase_price, annual_rent):
        self.purchase_price = purchase_price
        self.annual_rent = annual_rent

    def calculate_yield(self):
        return round((self.annual_rent / self.purchase_price) * 100, 2)
