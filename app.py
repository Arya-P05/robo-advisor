import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from portfolio_optimizer import fetch_stock_data, optimize_portfolio

st.title("Robo-Advisor Dashboard")

# User inputs
investment_amount = st.number_input("Investment Amount (CAD)", min_value=1000, value=750000)
tickers = st.text_input("Enter Stock Tickers (comma-separated)", "AAPL, MSFT, GOOGL").split(", ")

if st.button("Optimize Portfolio"):
    st.write("Fetching data and optimizing...")
    returns = fetch_stock_data(tickers)
    weights = optimize_portfolio(returns)
    
    # Display results
    st.subheader("Recommended Allocation")
    allocation = pd.DataFrame({
        "Stock": tickers,
        "Weight": weights,
        "Amount (CAD)": weights * investment_amount
    })
    st.dataframe(allocation)
    
    # Pie chart
    fig, ax = plt.subplots()
    ax.pie(weights, labels=tickers, autopct="%1.1f%%")
    st.pyplot(fig)