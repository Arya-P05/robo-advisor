import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from portfolio_optimizer import fetch_stock_data, optimize_portfolio
import numpy as np
from matplotlib.patches import FancyBboxPatch

st.title("Robo-Advisor Dashboard")

# User inputs
investment_text = st.text_input(
    "Investment Amount (CAD)", 
    value="", 
    placeholder="1000"
)

tickers_text = st.text_input(
    "Enter Stock Tickers (comma-separated)", 
    value="", 
    placeholder="e.g., AAPL, MSFT, GOOGL"
)
tickers = [ticker.strip() for ticker in tickers_text.split(",") if ticker.strip()]

if st.button("Optimize Portfolio"):
    if not investment_text:
        st.error("Please enter an investment amount.")
        st.stop()
    try:
        investment_amount = int(investment_text)
        if investment_amount < 100:
            st.error("Investment amount must be at least $100.")
            st.stop()
    except ValueError:
        st.error("Please enter a valid numeric investment amount.")
        st.stop()
    
    if not tickers:
        st.error("Please enter at least one ticker.")
        st.stop()

    with st.spinner("Fetching data and optimizing..."):
        returns = fetch_stock_data(tickers)
        weights = optimize_portfolio(returns)
    
    print("Optimization worked!")

    print(f"Tickers: {tickers}")
    print(f"Weights: {weights}")
    
    # Filter out tickers with 0% weight for the chart
    filtered_data = [(ticker, weight) for ticker, weight in zip(tickers, weights) if ((weight * 100).round(2)) > 0]
    if not filtered_data:
        st.error("No stocks with non-zero allocation to display on the chart.")
        st.stop()
    filtered_tickers, filtered_weights = zip(*filtered_data)

    print(f"Filtered Tickers: {filtered_tickers}")

    # Prepare the allocation DataFrame.
    allocation = pd.DataFrame({
        "Stock": tickers,
        "Weight (%)": (weights * 100).round(2),
        "Amount (CAD)": (weights * investment_amount).round(2)
    })
    allocation = allocation.sort_values("Weight (%)", ascending=False)
    
    st.markdown("## Recommended Allocation")
    st.dataframe(
        allocation.style.format({
            "Amount (CAD)": "{:,.2f}",
            "Weight (%)": "{:.2f}"
        }),
        use_container_width=True
    )
    
    # Create the figure and axis.
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Make the original axes background transparent.
    ax.patch.set_alpha(0)
    
    # Add a FancyBboxPatch to simulate a white rounded-corner background.
    fancy_box = FancyBboxPatch(
        (0, 0), 1, 1,
        transform=ax.transAxes,
        boxstyle="round,pad=0.1,rounding_size=15",
        fc="white",
        ec="none",
        zorder=-1
    )
    ax.add_patch(fancy_box)
    
    # Set the figure's overall background to white.
    fig.patch.set_facecolor("white")
    
    # Use a minimal color palette.
    colors = plt.get_cmap("tab10").colors
    
    # Plot the donut (pie) chart without autopct so that custom labels can be added.
    wedges, _ = ax.pie(
        filtered_weights,
        startangle=90,
        colors=colors[:len(filtered_tickers)],
        wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'}
    )
    
    # Add custom ticker labels outside the donut chart.
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 + wedge.theta1) / 2.0
        x = 1.15 * np.cos(np.deg2rad(angle))
        y = 1.15 * np.sin(np.deg2rad(angle))
        label = f"{filtered_tickers[i]}\n{filtered_weights[i]*100:.1f}%"
        ax.text(x, y, label, ha="center", va="center", fontsize=12, color="black")
    
    # Add a white circle at the center to create the donut effect.
    centre_circle = plt.Circle((0, 0), 0.70, fc='white', linewidth=0)
    ax.add_artist(centre_circle)
    
    # Ensure the pie chart is drawn as a circle.
    ax.axis('equal')
    
    # Removed the title as requested.
    
    fig.tight_layout()
    st.pyplot(fig)

