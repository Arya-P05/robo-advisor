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
    
    # Create a DataFrame with updated formatting for better visuals.
    allocation = pd.DataFrame({
        "Stock": tickers,
        "Weight (%)": (weights * 100).round(2),
        "Amount (CAD)": (weights * investment_amount).round(2)
    })
    
    st.markdown("## Recommended Allocation")
    
    # Split the results into two columns: one for the table and one for the chart.
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(allocation.style.format({"Amount (CAD)": "{:,.2f}"}))
    
    with col2:
        # Create a donut chart (pie chart with a central white circle).
        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            weights,
            labels=tickers,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )
        # Draw a circle at the center for the donut effect.
        centre_circle = plt.Circle((0, 0), 0.70, fc="white")
        ax.add_artist(centre_circle)
        ax.axis('equal')  # Ensure the pie is drawn as a circle.
        plt.title("Portfolio Allocation")
        st.pyplot(fig)
