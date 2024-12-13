import pandas as pd


def main():
    sp500 = pd.read_csv("data/SP500_Total_Return.csv")
    dax = pd.read_csv("data/DAX.csv")
    print("Done!")

if __name__ == "__main__":
    main()