import yfinance as yf
import numpy as np
from scipy.optimize import minimize

def fetch_stock_data(tickers, start_date="2015-01-01", end_date="2023-01-01"):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    returns = data.pct_change().dropna()
    return returns

def optimize_portfolio(returns):
    n_assets = len(returns.columns)
    initial_weights = np.array([1/n_assets] * n_assets)
    bounds = [(0, 1) for _ in range(n_assets)]
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    
    def negative_sharpe(weights):
        portfolio_return = np.sum(returns.mean() * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        return -portfolio_return / portfolio_volatility
    
    result = minimize(negative_sharpe, initial_weights, bounds=bounds, constraints=constraints)
    return result.x