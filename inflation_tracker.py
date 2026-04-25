import streamlit as st
import pandas as pd
import requests
import plotly.express as px

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
        data = response.json()[1] # [1] = actual data, [0] = metadata
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

    st.subheader("Purchasing Power Calculator")
    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount in 2015 (₦)", value=250000, step=10000, min_value=1)

    with col2:
        cpi_2015 = df[df['Year'] == 2015]['CPI'].values
        cpi_2024 = df[df['Year'] == 2024]['CPI'].values

        if len(cpi_2015) > 0 and len(cpi_2024) > 0:
            equivalent = amount * (cpi_2024 / cpi_2015)
            st.metric("Equivalent in 2024", f"₦{equivalent:,.0f}")

            cumulative_loss = ((cpi_2024 / cpi_2015) - 1) * 100
            st.info(f"**Key Insight:** ₦{amount:,.0f} in 2015 has the same purchasing power as ₦{equivalent:,.0f} in 2024. That's {cumulative_loss:.0f}% cumulative inflation.")
        else:
            st.warning("2015 or 2024 CPI data missing from World Bank API.")

    with st.expander("View Raw Data"):
        st.dataframe(df[['Year', 'CPI', 'YoY_Inflation']].round(2), use_container_width=True)

st.caption("Data Source: World Bank CPI (FP.CPI.TOTL) | Built by Omotoso Odunayo Bolaji")
