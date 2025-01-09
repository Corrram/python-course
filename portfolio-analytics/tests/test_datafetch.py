"""
test_datafetch.py

Tests for the DataFetcher class in datafetch.py, focusing on object-oriented fetching via yfinance.
"""

import pytest
import pandas as pd
from portfolio_analytics.datafetch import DataFetcher


def test_datafetch_single_ticker():
    """
    Test fetching data for a single ticker over a small date range.
    We don't assume data is definitely returned (date range might yield an empty DataFrame),
    but we do check that the object is a DataFrame with 'AAPL' column if not empty.
    """
    fetcher = DataFetcher(tickers=["AAPL"], start="2023-01-01", end="2023-01-05")
    df = fetcher.fetch_data()
    assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
    if not df.empty:
        assert (
            "AAPL" in df.columns
        ), "Returned DataFrame should contain the 'AAPL' column"


def test_datafetch_no_tickers():
    """
    If we pass an empty list of tickers, DataFetcher should raise ValueError.
    """
    fetcher = DataFetcher(tickers=[], start="2023-01-01", end="2023-01-10")
    with pytest.raises(ValueError):
        fetcher.fetch_data()


def test_datafetch_get_data_before_after_fetch():
    """
    Confirm that get_data() returns None before fetching, and a DataFrame afterwards.
    """
    fetcher = DataFetcher(tickers=["MSFT"], start="2023-01-01", end="2023-01-05")
    assert (
        fetcher.get_data() is None
    ), "get_data() should be None before fetch_data() is called"

    df_fetched = fetcher.fetch_data()
    df_stored = fetcher.get_data()
    assert isinstance(
        df_stored, pd.DataFrame
    ), "After fetch, get_data() should return a DataFrame"
    # They should refer to the same underlying data object or be equal in content
    assert df_stored.equals(
        df_fetched
    ), "get_data() should match the DataFrame returned by fetch_data()"


def test_datafetch_multiple_tickers():
    """
    Test fetching data for multiple tickers at once.
    """
    fetcher = DataFetcher(
        tickers=["AAPL", "MSFT"], start="2023-01-10", end="2023-01-15"
    )
    df = fetcher.fetch_data()
    assert isinstance(
        df, pd.DataFrame
    ), "Should return a pandas DataFrame for multiple tickers"
    if not df.empty:
        # Check columns
        for ticker in ["AAPL", "MSFT"]:
            assert ticker in df.columns, f"Returned DataFrame should contain '{ticker}'"
