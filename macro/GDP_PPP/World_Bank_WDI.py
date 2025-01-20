import pandas as pd
import matplotlib.pyplot as plt


def excel_to_df(excel_file: str) -> pd.DataFrame:
    """
    Reads a World Bank-style Excel file, cleans/formats the data, and returns a DataFrame.
    Also plots a sanity check for certain countries/regions.

    Parameters
    ----------
    excel_file : str
        Path to the .xls or .xlsx file from the World Bank.

    Returns
    -------
    pd.DataFrame
        A cleaned DataFrame with years as the index and country names as columns.
    """
    # Read raw Excel
    df_raw = pd.read_excel(excel_file)

    # Drop unused columns and the first two header rows
    df_clean = df_raw.drop(
        columns = ["World Development Indicators", "Unnamed: 2", "Unnamed: 3"]
    )
    df_clean = df_clean.drop([0, 1], axis=0)

    # Transpose and set the new index
    df_clean = df_clean.transpose()
    df_clean = df_clean.set_index(2)

    # The row labeled "Country Name" is just a header; remove it
    df_clean.columns = df_clean.iloc[0]
    df_clean = df_clean.drop("Country Name", axis=0)

    # Drop any rows with null index (if they exist)
    df_clean = df_clean[df_clean.index.notnull()]

    # Transpose to get years as rows, then rename columns to int
    df_clean = df_clean.transpose()
    df_clean.columns = df_clean.columns.astype(int)
    df_clean = df_clean.transpose()
    df_clean.index.names = ["Year"]

    # Optional multiply (uncomment if needed)
    # df_clean = df_clean * 1000

    # Quick sanity check plot
    countries_to_plot = ["World", "Germany", "United States", "China"]
    existing_cols = [c for c in countries_to_plot if c in df_clean.columns]
    if existing_cols:
        ax = df_clean[existing_cols].plot.line()
        ax.set_ylabel("Dollars (annual)")
        ax.legend(existing_cols)
        ax.grid()
        plt.show()

    return df_clean


def aggregate_by_region(
    gdp_df: pd.DataFrame, income_classification_csv: str, oecd_csv_file: str
) -> pd.DataFrame:
    """
    Aggregate data by region categories. Uses:
      1) gdp_df: DataFrame with countries as columns, years as rows.
      2) income_classification_csv: CSV with columns [Country, IncomeGroup].
      3) oecd_csv_file: CSV with a single column 'Country' listing OECD countries.

    Returns a DataFrame whose columns are sums for each region.

    Parameters
    ----------
    gdp_df : pd.DataFrame
        DataFrame that has countries as columns and years as the index.
    income_classification_csv : str
        Path to CSV with two columns: Country, IncomeGroup (High, Upper_Middle, etc.).
    oecd_csv_file : str
        Path to CSV with a single column 'Country' listing OECD countries.

    Returns
    -------
    pd.DataFrame
        A DataFrame whose columns represent aggregated (summed) data per region.
    """
    # 1) Our main data is already a DataFrame
    data = gdp_df.copy()

    # 2) Read income classification (e.g., High, Low, etc.)
    classification_df = pd.read_csv(income_classification_csv)
    classification_dict = dict(
        zip(classification_df["Country"], classification_df["IncomeGroup"])
    )

    # 3) Read OECD countries from CSV
    df_oecd = pd.read_csv(oecd_csv_file)
    oecd_countries = df_oecd["Country"].tolist()

    # 4) Define special single-country "regions"
    usa_country = "United States"
    india_country = "India"
    russia_country = "Russian Federation"
    brazil_country = "Brazil"
    china_country = "China"

    # A) Low Income Countries (Low + Lower_Middle), excluding India
    low_income_countries = [
        c
        for c, inc in classification_dict.items()
        if inc in ["Low", "Lower_Middle"] and c != india_country
    ]

    # B) Other High Income:
    #    Income == "High" but NOT in {USA, Australia, NZ, Russia} or OECD
    other_high_income = [
        c
        for c, inc in classification_dict.items()
        if inc == "High"
        and c not in [usa_country, "Australia", "New Zealand", russia_country]
        and c not in oecd_countries
    ]

    # C) Developing countries:
    #    Income == "Upper_Middle" but exclude {China, Brazil, Turkiye}
    developing_countries = [
        c
        for c, inc in classification_dict.items()
        if inc == "Upper_Middle" and c not in [china_country, brazil_country, "Turkiye"]
    ]

    # 5) Build regions dictionary
    regions = {
        "USA": [usa_country],
        "India": [india_country],
        "Russia": [russia_country],
        "Brazil": [brazil_country],
        "China": [china_country],
        "Australia and New Zealand": ["Australia", "New Zealand"],
        "OECD Europe": oecd_countries,
        "Low Income Countries": low_income_countries,
        "Other High Income": other_high_income,
        "Developing countries": developing_countries,
        # Only valid if "World" is a column in data
        "World": ["World"],
    }

    # 6) Sum up data for each region
    df_result = pd.DataFrame(dtype=float)
    for region_name, countries in regions.items():
        valid_countries = [c for c in countries if c in data.columns]
        df_result[region_name] = data[valid_countries].sum(axis=1)

    return df_result


