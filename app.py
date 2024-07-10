import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Page configuration
st.set_page_config(page_title="Simple Stock Price App", layout="wide")

# Custom CSS
st.markdown("""
<style>
.big-font {
    font-size:50px !important;
    font-weight: bold;
    color: #1E90FF;
}
.stSelectbox > div > div {
    background-color: #F0F8FF;
}
.stDateInput > div > div > input {
    background-color: #F0F8FF;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="big-font">Simple Stock Price App</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Settings")

# List of companies
companies = {
    'Google': 'GOOGL',
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'Facebook': 'META',
    'Tesla': 'TSLA',
    'NVIDIA': 'NVDA'
}

# Company selection
selected_company = st.sidebar.selectbox('Select a company', list(companies.keys()))
tickerSymbol = companies[selected_company]

# Date range selection
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input('Start date', value=date.today() - timedelta(days=365))
with col2:
    end_date = st.date_input('End date', value=date.today())

# Fetch data
@st.cache_data
def load_data(ticker, start, end):
    return yf.Ticker(ticker).history(start=start, end=end)

with st.spinner('Loading data...'):
    tickerDataframe = load_data(tickerSymbol, start_date, end_date)

# Main content
if not tickerDataframe.empty:
    # Stock price chart
    st.subheader(f'{selected_company} Stock Price')
    st.line_chart(tickerDataframe.Close, use_container_width=True)

    # Trading volume chart
    st.subheader(f'{selected_company} Trading Volume')
    st.bar_chart(tickerDataframe.Volume, use_container_width=True)

    # Key statistics
    st.subheader('Key Statistics')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Open", f"${tickerDataframe.Open[-1]:.2f}")
    col2.metric("Close", f"${tickerDataframe.Close[-1]:.2f}")
    col3.metric("High", f"${tickerDataframe.High[-1]:.2f}")
    col4.metric("Low", f"${tickerDataframe.Low[-1]:.2f}")

    # Data table
    st.subheader('Recent Data')
    st.dataframe(tickerDataframe.tail().style.highlight_max(axis=0))
else:
    st.error("No data available for the selected date range. Please try a different range.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ using Streamlit")
