import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Naira Inflation Tracker",
    page_icon="📈",
    layout="wide"
)

st.title("Naira Inflation Tracker 🇳🇬")
st.write("Live Consumer Price Index data from World Bank API")

# --- Fetch Data ---
@st.cache_data
def load_data():
    url = "https://api.worldbank.org/v2/country/NG/indicator/FP.CPI.TOTL.ZG?format=json&per_page=100"
    response = requests.get(url)
    data = response.json()[1]

    df = pd.DataFrame(data)
    df = df[['date', 'value']]
    df.columns = ['Year', 'Inflation Rate (%)']
    df = df.dropna()
    df['Year'] = df['Year'].astype(int)
    df = df.sort_values('Year')
    return df

try:
    df = load_data()

    # --- Metrics ---
    latest_year = df['Year'].iloc[-1]
    latest_rate = df['Inflation Rate (%)'].iloc[-1]
    prev_rate = df['Inflation Rate (%)'].iloc[-2]
    change = latest_rate - prev_rate

    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Year", f"{latest_year}")
    col2.metric("Inflation Rate", f"{latest_rate:.2f}%")
    col3.metric("YoY Change", f"{change:+.2f}%", delta=f"{change:.2f}%")

    # --- Chart ---
    st.subheader("Annual Inflation Trend")
    st.line_chart(df.set_index('Year'))

    # --- Data Table ---
    with st.expander("View Raw Data"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Could not load data. World Bank API might be down.")
    st.code(f"Error: {e}")

# --- AUTHOR CREDIT ---
st.markdown("---")
st.caption("Built by Omotoso Odunayo Bolaji")