def aggregate_by_decade(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame with years as the index and aggregates values by decade.
    Also plots annual data (from year ~30 onward) and bar-charts for decade data.

    Parameters
    ----------
    data_df : pd.DataFrame
        DataFrame that has an integer year index and columns for different
        countries or regions.

    Returns
    -------
    pd.DataFrame
        A DataFrame aggregated by decade (sum of each 10-year span).
    """
    df = data_df.copy()
    df = df.loc[(df != 0).any(axis=1)]

    min_year = df.index.min()
    max_year = df.index.max()

    # Build a year range and a decade range
    all_years = range(min_year, max_year + 1)
    all_decades = range(min_year + 10, max_year + 1, 10)

    # Create a DataFrame to hold annual sums
    df_annual = pd.DataFrame(index=all_years, columns=df.columns)

    # DataFrame for decade sums
    df_decades = pd.DataFrame(index=all_decades)

    # 1) Summation by year
    for col in df.columns:
        for year in all_years:
            df_year = df.loc[df.index == year]
            df_annual.loc[year, col] = df_year[col].sum()

    # 2) Summation by decade
    for decade in all_decades:
        # The decade chunk is [decade-9 ... decade]
        start_idx = df_annual.index.get_loc(decade) - 9
        end_idx = df_annual.index.get_loc(decade) + 1
        df_decade_slice = df_annual.iloc[start_idx:end_idx]

        for col in df.columns:
            df_decades.loc[decade, col] = df_decade_slice[col].sum()

    # Optional: convert to millions, billions, etc. if needed
    # df_decades = df_decades * (1 / 1_000_000)

    # Plot annual data from year ~30 onward (to skip incomplete data)
    if 30 in df_annual.index:
        df_annual_sub = df_annual.loc[30:]
    else:
        df_annual_sub = df_annual

    ax1 = df_annual_sub.plot.line()
    ax1.set_ylabel("Dollars (annual)")
    ax1.set_xlabel("Year")
    ax1.grid()
    plt.show()

    # Plot decade-aggregated data
    ax2 = df_decades.plot.bar()  # skip first few if incomplete
    ax2.set_ylabel("Dollars per Decade")
    ax2.set_xlabel("Decade End")
    ax2.grid()
    plt.show()

    return df_decades


if __name__ == "__main__":
    # 1) Convert Excel to DataFrame (and plot)
    df_world_bank = excel_to_df("World_Bank_2022_WDI.xls")

    # 2) Aggregate data by region
    df_regions = aggregate_by_region(
        gdp_df=df_world_bank,
        income_classification_csv="../income_levels.csv",
        oecd_csv_file="../oecd_countries.csv",
    )

    # 3) Aggregate data by decade
    df_decade = aggregate_by_decade(df_regions)
