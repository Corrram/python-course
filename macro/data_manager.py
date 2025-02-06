# data_manager.py
import pandas as pd
from cleansers import (
    clean_territorial_emissions,
    clean_world_bank_data,
    clean_un_population_data,
)


class DataManager:
    """
    Loads raw data from disk (Excel, CSV, Parquet, etc.) exactly once
    and provides properties/methods to retrieve:
      - Cleaned DataFrames (Carbon, WBank, UN)
      - Classification dictionary (income_levels)
      - OECD country list
    """

    def __init__(self):
        # Raw data placeholders
        self._raw_carbon = None
        self._raw_wb = None
        self._raw_un_estimates = None
        self._raw_un_medium = None

        # Cleaned data placeholders
        self._df_carbon = None
        self._df_wb = None
        self._df_un = None

        # Classification placeholders
        self._classification_dict = None
        self._oecd_countries = None

    # ------------------------------------------------------------------
    # Data loading (only once)
    # ------------------------------------------------------------------
    def load_carbon(self, path_excel: str, sheet_name: str = "Territorial Emissions"):
        if self._raw_carbon is None:
            print(f"Loading Carbon data from {path_excel}...")
            self._raw_carbon = pd.read_excel(path_excel, sheet_name=sheet_name)

    def load_world_bank(self, path_excel: str):
        if self._raw_wb is None:
            print(f"Loading World Bank data from {path_excel}...")
            self._raw_wb = pd.read_excel(path_excel)

    def load_un_population(
        self,
        path_estimates: str,
        path_medium: str,
        sheet_est: str = "Estimates",
        sheet_med: str = "Medium variant",
        use_parquet: bool = False,
    ):
        if self._raw_un_estimates is None or self._raw_un_medium is None:
            if use_parquet:
                print(
                    f"Loading UN population from {path_estimates} and {path_medium} (Parquet)..."
                )
                if not path_estimates.endswith(".parquet"):
                    raise ValueError("Expected .parquet file for UN estimates.")
                self._raw_un_estimates = pd.read_parquet(path_estimates)
                if not path_medium.endswith(".parquet"):
                    raise ValueError("Expected .parquet file for UN medium variant.")
                self._raw_un_medium = pd.read_parquet(path_medium)
            else:
                print(
                    f"Loading UN population from {path_estimates} and {path_medium} (Excel)..."
                )
                if not path_estimates.endswith(".xlsx"):
                    raise ValueError("Expected .xlsx file for UN estimates.")
                self._raw_un_estimates = pd.read_excel(
                    path_estimates, sheet_name=sheet_est
                )
                if not path_medium.endswith(".xlsx"):
                    raise ValueError("Expected .xlsx file for UN medium variant.")
                self._raw_un_medium = pd.read_excel(path_medium, sheet_name=sheet_med)

    def load_classification_data(self, income_levels_csv: str, oecd_countries_csv: str):
        """
        Reads classification files (income_levels.csv + oecd_countries.csv)
        exactly once.
        """
        if self._classification_dict is None or self._oecd_countries is None:
            print(
                f"Loading classification data from {income_levels_csv} and {oecd_countries_csv}..."
            )
            classification_df = pd.read_csv(income_levels_csv)
            self._classification_dict = dict(
                zip(classification_df["Country"], classification_df["IncomeGroup"])
            )

            df_oecd = pd.read_csv(oecd_countries_csv)
            self._oecd_countries = df_oecd["Country"].tolist()

    # ------------------------------------------------------------------
    # Properties: cleaned data
    # ------------------------------------------------------------------
    @property
    def df_carbon(self) -> pd.DataFrame:
        if self._df_carbon is None:
            if self._raw_carbon is None:
                raise ValueError("Carbon data not loaded. Call load_carbon first.")
            self._df_carbon = clean_territorial_emissions(self._raw_carbon)
        return self._df_carbon

    @property
    def df_wb(self) -> pd.DataFrame:
        if self._df_wb is None:
            if self._raw_wb is None:
                raise ValueError(
                    "World Bank data not loaded. Call load_world_bank first."
                )
            self._df_wb = clean_world_bank_data(self._raw_wb)
        return self._df_wb

    @property
    def df_un(self) -> pd.DataFrame:
        if self._df_un is None:
            if self._raw_un_estimates is None or self._raw_un_medium is None:
                raise ValueError(
                    "UN population data not loaded. Call load_un_population first."
                )

            df_est = clean_un_population_data({"Estimates": self._raw_un_estimates})
            df_med = clean_un_population_data({"Medium variant": self._raw_un_medium})
            self._df_un = pd.concat([df_est, df_med], axis=0)

        return self._df_un

    # ------------------------------------------------------------------
    # Properties: classification + OECD
    # ------------------------------------------------------------------
    @property
    def classification_dict(self) -> dict:
        if self._classification_dict is None:
            raise ValueError(
                "Classification data not loaded. Call load_classification_data first."
            )
        return self._classification_dict

    @property
    def oecd_countries(self) -> list[str]:
        if self._oecd_countries is None:
            raise ValueError(
                "OECD data not loaded. Call load_classification_data first."
            )
        return self._oecd_countries
