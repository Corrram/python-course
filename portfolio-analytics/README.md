# Portfolio Analytics – Advanced Edition

A Python package offering:

- **Financial data fetching** (via `yfinance`)
- **Computation of daily/annualized returns, covariance matrices, Sharpe ratios**
- **Mean-variance optimization** (Markowitz) for minimum variance and maximum Sharpe portfolios
- **Decorators** for logging and timing function calls
- **Sphinx-compatible docstrings**

Designed for **Finance/Economics Master** students looking to explore real-world portfolio analytics in Python.

---

## Features

1. **DataFetch** (`datafetch.py`):
   - Fetch daily price data for multiple tickers using `yfinance`.
   - Returns a `pandas.DataFrame` of adjusted close prices.

2. **Metrics** (`metrics.py`):
   - Compute daily returns, annualized mean returns, covariance matrices.
   - Evaluate portfolio performance (return/volatility) and Sharpe ratios.

3. **Optimize** (`optimize.py`):
   - Implement **Markowitz** mean-variance optimization.
   - Find **minimum-variance** portfolio (no short-selling).
   - Find **maximum Sharpe ratio** portfolio under risk-free rate.

4. **Decorators** (`decorators.py`):
   - `@log_calls`: logs function calls and results.
   - `@timing`: measures execution time.

---

## Installation

1. **Clone** this repository or download it locally.
2. **Install Poetry** if not already:
   ```bash
   pip install poetry
