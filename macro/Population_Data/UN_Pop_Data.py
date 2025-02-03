import pandas as pd
import matplotlib.pyplot as plt


def Excl_to_Csv(file_name, projection_sheet):
    """
    Reads multiple sheets ("Estimates", `projection_sheet`) from UN_2024_Population_Data.xlsx
    and merges them into a single DataFrame with 'Year' as index and one column per region.
    Returns this DataFrame after multiplying values by 1,000 (since original data is in 'thousands').
    Also plots a quick check with "World", "China", and "India".
    """
    # Create a dictionary to hold DataFrames from each sheet
    dict_data = {}

    for sheet in ["Estimates", projection_sheet]:
        # Read the file
        df = pd.read_excel("UN_2024_Population_Data.xlsx", sheet)

        # Skip the first 15 rows, then re-assign column headers from row 16
        df = df.iloc[15:, :].copy()
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace=True)  # remove the duplicate header row

        # Rename the main region column
        df.rename(
            columns={"Region, subregion, country or area *": "Region"}, inplace=True
        )

        # Collect ages 0..98 plus "100+"
        ages = list(range(0, 99)) + ["100+"]

        # Keep only ["Region", "Year"] + ages
        df = df[["Region", "Year"] + ages].copy()

        # Sum across all ages for "Total Population"
        df["Total Population"] = df[ages].sum(axis=1)

        # Keep only ["Region", "Year", "Total Population"]
        df = df[["Region", "Year", "Total Population"]]

        # Unique region names, unique years
        regions = df["Region"].unique()
        years = [year for year in df["Year"].unique() if isinstance(year, int)]

        # Set multi-index (Region, Year)
        df.set_index(["Region", "Year"], inplace=True)
        df.sort_index(inplace=True)

        # Create a blank DataFrame (years as index, each region as a column)
        csv_df = pd.DataFrame(columns=regions, index=years, dtype=float)

        # Fill in the values from df
        missing = set()  # track regions that have no data
        for region in regions:
            for year in years:
                try:
                    val = df.loc[(region, year), "Total Population"]
                    # If multiple rows, val might be a Series -> pick first
                    csv_df.loc[year, region] = (
                        val.iloc[0] if hasattr(val, "iloc") else val
                    )
                except KeyError:
                    missing.add(region)

        print(f"Sheet: {sheet}. Regions without numbers:", missing)

        # Drop columns that have no data
        csv_df.drop(columns=missing, inplace=True)

        dict_data[sheet] = csv_df

    # Merge DataFrames for "Estimates" and the projection_sheet
    merged_df = pd.concat([dict_data["Estimates"], dict_data[projection_sheet]])

    # Multiply by 1,000 (data was in thousands)
    merged_df = merged_df * 1000

    # Quick sanity-check plot
    # If columns "World", "China", "India" exist, plot them
    to_plot = [col for col in ["World", "China", "India"] if col in merged_df.columns]
    if to_plot:
        ax = merged_df[to_plot].plot.line()
        ax.set_ylabel("Population")
        ax.grid()
        plt.show()

    return merged_df


def Aggregate_by_Region(
    file_name: str, start_year: int, income_levels_csv: str, oecd_countries_csv: str
):
    """
    Aggregates population data by region. Uses 'income_levels.csv' and 'oecd_countries.csv'
    to build region groups instead of hardcoded lists.

    Parameters
    ----------
    file_name : str
        Path to the CSV file produced by Excl_to_Csv.
    start_year : int
        The year from which decades are counted (for final bar plot).
    income_levels_csv : str
        CSV with columns: [Country, IncomeGroup] -> 'High', 'Upper_Middle', 'Lower_Middle', 'Low'.
    oecd_countries_csv : str
        CSV with one column [Country], listing OECD countries.

    Returns
    -------
    pd.DataFrame
        A DataFrame (df_model) aggregated by region/decade + a bar-plot for sanity check.
    """

    data = pd.read_csv(file_name, index_col=0)

    # 1) Build classification dict from 'income_levels.csv'
    classification_df = pd.read_csv(income_levels_csv)
    classification_dict = dict(
        zip(classification_df["Country"], classification_df["IncomeGroup"])
    )

    # 2) Read OECD countries
    df_oecd = pd.read_csv(oecd_countries_csv)
    oecd_countries = df_oecd["Country"].tolist()

    # 3) Build the 4 lists from the classification dict
    high_income = [c for c, grp in classification_dict.items() if grp == "High"]
    upper_middle_income = [
        c for c, grp in classification_dict.items() if grp == "Upper_Middle"
    ]
    lower_middle_income = [
        c for c, grp in classification_dict.items() if grp == "Lower_Middle"
    ]
    low_income = [c for c, grp in classification_dict.items() if grp == "Low"]

    # 4) Build the 'regions' dict (some naming mismatches may require manual fixes)
    regions = {
        "USA": ["United States of America"],
        "India": ["India"],
        "Russia": ["Russian Federation"],
        "Brazil": ["Brazil"],
        "China": ["China"],
        "Australia and New Zealand": ["Australia/New Zealand"],
        "OECD Europe": oecd_countries,
        "Low Income Countries": [
            c for c in (low_income + lower_middle_income) if c != "India"
        ],
        "Other High Income": [
            c
            for c in high_income
            if c
            not in [
                "United States of America",
                "Australia/New Zealand",
                "Russian Federation",
            ]
            + oecd_countries
        ],
        "Developing countries": [
            c for c in upper_middle_income if c not in ["China", "Brazil", "Türkiye"]
        ],
        "World": ["World"],
    }

    # 5) Aggregate the population for these regions
    df = pd.DataFrame(dtype=float)
    for region_name, countries in regions.items():
        valid_cols = [c for c in countries if c in data.columns]
        df[region_name] = data[valid_cols].sum(axis=1)

    # 6) Extend population through 2110 by repeating row 2100 (if present)
    if 2100 in df.index:
        repeated_pop = df.loc[[2100] * 10].copy()
        repeated_pop.index = list(range(2101, 2111))
        df = pd.concat([df, repeated_pop])
    else:
        print("Note: Year 2100 not found in data, skipping extension to 2110")

    # 7) Decade-aggregation logic
    periods = list(range(start_year + 4, start_year + 94, 10))
    list_model = []
    for period in periods:
        subset = df.loc[period - 4 : period + 5].copy()
        list_model.append(subset.mean())

    df_model = pd.concat(list_model, axis=1).T

    # Plot a bar chart for the decade-aggregated DataFrame
    ax = df_model.plot.bar()
    ax.set_xlabel(f"Decades since {start_year - 1}")
    ax.set_ylabel("Mean Population in each Category")
    ax.grid()
    plt.show()

    return df_model


if __name__ == "__main__":
    projection_sheet = "Medium variant"
    start_year = 2011

    # 1) Produce the base DataFrame from Excel (no CSV writing)
    df_csv = Excl_to_Csv("UN_2024_Population_Data.xlsx", projection_sheet)

    # 2) Aggregate by region using your new CSV approach (again, no CSV writing here)
    df_mult = Aggregate_by_Region(
        file_name=f"UN Population Projections {projection_sheet}.csv",  # Or pass an in-memory DF if desired
        start_year=start_year,
        income_levels_csv="../income_levels.csv",
        oecd_countries_csv="../oecd_countries.csv",
    )
