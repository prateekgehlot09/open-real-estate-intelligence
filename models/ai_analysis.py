import anthropic


def get_ai_insight(
    location: str,
    asset_type: str,
    price: int,
    yield_value: float,
    yield_grade: str,
    projection_gap: float,
    risk: str,
) -> str:
    """
    Calls the Claude API to generate an AI-powered investment insight
    for a given property based on validated yield and risk data.

    Args:
        location:        Property location (e.g. "Business Bay")
        asset_type:      Property type (e.g. "1BR Apartment")
        price:           Purchase price in AED
        yield_value:     Validated gross rental yield (%)
        yield_grade:     Human-readable yield grade (Excellent/Good/Fair/Poor)
        projection_gap:  Actual yield minus projected yield (%)
        risk:            Risk category (Low Risk / Moderate Risk / High Risk)

    Returns:
        AI-generated insight string from Claude.

    Raises:
        anthropic.APIError: If the API call fails.
    """
    client = anthropic.Anthropic()

    prompt = f"""You are a senior real estate investment analyst reviewing a validated property report.

Property Details:
- Location: {location}
- Type: {asset_type}
- Purchase Price: AED {price:,}
- Validated Gross Yield: {yield_value}% ({yield_grade})
- Projection Gap: {projection_gap}% (actual minus projected benchmark of {yield_value - projection_gap:.1f}%)
- Risk Category: {risk}

Provide a concise 3-4 sentence investment insight covering:
1. What the yield and projection gap indicate about this asset's income performance
2. What the risk category implies for an investor's portfolio positioning
3. One specific actionable recommendation

Be direct and specific. Do not use generic phrases. Base your analysis strictly on the numbers provided."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
  
    return message.content[0].text  
    return message.content[0].text
