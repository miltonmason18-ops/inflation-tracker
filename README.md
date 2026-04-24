# 🇳🇬 Naira Inflation Tracker

**Live App:** https://inflation-tracker-7hhhzfpxz9fg5qbq3xdxx8.streamlit.app

Track how much purchasing power the Naira lost since 2015 using World Bank CPI data.

### Key Finding
₦250,000 in 2015 = ₦1,100,128 needed in 2024 for the same value.
That's 340% cumulative inflation from 2015 to 2024.

### Demo
![App Screenshot](screenshot.png)

### Tech Stack
- **Python** - Data processing
- **Streamlit** - Web app framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts
- **World Bank API** - CPI data source (FP.CPI.TOTL)

### Features
- Real-time CPI data from World Bank
- Converts CPI index to Year-over-Year inflation rates
- Calculates cumulative purchasing power loss
- Interactive chart of inflation trend 2015-2024
- Amount calculator: "₦X in 2015 = ₦Y today"

### What I Learned
- REST API integration with error handling + caching
- CPI index → YoY inflation rate conversion
- Data validation and debugging compound calculation errors
- Deploying production apps to Streamlit Cloud

### Run Locally
```bash
pip install streamlit pandas plotly requests
streamlit run inflation_tracker.py
