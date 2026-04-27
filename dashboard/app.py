import sys
import os
import pandas as pd
import streamlit as st

# Ensure repo root is on the path regardless of where streamlit is invoked
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.yield_validator import YieldValidator
from core.risk_scoring import RiskScorer
from models.report_generator import generate_report

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OREIL — Titan Crest Intelligence Dashboard",
    page_icon="🏙️",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏙️ OREIL Intelligence Dashboard")
st.caption("Real Estate Decision Intelligence · Powered by Titan Crest")
st.divider()

# ── Sidebar: Property Inputs ──────────────────────────────────────────────────
with st.sidebar:
    st.header("Property Parameters")
    location = st.text_input("Location", "Business Bay")
    asset_type = st.selectbox(
        "Asset Type",
        ["Studio", "1BR Apartment", "2BR Apartment", "3BR Apartment",
         "Penthouse", "Villa", "Townhouse", "Commercial"]
    )
    price = st.number_input(
        "Purchase Price (AED)", min_value=100_000,
        max_value=100_000_000, value=1_500_000, step=50_000,
        format="%d"
    )
    rent = st.number_input(
        "Annual Rent (AED)", min_value=0,
        max_value=10_000_000, value=105_000, step=5_000,
        format="%d"
    )
    projected_yield = st.slider(
        "Projected Yield Benchmark (%)", 3.0, 15.0, 9.5, 0.5
    )

    st.divider()
    st.header("Risk Factors")
    st.caption("Rate each factor 1 (worst) → 5 (best)")
    liquidity = st.slider("Liquidity", 1, 5, 4,
                          help="How easily can this asset be sold?")
    demand = st.slider("Market Demand", 1, 5, 4,
                       help="Rental and buyer demand in this sub-market")
    pricing = st.slider("Pricing Attractiveness", 1, 5, 3,
                        help="Is the asset priced attractively vs comparables?")

# ── Calculations ──────────────────────────────────────────────────────────────
try:
    validator = YieldValidator(price, rent)
    scorer = RiskScorer(liquidity, demand, pricing)

    yield_val = validator.calculate_yield()
    yield_grade = validator.yield_grade()
    gap = validator.projection_gap(projected_yield)
    risk = scorer.risk_category()
    risk_score = scorer.calculate_score()
    conclusion = validator.investment_conclusion(risk)

    # ── Metrics Row ───────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Validated Yield",
        f"{yield_val}%",
        f"{gap:+.2f}% vs {projected_yield}% benchmark",
        delta_color="normal"
    )
    col2.metric("Yield Grade", yield_grade)
    col3.metric(
        "Risk Score",
        f"{risk_score:.2f} / 4.0",
        help="0 = no risk, 4 = maximum risk"
    )
    col4.metric("Risk Category", risk)

    st.divider()

    # ── Conclusion ────────────────────────────────────────────────────────────
    conclusion_colour = {
        "High-yield": "success",
        "Income-stable": "info",
        "Below-average": "warning",
        "Yield insufficient": "error",
    }
    colour = "info"
    for key, val in conclusion_colour.items():
        if key.lower() in conclusion.lower():
            colour = val
            break

    if colour == "success":
        st.success(f"✅ {conclusion}")
    elif colour == "warning":
        st.warning(f"⚠️ {conclusion}")
    elif colour == "error":
        st.error(f"❌ {conclusion}")
    else:
        st.info(f"ℹ️ {conclusion}")

    # ── Full Report ───────────────────────────────────────────────────────────
    st.subheader("Structured Report")
    data = {
        "location": location, "type": asset_type, "price": price,
        "yield": yield_val, "yield_grade": yield_grade,
        "risk": risk, "projection_gap": gap, "conclusion": conclusion,
    }
    st.code(generate_report(data), language=None)

except ValueError as e:
    st.error(f"Input error: {e}")

# ── Portfolio View ────────────────────────────────────────────────────────────
st.divider()
st.subheader("Portfolio View — Dubai Sample Dataset")

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "sample_dubai_transactions.csv"
)

try:
    df = pd.read_csv(DATA_FILE)
    df["yield_%"] = (df["rent"] / df["price"] * 100).round(2)
    df["yield_grade"] = df.apply(
        lambda r: YieldValidator(r["price"], r["rent"]).yield_grade(), axis=1
    )
    df["risk_category"] = df.apply(
        lambda r: RiskScorer(
            int(r["liquidity"]), int(r["demand"]), int(r["pricing"])
        ).risk_category(), axis=1
    )
    df["conclusion"] = df.apply(
        lambda r: YieldValidator(r["price"], r["rent"]).investment_conclusion(
            RiskScorer(int(r["liquidity"]), int(r["demand"]), int(r["pricing"])).risk_category()
        ), axis=1
    )

    display_cols = ["location", "type", "price", "rent",
                    "yield_%", "yield_grade", "risk_category", "conclusion"]
    st.dataframe(
        df[display_cols].rename(columns={
            "location": "Location", "type": "Type",
            "price": "Price (AED)", "rent": "Annual Rent (AED)",
            "yield_%": "Yield %", "yield_grade": "Grade",
            "risk_category": "Risk", "conclusion": "Conclusion"
        }),
        use_container_width=True
    )
except FileNotFoundError:
    st.warning("No dataset found at data/sample_dubai_transactions.csv")
