# visualizers.py

import matplotlib.pyplot as plt
import pandas as pd


def plot_sanity_check(df: pd.DataFrame, sample_cols: list, ylabel: str = ""):
    existing = [c for c in sample_cols if c in df.columns]
    if existing:
        ax = df[existing].plot.line()
        ax.legend(existing)
        if ylabel:
            ax.set_ylabel(ylabel)
        ax.grid()
        plt.show()


def plot_annual_and_decade(df_annual: pd.DataFrame, df_decade: pd.DataFrame):
    ax1 = df_annual.plot.line()
    ax1.set_ylabel("Value (annual)")
    ax1.set_xlabel("Year")
    ax1.grid()
    plt.show()

    ax2 = df_decade.plot.bar()
    ax2.set_ylabel("Value per Decade")
    ax2.set_xlabel("Decade End")
    ax2.grid()
    plt.show()
