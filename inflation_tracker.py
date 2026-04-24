import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

st.set_page_config(
    page_title="Naira Inflation Tracker",
    page_icon="🇳🇬",
    layout="wide"
)

@st.cache_data(ttl=86400)
def get_inflation_data():
    """Fetch Nigeria CPI data from World Bank API 2015-2024"""
    url = "https://api.worldbank.org/v2/country/NG/indicator/FP.CPI.TOTL?date=2015:2024&format=json&per_page=20"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if len(data) < 2:
            return None

        records = data[1]
        df = pd.DataFrame([
            {"Year": int(item["date"]), "Inflation Rate": item["value"]}
            for item in records if item["value"] is not None
        ])
        return df.sort_values("Year")
    except:
        return None

def calculate_purchasing_power(amount, start_year, end_year, df):
    """Calculate equivalent purchasing power using cumulative inflation"""
    df_range = df[(df["Year"] >= start_year) & (df["Year"] <= end_year-1)]
    if df_range.empty:
        return amount

    cumulative_multiplier = 1.0
    for rate in df_range["Inflation Rate"]:
        cumulative_multiplier *= (1 + rate/100)
    return round(amount * cumulative_multiplier, 2)

# --- UI ---
st.title("🇳🇬 Naira Inflation Tracker")
st.markdown("Track Nigeria's inflation and see how much purchasing power the Naira has lost since 2015")

df = get_inflation_data()

if df is None:
    st.error("Failed to load World Bank data. Please refresh.")
    st.stop()

# Key Metrics
current_rate = df.iloc[-1]["Inflation Rate"]
avg_5yr = df.tail(5)["Inflation Rate"].mean()
peak_year = df.loc[df["Inflation Rate"].idxmax()]

col1, col2, col3 = st.columns(3)
col1.metric("Current Inflation Rate", f"{current_rate:.1f}%", f"{df.iloc[-1]['Year']}")
col2.metric("5-Year Average", f"{avg_5yr:.1f}%")
col3.metric("Peak Year", f"{peak_year['Inflation Rate']:.1f}%", f"{int(peak_year['Year'])}")

# Chart
st.subheader("📈 Inflation Trend 2015-2024")
fig = px.line(
    df, x="Year", y="Inflation Rate",
    markers=True,
    labels={"Inflation Rate": "Inflation Rate (%)"},
    template="plotly_white"
)
fig.update_traces(line_color="#008751", line_width=3)
fig.update_layout(height=400, hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Calculator
st.subheader("💰 Purchasing Power Calculator")
st.markdown("See what your money from a past year is worth today")

col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Amount (₦)", min_value=100, value=10000, step=1000)
    start_year = st.selectbox("From Year", options=df["Year"].tolist()[:-1], index=5)
with col2:
    end_year = df["Year"].max()
    st.metric("To Year", end_year)

    if st.button("Calculate", type="primary"):
        result = calculate_purchasing_power(amount, start_year, end_year, df)
        loss = result - amount
        pct_loss = (loss / amount) * 100

        st.success(f"**₦{amount:,.0f} in {start_year} = ₦{result:,.0f} in {end_year}**")
        st.warning(f"Purchasing power lost: ₦{loss:,.0f} ({pct_loss:.1f}%)")

st.caption("Data: World Bank | Built with Streamlit | @miltonmason18-ops")
