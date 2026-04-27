import pytest
from core.yield_validator import YieldValidator
from core.risk_scoring import RiskScorer

class TestYieldValidator:
    def test_standard_yield(self):
        v = YieldValidator(1500000, 105000)
        assert v.calculate_yield() == 7.0

    def test_projection_gap_negative(self):
        v = YieldValidator(1500000, 105000)
        assert v.projection_gap(9.5) == -2.5

    def test_zero_price_raises(self):
        with pytest.raises(ValueError):
            YieldValidator(0, 105000)

    def test_negative_rent_raises(self):
        with pytest.raises(ValueError):
            YieldValidator(1500000, -1)

    def test_yield_grade_good(self):
        v = YieldValidator(1500000, 105000)  # 7.0% → Good
        assert v.yield_grade() == "Good"

    def test_yield_grade_excellent(self):
        v = YieldValidator(1000000, 90000)   # 9.0% → Excellent
        assert v.yield_grade() == "Excellent"

class TestRiskScorer:
    def test_low_risk_category(self):
        s = RiskScorer(4, 4, 3)
        assert s.risk_category() == "Low Risk"

    def test_high_risk_category(self):
        s = RiskScorer(1, 1, 1)
        assert s.risk_category() == "High Risk"

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError):
            RiskScorer(6, 4, 3)

    def test_score_calculation(self):
        s = RiskScorer(4, 4, 3)
        # (1)*0.3 + (1)*0.3 + (2)*0.4 = 1.4
        assert s.calculate_score() == 1.4
