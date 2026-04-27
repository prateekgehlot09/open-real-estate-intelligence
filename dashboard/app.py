import streamlit as st
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.yield_validator import YieldValidator
from core.risk_scoring import RiskScorer
from models.report_generator import generate_report

st.set_page_config(page_title="OREIL Intelligence Dashboard", layout="wide")
st.title("OREIL — Real Estate Intelligence Dashboard")
st.caption("Powered by Titan Crest | Built on the OREIL framework")

# Sidebar — inputs
st.sidebar.header("Property Parameters")
location = st.sidebar.text_input("Location", "Business Bay")
asset_type = st.sidebar.selectbox("Type", ["Studio", "1BR Apartment", "2BR Apartment", "Villa", "Penthouse"])
price = st.sidebar.number_input("Purchase Price (AED)", min_value=100000, value=1500000, step=50000)
rent = st.sidebar.number_input("Annual Rent (AED)", min_value=0, value=105000, step=5000)
projected_yield = st.sidebar.slider("Projected Yield Benchmark (%)", 4.0, 15.0, 9.5, 0.5)

st.sidebar.header("Risk Factors (1=Worst, 5=Best)")
liquidity = st.sidebar.slider("Liquidity", 1, 5, 4)
demand = st.sidebar.slider("Demand", 1, 5, 4)
pricing = st.sidebar.slider("Pricing Attractiveness", 1, 5, 3)

# Calculations
validator = YieldValidator(price, rent)
scorer = RiskScorer(liquidity, demand, pricing)

yield_val = validator.calculate_yield()
yield_grade = validator.yield_grade()
gap = validator.projection_gap(projected_yield)
risk = scorer.risk_category()
score = scorer.calculate_score()
conclusion = validator.investment_conclusion(risk)

# Dashboard — metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Validated Yield", f"{yield_val}%", f"{gap:+.2f}% vs benchmark")
col2.metric("Yield Grade", yield_grade)
col3.metric("Risk Score", f"{score}/4.0")
col4.metric("Risk Category", risk)

st.divider()
st.subheader("Investment Conclusion")
st.info(conclusion)

st.subheader("Full Report")
data = {
    "location": location, "type": asset_type, "price": price,
    "yield": yield_val, "yield_grade": yield_grade,
    "risk": risk, "projection_gap": gap, "conclusion": conclusion,
}
st.code(generate_report(data))

# Portfolio comparison from CSV
st.divider()
st.subheader("Portfolio View")
try:
    df = pd.read_csv("data/sample_dubai_transactions.csv")
    df["yield_%"] = (df["rent"] / df["price"] * 100).round(2)
    st.dataframe(df[["location", "type", "price", "rent", "yield_%"]], use_container_width=True)
except FileNotFoundError:
    st.warning("No dataset loaded.")
