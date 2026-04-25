import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import io

st.set_page_config(page_title="Naira Inflation Tracker", page_icon="🇳🇬", layout="wide")

st.title("🇳🇬 Naira Inflation Tracker")
st.markdown("Track how much purchasing power the Naira lost since 2015 using World Bank CPI data.")

st.markdown("### Key Finding")
st.markdown("**₦250,000 in 2015 = ₦1,100,128 needed in 2024 for the same value.**")
st.markdown("That's **340% cumulative inflation** from 2015 to 2024.")

@st.cache_data(ttl=3600)
def fetch_cpi_data():
    url = "https://api.worldbank.org/v2/country/NGA/indicator/FP.CPI.TOTL?format=json&date=2015:2024&per_page=100"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()[1]
        df = pd.DataFrame(data)[['date', 'value']]
        df.columns = ['Year', 'CPI']
        df = df.dropna()
        df['Year'] = df['Year'].astype(int)
        df = df[(df['Year'] >= 2015) & (df['Year'] <= 2024)]
        df = df.sort_values('Year')
        return df
    except Exception as e:
        st.error(f"Could not fetch World Bank CPI data: {e}")
        return pd.DataFrame()

df = fetch_cpi_data()

if df.empty:
    st.stop()
else:
    df['YoY_Inflation'] = df['CPI'].pct_change() * 100

    st.subheader("Nigeria Inflation Rate 2015-2024")
    fig = px.line(df, x='Year', y='YoY_Inflation',
                  title='Year-over-Year Inflation Rate (%)',
                  markers=True)
    fig.update_traces(line_color='#008751')
    fig.update_layout(yaxis_title="Inflation Rate (%)", xaxis_title="Year")
    st.plotly_chart(fig, use_container_width=True)

    # Download chart as PNG - with error handling
    try:
        img_bytes = fig.to_image(format="png", width=1200, height=600, scale=2)
        st.download_button(
            label="📸 Download Chart as PNG",
            data=img_bytes,
            file_name="naira_inflation_2015_2024.png",
            mime="image/png"
        )
    except Exception:
        st.caption("Tip: Right-click the chart → 'Save image as...' to download manually")

    st.subheader("Purchasing Power Calculator")
    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount (₦)", value=250000, step=10000, min_value=1)
        start_year = st.selectbox("From Year", options=df['Year'].tolist(), index=0)
        end_year = st.selectbox("To Year", options=df['Year'].tolist(), index=len(df)-1)

    with col2:
        if start_year >= end_year:
            st.warning("Start year must be before end year")
        else:
            cpi_start = df[df['Year'] == start_year]['CPI'].values
            cpi_end = df[df['Year'] == end_year]['CPI'].values

            if len(cpi_start) > 0 and len(cpi_end) > 0:
                cpi_start_val = cpi_start[0]
                cpi_end_val = cpi_end[0]
                equivalent = amount * (cpi_end_val / cpi_start_val)
                st.metric(f"Equivalent in {end_year}", f"₦{equivalent:,.0f}")

                cumulative_loss = ((cpi_end_val / cpi_start_val) - 1) * 100
                st.info(f"**Key Insight:** ₦{amount:,.0f} in {start_year} has the same purchasing power as ₦{equivalent:,.0f} in {end_year}. That's {cumulative_loss:.0f}% cumulative inflation.")

                loss = equivalent - amount
                st.error(f"Purchasing power lost: ₦{loss:,.0f}")
            else:
                st.warning(f"CPI data missing for {start_year} or {end_year}.")

    with st.expander("View Raw Data"):
        st.dataframe(df[['Year', 'CPI', 'YoY_Inflation']].round(2), use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="nigeria_cpi_2015_2024.csv",
            mime="text/csv"
        )

st.caption("Data Source: World Bank CPI (FP.CPI.TOTL) | Built by Omotoso Odunayo Bolaji")
