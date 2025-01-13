"""
datafetch.py

Object-oriented approach to fetching historical price data using yfinance.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import List, Optional


class DataFetcher:
    """
    A class to download daily adjusted close prices for a set of tickers
    between specified start/end dates using yfinance.

    :param tickers: A list of ticker symbols (e.g. ["AAPL", "MSFT"]).
    :type tickers: List[str]
    :param start: Start date (YYYY-MM-DD) for fetching data.
    :type start: str
    :param end: End date (YYYY-MM-DD) for fetching data. If None, defaults to today's date.
    :type end: Optional[str]
    """

    def __init__(
        self, tickers: List[str], start: str, end: Optional[str] = None
    ) -> None:
        self.tickers = tickers
        self.start = start
        # If no end date is provided, default to today's date
        self.end = end if end else datetime.today().strftime("%Y-%m-%d")

        # This attribute will hold the fetched DataFrame after fetch_data() is called
        self.data: Optional[pd.DataFrame] = None

    def fetch_data(self) -> pd.DataFrame:
        """
        Download daily adjusted close prices for the provided tickers.

        :return: A pandas DataFrame with columns = ticker symbols, index = date.
        :rtype: pd.DataFrame
        :raises ValueError: If no tickers are specified.
        """
        if not self.tickers:
            raise ValueError("No tickers specified for DataFetcher.")

        df = yf.download(self.tickers, start=self.start, end=self.end, progress=False)[
            "Close"
        ]

        # If only one ticker was provided, yfinance might return a Series instead of DataFrame
        if isinstance(df, pd.Series):
            df = df.to_frame()

        # Drop rows where all tickers have missing data
        df.dropna(how="all", inplace=True)

        # Store the resulting data internally
        self.data = df
        return df

    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Return the internally stored DataFrame if data has been fetched, otherwise None.

        :return: The DataFrame of downloaded prices or None if not fetched yet.
        :rtype: Optional[pd.DataFrame]
        """
        return self.data
