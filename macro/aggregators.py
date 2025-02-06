# aggregators.py

import pandas as pd


def aggregate_by_region(
    df_in: pd.DataFrame, classification_dict: dict, oecd_list: list[str]
) -> pd.DataFrame:
    """
    Summation by region using a classification dict + a list of OECD countries.
    """
    data = df_in.copy()

    # Build lists from classification_dict
    high_income = [c for c, grp in classification_dict.items() if grp == "High"]
    upper_middle = [
        c for c, grp in classification_dict.items() if grp == "Upper_Middle"
    ]
    lower_middle = [
        c for c, grp in classification_dict.items() if grp == "Lower_Middle"
    ]
    low_income = [c for c, grp in classification_dict.items() if grp == "Low"]

    regions = {
        "USA": ["USA", "United States of America"],
        "India": ["India"],
        "Russia": ["Russia", "Russian Federation"],
        "Brazil": ["Brazil"],
        "China": ["China"],
        "Australia and New Zealand": ["Australia", "New Zealand"],
        "OECD Europe": oecd_list,
        "Low Income Countries": [
            c for c in (low_income + lower_middle) if c not in ["India"]
        ],
        "Other High Income": [
            c
            for c in high_income
            if c not in ["USA", "Australia", "New Zealand", "Russia"] + oecd_list
        ],
        "Developing countries": [
            c for c in upper_middle if c not in ["China", "Brazil", "Türkiye"]
        ],
        "World": ["World"],
    }

    df_agg = pd.DataFrame(dtype=float)
    for region_name, countries in regions.items():
        valid_cols = [col for col in countries if col in data.columns]
        df_agg[region_name] = data[valid_cols].sum(axis=1)

    return df_agg


def aggregate_by_decade(df_in: pd.DataFrame) -> pd.DataFrame:
    df = df_in.copy()
    df.index = df.index.astype(int)

    min_year, max_year = df.index.min(), df.index.max()

    all_years = range(min_year, max_year + 1)
    df_annual = df.reindex(all_years, fill_value=0)

    all_decades = range(min_year + 9, max_year + 1, 10)
    df_decades = pd.DataFrame(index=all_decades, columns=df.columns, dtype=float)

    for dec in all_decades:
        decade_slice = df_annual.loc[dec - 9 : dec]
        df_decades.loc[dec] = decade_slice.sum(axis=0)

    return df_decades
