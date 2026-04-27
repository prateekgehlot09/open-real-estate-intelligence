import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.models import PropertyRequest, PropertyResponse
from core.yield_validator import YieldValidator
from core.risk_scoring import RiskScorer
from models.report_generator import generate_report
from models.ai_analysis import get_ai_insight

app = FastAPI(
    title="OREIL API",
    description=(
        "Open Real Estate Intelligence Layer — "
        "Titan Crest decision intelligence framework"
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "service": "OREIL API",
        "version": "0.1.0",
        "status": "operational",
        "powered_by": "Titan Crest Real Estate",
    }


@app.post("/analyse", response_model=PropertyResponse, tags=["Intelligence"])
def analyse_property(req: PropertyRequest):
    """
    Analyse a single property and return validated yield, risk score,
    investment conclusion, and optionally an AI insight from Claude.

    - Set `include_ai: true` to enable Claude analysis (requires
      ANTHROPIC_API_KEY environment variable on the server).
    """
    try:
        validator = YieldValidator(
            purchase_price=req.price,
            annual_rent=req.rent
        )
        scorer = RiskScorer(
            liquidity=req.liquidity,
            demand=req.demand,
            pricing=req.pricing
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    yield_value = validator.calculate_yield()
    yield_grade = validator.yield_grade()
    gap = validator.projection_gap(req.projected_yield)
    risk = scorer.risk_category()
    risk_score = scorer.calculate_score()
    conclusion = validator.investment_conclusion(risk)

    data = {
        "location": req.location,
        "type": req.asset_type,
        "price": int(req.price),
        "yield": yield_value,
        "yield_grade": yield_grade,
        "risk": risk,
        "projection_gap": gap,
        "conclusion": conclusion,
    }
    report = generate_report(data)

    ai_insight = None
    if req.include_ai:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise HTTPException(
                status_code=503,
                detail="AI analysis unavailable: ANTHROPIC_API_KEY not configured"
            )
        try:
            ai_insight = get_ai_insight(
                location=req.location,
                asset_type=req.asset_type,
                price=int(req.price),
                yield_value=yield_value,
                yield_grade=yield_grade,
                projection_gap=gap,
                risk=risk,
            )
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"AI analysis failed: {str(e)}"
            )

    return PropertyResponse(
        location=req.location,
        asset_type=req.asset_type,
        price=req.price,
        validated_yield=yield_value,
        yield_grade=yield_grade,
        projection_gap=gap,
        risk_score=risk_score,
        risk_category=risk,
        conclusion=conclusion,
        ai_insight=ai_insight,
        report=report,
    )
