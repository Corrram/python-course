"""
test_metrics.py

Tests for the metrics module.
"""

import pandas as pd
import numpy as np
from portfolio_analytics.metrics import (
    daily_returns,
    mean_returns,
    cov_matrix,
    portfolio_performance,
    sharpe_ratio,
)


def test_daily_returns():
    data = pd.DataFrame({"A": [100, 101, 102], "B": [50, 50.5, 51]})
    rets = daily_returns(data)
    assert rets.shape == (2, 2)
    assert abs(rets.loc[1, "A"] - 0.01) < 1e-9


def test_mean_returns():
    rets = pd.DataFrame({"A": [0.01, 0.02, 0.015], "B": [-0.005, 0.0, 0.002]})
    means = mean_returns(rets, annualize_factor=3)  # short data to simulate
    # average for A: (0.01 + 0.02 + 0.015) / 3 = 0.015
    # multiplied by 3 => 0.045
    assert abs(means["A"] - 0.045) < 1e-9


def test_cov_matrix():
    rets = pd.DataFrame({"A": [0.01, 0.02, 0.015], "B": [-0.005, 0.0, 0.002]})
    cv = cov_matrix(rets, annualize_factor=3)
    assert cv.shape == (2, 2)


def test_portfolio_performance():
    mean_ret = pd.Series({"A": 0.1, "B": 0.05})
    cov = pd.DataFrame({"A": [0.04, 0.00], "B": [0.00, 0.02]}, index=["A", "B"])
    weights = np.array([0.6, 0.4])
    port_ret, port_vol = portfolio_performance(weights, mean_ret, cov)
    return_difference = abs(port_ret - 0.08)
    assert return_difference < 1e-9  # 0.6*0.1 + 0.4*0.05
    volatility_difference = abs(port_vol - 0.06)
    assert volatility_difference < 1e-9  # sqrt(0.6^2 * 0.04 + 0.4^2 * 0.02)


def test_sharpe_ratio():
    sr = sharpe_ratio(port_ret=0.1, port_vol=0.05, risk_free_rate=0.02)
    assert abs(sr - 1.6) < 1e-9
