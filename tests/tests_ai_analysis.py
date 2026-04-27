from unittest.mock import MagicMock, patch
from models.ai_analysis import get_ai_insight
from core.yield_validator import YieldValidator


class TestAIAnalysis:
    """Tests for the Claude AI analysis layer using mocked API calls."""

    @patch("models.ai_analysis.anthropic.Anthropic")
    def test_returns_string(self, mock_anthropic):
        """AI insight should return a non-empty string."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content[0].text = (
            "Mocked Claude insight for testing."
        )
        result = get_ai_insight(
            location="Business Bay",
            asset_type="1BR Apartment",
            price=1500000,
            yield_value=7.0,
            yield_grade="Good",
            projection_gap=-2.5,
            risk="Low Risk",
        )
        assert isinstance(result, str)
        assert len(result) > 0

    @patch("models.ai_analysis.anthropic.Anthropic")
    def test_prompt_contains_location(self, mock_anthropic):
        """Prompt sent to Claude must include the property location."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content[0].text = "Insight."

        get_ai_insight(
            location="Palm Jumeirah",
            asset_type="Villa",
            price=8000000,
            yield_value=5.25,
            yield_grade="Fair",
            projection_gap=-4.25,
            risk="Moderate Risk",
        )
        call_args = mock_client.messages.create.call_args
        prompt_text = call_args[1]["messages"][0]["content"]
        assert "Palm Jumeirah" in prompt_text

    @patch("models.ai_analysis.anthropic.Anthropic")
    def test_prompt_contains_yield(self, mock_anthropic):
        """Prompt sent to Claude must include the validated yield value."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content[0].text = "Insight."

        get_ai_insight(
            location="JVC",
            asset_type="Studio",
            price=600000,
            yield_value=7.5,
            yield_grade="Good",
            projection_gap=-2.0,
            risk="Moderate Risk",
        )
        call_args = mock_client.messages.create.call_args
        prompt_text = call_args[1]["messages"][0]["content"]
        assert "7.5" in prompt_text

    @patch("models.ai_analysis.anthropic.Anthropic")
    def test_api_called_once_per_property(self, mock_anthropic):
        """Claude API should be called exactly once per property analysis."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content[0].text = "Insight."

        get_ai_insight(
            location="Dubai Marina",
            asset_type="1BR Apartment",
            price=1400000,
            yield_value=7.0,
            yield_grade="Good",
            projection_gap=-2.5,
            risk="Low Risk",
        )
        assert mock_client.messages.create.call_count == 1

    def test_investment_conclusion_high_yield_low_risk(self):
        """Excellent yield + Low Risk should return the strongest conclusion."""
        v = YieldValidator(1000000, 90000)  # 9.0% → Excellent
        result = v.investment_conclusion("Low Risk")
        assert "High-yield" in result

    def test_investment_conclusion_poor_yield(self):
        """Poor yield should return capital-play-only conclusion."""
        v = YieldValidator(10000000, 100000)  # 1.0% → Poor
        result = v.investment_conclusion("High Risk")
        assert "Capital play only" in result
