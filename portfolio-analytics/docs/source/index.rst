.. portfolio-analytics documentation master file, created by
   sphinx-quickstart on Wed Jan 22 14:57:44 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

portfolio-analytics documentation
=================================

Introduction
------------

Welcome to the **portfolio-analytics** package! This library provides a set of tools
to help you fetch financial data, calculate key metrics (returns, covariance matrix, etc.),
and optimize portfolios under various strategies (e.g., minimum variance, maximum Sharpe
ratio). Below is a quick walkthrough demonstrating how to use some of the core functions.

Quick Start Example
-------------------

.. code-block:: python

   from portfolio_analytics.metrics import daily_returns, mean_returns, cov_matrix
   from portfolio_analytics.optimize import min_variance, max_sharpe
   from portfolio_analytics.datafetch import DataFetcher

   # 0) Select some tickers
   tickers = ["AAPL", "MSFT", "BTC-USD"]

   # 1) Fetch daily stock prices
   fetcher = DataFetcher(tickers=tickers, start="2023-01-01")
   prices = fetcher.fetch_data()
   print(prices.head())
   df_again = fetcher.get_data()  # same DataFrame as prices

   # 2) Calculate daily returns
   rets = daily_returns(prices)

   # 3) Compute annualized mean returns and covariance matrix
   m = mean_returns(rets)  # e.g. ~10% Apple, ~8% MSFT (example)
   cv = cov_matrix(rets)

   # 4) Find the min-variance portfolio
   weights_mv = min_variance(m, cv)
   print("Minimum Variance Weights:", weights_mv)

   # 5) Find the max Sharpe ratio portfolio (assuming 2% risk-free rate)
   weights_ms = max_sharpe(m, cv, risk_free_rate=0.02)
   print("Max Sharpe Weights:", weights_ms)

In just a few lines of code, you can pull daily price data, compute relevant metrics,
and determine portfolio weights that minimize variance or maximize your risk-adjusted
returns. For more detailed usage and advanced features, refer to the sections below.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
