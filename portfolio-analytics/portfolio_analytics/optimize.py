"""
optimize.py

Functions to optimize a portfolio using mean-variance (Markowitz) approaches.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Callable
from scipy.optimize import minimize
from .metrics import portfolio_performance, sharpe_ratio


def min_variance(mean_rets: pd.Series, cov: pd.DataFrame) -> np.ndarray:
    """
    Find the portfolio weights that achieve the minimum variance (no short-selling constraint).

    :param mean_rets: Series of expected returns for each asset.
    :param cov: Covariance matrix for the assets.
    :return: Optimal weights as a 1D numpy array.
    """
    n_assets = len(mean_rets)
    init_guess = np.repeat(1 / n_assets, n_assets)

    # Constraint: weights sum to 1
    constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    # Bounds: each weight >= 0
    bounds = [(0.0, 1.0) for _ in range(n_assets)]

    def portfolio_var(w: np.ndarray) -> float:
        # Only variance part
        _, port_vol = portfolio_performance(w, mean_rets, cov)
        return port_vol**2

    result = minimize(
        portfolio_var,
        init_guess,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    return result.x if result.success else init_guess


def max_sharpe(
    mean_rets: pd.Series, cov: pd.DataFrame, risk_free_rate: float = 0.02
) -> np.ndarray:
    """
    Find portfolio weights that maximize Sharpe ratio.

    :param mean_rets: Series of expected returns.
    :param cov: Covariance matrix.
    :param risk_free_rate: Risk-free rate.
    :return: Optimal weights.
    """
    n_assets = len(mean_rets)
    init_guess = np.repeat(1 / n_assets, n_assets)
    constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    bounds = [(0.0, 1.0) for _ in range(n_assets)]

    def neg_sharpe(w: np.ndarray) -> float:
        port_ret, port_vol = portfolio_performance(w, mean_rets, cov)
        return -sharpe_ratio(port_ret, port_vol, risk_free_rate)

    result = minimize(
        neg_sharpe, init_guess, method="SLSQP", bounds=bounds, constraints=constraints
    )
    return result.x if result.success else init_guess
