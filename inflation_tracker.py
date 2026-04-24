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

def calculate_purchasing_power(amount
