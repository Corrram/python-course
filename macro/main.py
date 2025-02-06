# main.py

from data_manager import DataManager
from aggregators import aggregate_by_region, aggregate_by_decade
from visualizers import plot_annual_and_decade, plot_sanity_check


def main():
    manager = DataManager()

    # 1) Classification data (read once)
    manager.load_classification_data("income_levels.csv", "oecd_countries.csv")

    # 2) Carbon Emissions
    manager.load_carbon(
        "Emissions_Data/Carbon_Project_2023_Emissions_by_Nation.xlsx",
        sheet_name="Territorial Emissions",
    )
    df_carbon = manager.df_carbon
    plot_sanity_check(
        df_carbon,
        ["World", "Germany", "USA", "China", "India"],
        ylabel="Emissions in MtC",
    )

    df_carbon_reg = aggregate_by_region(
        df_carbon,
        classification_dict=manager.classification_dict,
        oecd_list=manager.oecd_countries,
    )
    df_carbon_dec = aggregate_by_decade(df_carbon_reg)
    plot_annual_and_decade(df_carbon_reg, df_carbon_dec)

    # 3) World Bank
    manager.load_world_bank("GDP_PPP/World_Bank_2022_WDI.xls")
    df_wb = manager.df_wb
    plot_sanity_check(
        df_wb, ["World", "Germany", "United States", "China"], ylabel="WDI Metric"
    )

    df_wb_reg = aggregate_by_region(
        df_wb,
        classification_dict=manager.classification_dict,
        oecd_list=manager.oecd_countries,
    )
    df_wb_dec = aggregate_by_decade(df_wb_reg)
    plot_annual_and_decade(df_wb_reg, df_wb_dec)

    # 4) UN Population
    manager.load_un_population(
        path_estimates="Population_Data/UN_2024_Population_Data_Estimates.parquet",
        path_medium="Population_Data/UN_2024_Population_Data_Medium_variant.parquet",
        sheet_est="Estimates",
        sheet_med="Medium variant",
        use_parquet=True,
    )
    df_un = manager.df_un
    plot_sanity_check(df_un, ["World", "China", "India"], ylabel="Population")

    df_un_reg = aggregate_by_region(
        df_un,
        classification_dict=manager.classification_dict,
        oecd_list=manager.oecd_countries,
    )
    df_un_dec = aggregate_by_decade(df_un_reg)
    plot_annual_and_decade(df_un_reg, df_un_dec)

    print("=== Done! ===")


if __name__ == "__main__":
    main()
