# 🇳🇬 Naira Inflation Tracker

**Live App:** https://inflation-tracker-h6mazamoczdycohjd8dojd.streamlit.app

Track how much purchasing power the Naira lost since 2015 using World Bank CPI data.

### Key Finding
₦250,000 in 2015 = ₦1,100,128 needed in 2024 for the same value.
That's 340% cumulative inflation from 2015 to 2024.

### Tech Stack
- **Python** - Data processing
- **Streamlit** - Web app framework 
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts
- **World Bank API** - CPI data source (FP.CPI.TOTL)

### Features
- Real-time CPI data from World Bank
- Converts CPI index to Year-over-Year inflation rates
- Calculates cumulative purchasing power loss 2015-2024
- Interactive chart of inflation trend
- Amount calculator: "₦X in 2015 = ₦Y today"

### Run Locally
```bash
git clone https://github.com/odunayo/inflation-tracker
cd inflation-tracker
pip install -r requirements.txt
streamlit run inflation_tracker.py
