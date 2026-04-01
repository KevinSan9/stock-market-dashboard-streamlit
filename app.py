import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("Stock Market Dashboard")
st.write("Interactive dashboard to explore stock prices and trading volume.")

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Controls")

ticker = st.sidebar.selectbox(
    "Select a stock",
    ["AAPL", "TSLA", "MSFT", "AMZN"]
)

start_date = st.sidebar.date_input(
    "Start date",
    pd.to_datetime("2020-01-01")
)

end_date = st.sidebar.date_input(
    "End date",
    pd.to_datetime("2024-01-01")
)

# -----------------------------
# Validate dates
# -----------------------------
if start_date >= end_date:
    st.error("Start date must be earlier than end date.")
    st.stop()

# -----------------------------
# Download data
# -----------------------------
data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    st.error("No data loaded. Try another ticker or date range.")
    st.stop()

# -----------------------------
# Fix MultiIndex columns if needed
# -----------------------------
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# -----------------------------
# Prepare data
# -----------------------------
data = data.reset_index()
data["MA50"] = data["Close"].rolling(window=50).mean()

# -----------------------------
# Price chart
# -----------------------------
st.subheader(f"{ticker} Closing Price")

fig_price = px.line(
    data,
    x="Date",
    y=["Close", "MA50"],
    title=f"{ticker} Price with MA50"
)

fig_price.update_layout(
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    legend_title="Series"
)

st.plotly_chart(fig_price, width="stretch")

# -----------------------------
# Volume chart
# -----------------------------
st.subheader(f"{ticker} Trading Volume")

fig_volume = px.bar(
    data,
    x="Date",
    y="Volume",
    title=f"{ticker} Volume"
)

fig_volume.update_layout(
    xaxis_title="Date",
    yaxis_title="Volume"
)

st.plotly_chart(fig_volume, width="stretch")

# -----------------------------
# Metrics
# -----------------------------
latest_close = data["Close"].iloc[-1]
highest_close = data["Close"].max()
lowest_close = data["Close"].min()

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Latest Close", f"${latest_close:.2f}")
col2.metric("Highest Close", f"${highest_close:.2f}")
col3.metric("Lowest Close", f"${lowest_close:.2f}")