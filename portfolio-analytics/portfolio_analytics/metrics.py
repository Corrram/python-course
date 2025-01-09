"""
metrics.py

Core financial metrics: returns, covariance, Sharpe ratio, etc.
"""

import pandas as pd
import numpy as np
from typing import Optional


def daily_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily returns from a price DataFrame.

    :param price_df: DataFrame of prices with columns as tickers, index as dates.
    :return: DataFrame of daily returns.
    """
    return price_df.pct_change(fill_method=None).dropna()


def mean_returns(returns_df: pd.DataFrame, annualize_factor: int = 252) -> pd.Series:
    """
    Compute mean (expected) returns, annualized, from daily returns.

    :param returns_df: DataFrame of daily returns.
    :param annualize_factor: Trading days per year, default 252.
    :return: Series of annualized expected returns per ticker.
    """
    return returns_df.mean() * annualize_factor


def cov_matrix(returns_df: pd.DataFrame, annualize_factor: int = 252) -> pd.DataFrame:
    """
    Compute the covariance matrix of returns, annualized.

    :param returns_df: DataFrame of daily returns.
    :param annualize_factor: Trading days per year, default 252.
    :return: Annualized covariance matrix.
    """
    return returns_df.cov() * annualize_factor


def portfolio_performance(
    weights: np.ndarray, mean_rets: pd.Series, cov: pd.DataFrame
) -> (float, float):
    """
    Given portfolio weights, expected returns, and covariance,
    compute the portfolio's annualized return and volatility.

    :param weights: 1D array of portfolio weights.
    :param mean_rets: Series of annualized returns for each asset.
    :param cov: DataFrame of annualized covariances.
    :return: (portfolio_return, portfolio_volatility)
    """
    port_ret = np.dot(weights, mean_rets.values)
    port_vol = np.sqrt(weights @ cov.values @ weights)
    return port_ret, port_vol


def sharpe_ratio(
    port_ret: float, port_vol: float, risk_free_rate: float = 0.02
) -> float:
    """
    Compute the Sharpe ratio for a given portfolio return and volatility.

    :param port_ret: Annualized portfolio return (e.g. 0.08 = 8%).
    :param port_vol: Annualized portfolio std dev (volatility).
    :param risk_free_rate: Risk-free rate, default 2%.
    :return: Sharpe ratio (return - rf) / volatility.
    """
    return (port_ret - risk_free_rate) / port_vol if port_vol > 1e-12 else 0.0
