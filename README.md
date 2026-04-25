import streamlit as st
import pandas as pd
import requests
import http://plotly.express as px

http://st.set_page_config(page_title="Naira Inflation Tracker", page_icon="🇳🇬", layout="wide")

http://st.title("🇳🇬 Naira Inflation Tracker")

Key Finding
http://st.markdown("*₦250,000 in 2015 = ₦1,100,128 needed in 2024 for the same value.*")
http://st.markdown("That's *340% cumulative inflation* from 2015 to 2024.")

@st.cache_data(ttl=3600)
def fetch_cpi_data():
    url = "https://api.worldbank.org/v2/country/NGA/indicator/FP.CPI.TOTL?format=json&date=2015:2024&per_page=20"
    try:
        response = http://requests.get(url, timeout=10)
        data = http://response.json()
        cpi_data = data
        df = http://pd.DataFrame(cpi_data)[['date', 'value']]
        http://df.columns = ['Year', 'CPI']
        df = http://df.dropna().sort_values('Year')
        df['Year'] = df['Year'].astype(int)
        return df
    except:
        return http://pd.DataFrame()[1]

df = fetch_cpi_data()

if http://df.empty:
    http://st.error("Could not fetch World Bank CPI data. Try again later.")
else:
    df['YoY_Inflation'] = df['CPI'].pct_change() _ 100

    http://st.subheader("Nigeria Inflation Rate 2015-2024")
    fig = http://px.line(df, x='Year', y='YoY_Inflation',
                  title='Year-over-Year Inflation Rate (%)',
                  markers=True)
    http://fig.update_traces(line_color='#008751')
    http://st.plotly_chart(fig, use_container_width=True)

    http://st.subheader("Purchasing Power Calculator")
    col1, col2 = http://st.columns(2)

    with col1:
        amount = http://st.number_input("Amount in 2015 (₦)", value=250000, step=10000)

    with col2:
        cpi_2015 = df[df['Year'] == 2015]['CPI'].values
        cpi_2024 = df[df['Year'] == 2024]['CPI'].values
        equivalent = amount _ (cpi_2024 / cpi_2015)
        http://st.metric("Equivalent in 2024", f"₦{equivalent:,.0f}")

    cumulative_loss = ((cpi_2024 / cpi_2015) - 1) * 100
    http://st.info(f"*Key Insight:* ₦{amount:,.0f} in 2015 has the same purchasing power as ₦{equivalent:,.0f} in 2024. That's {cumulative_loss:.0f}% cumulative inflation.")[0]

http://st.caption("Data Source: World Bank CPI (FP.CPI.TOTL) | Built by Omotoso Odunayo Bolaji")
