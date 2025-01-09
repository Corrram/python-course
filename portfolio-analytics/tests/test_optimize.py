"""
test_optimize.py

Tests for the optimize module, focusing on min_variance and max_sharpe.
"""

import pytest
import numpy as np
import pandas as pd
from portfolio_analytics.optimize import min_variance, max_sharpe
from portfolio_analytics.metrics import portfolio_performance


def test_min_variance():
    mean_ret = pd.Series({"A": 0.1, "B": 0.05})
    cov = pd.DataFrame({"A": [0.04, 0.00], "B": [0.00, 0.02]}, index=["A", "B"])

    weights = min_variance(mean_ret, cov)
    assert abs(weights.sum() - 1.0) < 1e-7
    # Because B has lower variance, we expect more weight on B
    assert weights[1] > weights[0]


def test_max_sharpe():
    mean_ret = pd.Series({"A": 0.1, "B": 0.05})
    cov = pd.DataFrame({"A": [0.04, 0.00], "B": [0.00, 0.02]}, index=["A", "B"])

    weights = max_sharpe(mean_ret, cov, risk_free_rate=0.02)
    assert abs(weights.sum() - 1.0) < 1e-7
    # A has higher return, so we expect more weight on A
    assert weights[0] > weights[1]


def test_max_sharpe_zero_vol():
    # If an asset has zero variance, it might dominate
    mean_ret = pd.Series({"A": 0.08, "B": 0.06})
    cov = pd.DataFrame({"A": [0.0, 0.0], "B": [0.0, 0.0]}, index=["A", "B"])
    weights = max_sharpe(mean_ret, cov, risk_free_rate=0.02)
    # The solution might put everything in the zero-vol asset with best ratio
    assert abs(weights.sum() - 1.0) < 1e-7
