import pandas as pd
import matplotlib.pyplot as plt


def Excl_to_Csv(file_name: str) -> pd.DataFrame:
    """
    Reads an Excel sheet named "Territorial Emissions" from <file_name>.xlsx,
    performs formatting, and returns a cleaned DataFrame with 'Year' as the index
    and each country/region as a column.

    Parameters
    ----------
    file_name : str
        Base file name (without .xlsx extension).

    Returns
    -------
    pd.DataFrame
        The cleaned DataFrame with years as rows and countries/regions as columns.
    """
    # Read Excel
    df = pd.read_excel(f"{file_name}.xlsx", "Territorial Emissions")

    # Formatting
    # Drop the first 10 rows, set "Unnamed: 0" as index, rename columns from the first row, etc.
    df_clean = df.drop(range(0, 10), axis=0).copy()
    df_clean = df_clean.set_index("Unnamed: 0")
    df_clean.columns = df_clean.iloc[0]
    df_clean = df_clean.iloc[1:]
    df_clean.index.names = ["Year"]

    # (Optional) multiply by a factor if needed
    # df_clean = df_clean * 1000

    # Quick sanity check plot
    regions = ["World", "Germany", "USA", "China", "India"]
    existing_cols = [col for col in regions if col in df_clean.columns]
    if existing_cols:
        ax = df_clean[existing_cols].plot.line()
        ax.legend(existing_cols)
        ax.set_ylabel("Emissions in MtC")
        ax.grid()
        plt.show()

    return df_clean


def Aggregate_by_Region(
    df_in: pd.DataFrame, income_levels_csv: str, oecd_countries_csv: str
) -> pd.DataFrame:
    """
    Aggregates the input DataFrame by region groups (High, Upper_Middle, Lower_Middle, Low),
    and an OECD list. Reads 'income_levels.csv' and 'oecd_countries.csv' to avoid hard-coded lists.

    Parameters
    ----------
    df_in : pd.DataFrame
        DataFrame with years as rows (index) and country/region names as columns.
    income_levels_csv : str
        Path to a CSV with columns [Country, IncomeGroup]
        where IncomeGroup is one of {High, Upper_Middle, Lower_Middle, Low}.
    oecd_countries_csv : str
        Path to a CSV with a single column [Country], listing OECD countries.

    Returns
    -------
    pd.DataFrame
        A new DataFrame (df_agg) with aggregated emissions for each defined region.
    """
    data = df_in.copy()

    # 1) Read classification CSV (Country -> IncomeGroup)
    #    Example row: "Austria",High
    classification_df = pd.read_csv(income_levels_csv)
    classification_dict = dict(
        zip(classification_df["Country"], classification_df["IncomeGroup"])
    )

    # 2) Separate countries by income level
    high_income = [c for c, grp in classification_dict.items() if grp == "High"]
    upper_middle_income = [
        c for c, grp in classification_dict.items() if grp == "Upper_Middle"
    ]
    lower_middle_income = [
        c for c, grp in classification_dict.items() if grp == "Lower_Middle"
    ]
    low_income = [c for c, grp in classification_dict.items() if grp == "Low"]

    # 3) Read OECD countries
    df_oecd = pd.read_csv(oecd_countries_csv)
    oecd_countries = df_oecd["Country"].tolist()

    # 4) Build the regions dictionary
    regions = {
        "USA": ["USA"],
        "India": ["India"],
        "Russia": ["Russia"],
        "Brazil": ["Brazil"],
        "China": ["China"],
        "Australia and New Zealand": ["Australia", "New Zealand"],
        "OECD Europe": oecd_countries,  # from CSV
        # Combine Low + Lower_Middle, but exclude "India"
        "Low Income Countries": [
            c for c in (low_income + lower_middle_income) if c != "India"
        ],
        # High income minus {USA, Australia, NZ, Russia} and any in OECD
        "Other High Income": [
            c
            for c in high_income
            if c not in ["USA", "Australia", "New Zealand", "Russia"] + oecd_countries
        ],
        # Upper_Middle minus {China, Brazil, Türkiye}
        "Developing countries": [
            c for c in upper_middle_income if c not in ["China", "Brazil", "Türkiye"]
        ],
        "World": ["World"],
    }

    # 5) Aggregate the data
    df_agg = pd.DataFrame(dtype=float)
    for region_name, countries in regions.items():
        valid_cols = [col for col in countries if col in data.columns]
        df_agg[region_name] = data[valid_cols].sum(axis=1)

    return df_agg


def Aggregate_by_Decade(df_in: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates the input DataFrame by decade. Plots both annual and decade-based data.

    Parameters
    ----------
    df_in : pd.DataFrame
        DataFrame with integer years as the index and region/country columns.

    Returns
    -------
    pd.DataFrame
        Decade-aggregated DataFrame (sums per decade).
    """
    df = df_in.copy()

    # Ensure the index is integer-based
    df.index = df.index.astype(int)

    min_year = df.index.min()
    max_year = df.index.max()

    # Build year and decade ranges
    Years = range(min_year, max_year + 1, 1)
    Decades = range(min_year + 10, max_year + 1, 10)

    # Prepare DataFrames for annual and decade sums
    dfAnnual = pd.DataFrame(index=Years, columns=df.columns)
    dfDecades = pd.DataFrame(index=Decades)

    # 1) Summation by year
    for region in df.columns:
        for yr in Years:
            dfYear = df.loc[df.index == yr, region]
            dfAnnual.loc[yr, region] = dfYear.sum()

    # 2) Summation by decade
    for dec in Decades:
        start_loc = dfAnnual.index.get_loc(dec) - 9
        end_loc = dfAnnual.index.get_loc(dec) + 1
        dfDecade = dfAnnual.iloc[start_loc:end_loc]
        for region in df.columns:
            dfDecades.loc[dec, region] = dfDecade[region].sum()

    # Plot annual data
    plt1 = dfAnnual.plot.line()
    plt1.set_ylabel("Emissions in MtC")
    plt1.grid()
    plt.show()

    # Plot decade-aggregated data
    plt2 = dfDecades.plot.bar()
    plt2.set_ylabel("Emissions in MtC per Decade")
    plt2.grid()
    plt.show()

    return dfDecades


# ---------------
# Example usage
# ---------------
if __name__ == "__main__":
    # 1) Load Excel data into DataFrame (no CSV writing)
    csv_file_df = Excl_to_Csv(file_name="Carbon_Project_2023_Emissions_by_Nation")

    # 2) Aggregate by region, reading classification from CSV files
    df_mult = Aggregate_by_Region(
        df_in=csv_file_df,
        income_levels_csv="../income_levels.csv",
        oecd_countries_csv="../oecd_countries.csv",
    )

    # 3) Aggregate by decade (no CSV writing)
    df_mult_dec = Aggregate_by_Decade(df_mult)
