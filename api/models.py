from pydantic import BaseModel, Field, field_validator


class PropertyRequest(BaseModel):
    """Request schema for a single property analysis."""

    location: str = Field(..., example="Business Bay")
    asset_type: str = Field(..., example="1BR Apartment")
    price: float = Field(..., gt=0, example=1500000)
    rent: float = Field(..., ge=0, example=105000)
    liquidity: int = Field(..., ge=1, le=5, example=4)
    demand: int = Field(..., ge=1, le=5, example=4)
    pricing: int = Field(..., ge=1, le=5, example=3)
    projected_yield: float = Field(default=9.5, ge=0, example=9.5)
    include_ai: bool = Field(default=False)

    @field_validator("location", "asset_type")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field must not be empty")
        return v.strip()


class PropertyResponse(BaseModel):
    """Response schema for a single property analysis."""

    location: str
    asset_type: str
    price: float
    validated_yield: float
    yield_grade: str
    projection_gap: float
    risk_score: float
    risk_category: str
    conclusion: str
    ai_insight: str | None = None
    report: str
