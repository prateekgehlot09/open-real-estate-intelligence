"""Tests for models.ai_analysis. The Anthropic SDK call is mocked so tests
run offline and require no API key."""
from unittest.mock import patch, MagicMock
import pytest


def test_ai_insight_returns_string_when_enabled(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")

    from models import ai_analysis

    fake_message = MagicMock()
    fake_message.content = [MagicMock(text="Mocked Claude reasoning about Business Bay.")]

    fake_client = MagicMock()
    fake_client.messages.create.return_value = fake_message

    with patch.object(ai_analysis, "Anthropic", return_value=fake_client):
        result = ai_analysis.generate_insight(
            location="Business Bay",
            asset_type="1BR Apartment",
            validated_yield=7.0,
            risk_category="Moderate Risk",
            conclusion="Income-stable asset with moderate market sensitivity.",
        )

    assert isinstance(result, str)
    assert len(result) > 0


def test_ai_insight_disabled_without_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    from models import ai_analysis

    result = ai_analysis.generate_insight(
        location="Business Bay",
        asset_type="1BR Apartment",
        validated_yield=7.0,
        risk_category="Moderate Risk",
        conclusion="Income-stable asset with moderate market sensitivity.",
    )

    # When no key is set, the integration should degrade gracefully,
    # not crash. Either return None or a clear "AI disabled" string.
    assert result is None or "disabled" in result.lower() or "unavailable" in result.lower()
