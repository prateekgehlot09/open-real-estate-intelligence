from unittest.mock import MagicMock, patch
from models.ai_analysis import get_ai_insight


class TestAIAnalysis:
    """Tests for the Claude AI analysis layer using mocked API calls."""

    @patch("models.ai_analysis.anthropic.Anthropic")
    def test_returns_string(self, mock_anthropic):
        """AI insight should return a non-empty string."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content[0].text = (
            "Mocked Claude insight."
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
