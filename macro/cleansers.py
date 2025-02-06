# cleansers.py

import pandas as pd


def clean_territorial_emissions(df_raw: pd.DataFrame) -> pd.DataFrame:
    df_clean = df_raw.drop(range(0, 10), axis=0).copy()
    df_clean = df_clean.set_index("Unnamed: 0")
    df_clean.columns = df_clean.iloc[0]
    df_clean = df_clean.iloc[1:]
    df_clean.index.names = ["Year"]
    return df_clean


def clean_world_bank_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    df_clean = df_raw.copy()

    possible_cols = ["World Development Indicators", "Unnamed: 2", "Unnamed: 3"]
    cols_to_drop = [c for c in possible_cols if c in df_clean.columns]
    df_clean.drop(cols_to_drop, axis=1, inplace=True, errors="ignore")

    if df_clean.shape[0] > 2:
        df_clean.drop([0, 1], axis=0, inplace=True)

    df_clean = df_clean.transpose()
    if 2 in df_clean.index:
        df_clean = df_clean.set_index(2)

    if not df_clean.empty:
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean.iloc[1:]
        df_clean = df_clean[df_clean.index.notnull()]

        df_clean = df_clean.transpose()
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean.drop("Country Name", axis=0, errors="ignore")
        df_clean = df_clean.loc[:, df_clean.columns.notnull()]
        df_clean = df_clean.dropna(how="all", axis=1)

        df_clean.columns = [int(col) for col in df_clean.columns]
        df_clean = df_clean.transpose()
        df_clean.index.names = ["Year"]

    return df_clean


def clean_un_population_data(raw_sheets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    dict_data = {}
    for sheet_name, df in raw_sheets.items():
        df_clean = df.iloc[15:, :].copy()
        df_clean.columns = df_clean.iloc[0]
        df_clean.drop(df_clean.index[0], inplace=True)
        df_clean.rename(
            columns={"Region, subregion, country or area *": "Region"}, inplace=True
        )

        ages = [str(i) for i in range(0, 99)] + ["100+"]
        keep_cols = ["Region", "Year"] + [
            col for col in ages if col in df_clean.columns
        ]
        df_clean = df_clean[keep_cols].copy()
        df_clean = df_clean[~df_clean["Year"].isna()]

        df_clean["Total Population"] = df_clean[ages].astype(float).sum(axis=1)

        df_clean = df_clean[["Region", "Year", "Total Population"]]

        regions = df_clean["Region"].unique()
        years = [year for year in df_clean["Year"].unique()]

        df_clean.set_index(["Region", "Year"], inplace=True)
        df_clean.sort_index(inplace=True)

        csv_df = pd.DataFrame(index=years, columns=regions, dtype=float)

        missing = set()
        for region in regions:
            for year in years:
                try:
                    val = df_clean.loc[(region, year), "Total Population"]
                    csv_df.loc[year, region] = (
                        val.iloc[0] if hasattr(val, "iloc") else val
                    )
                except KeyError:
                    missing.add(region)

        csv_df.drop(columns=missing, inplace=True)
        dict_data[sheet_name] = csv_df

    merged_df = pd.concat(dict_data.values(), axis=0)
    merged_df = merged_df * 1000
    return merged_df
