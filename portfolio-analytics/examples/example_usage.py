from portfolio_analytics.metrics import daily_returns, mean_returns, cov_matrix
from portfolio_analytics.optimize import min_variance, max_sharpe
from portfolio_analytics.datafetch import DataFetcher

# 0) Select some tickers
tickers = ["AAPL", "MSFT", "BTC-USD"]

# 1) Fetch daily stock prices
fetcher = DataFetcher(tickers=tickers, start="2023-01-01")
prices = fetcher.fetch_data()
print(prices.head())
df_again = fetcher.get_data()  # same DataFrame as df_prices


# 2) Calculate daily returns
rets = daily_returns(prices)

# 3) Compute annualized mean returns and covariance matrix
m = mean_returns(rets)  # e.g. ~10% Apple, ~8% MSFT (example)
cv = cov_matrix(rets)

# 4) Find min-variance portfolio
weights_mv = min_variance(m, cv)
print("Minimum Variance Weights:", weights_mv)

# 5) Find max Sharpe ratio portfolio (assuming 2% risk-free rate)
weights_ms = max_sharpe(m, cv, risk_free_rate=0.02)
print("Max Sharpe Weights:", weights_ms)
