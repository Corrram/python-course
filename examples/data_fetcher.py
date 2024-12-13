import pathlib

import yfinance as yf

# Define ticker symbols for S&P 500 Total Return and DAX Index
tickers = {
    "SP500_Total_Return": "^SP500TR",
    "DAX": "^GDAXI"
}

# Define the date range for data retrieval
start_date = "2000-01-01"  # Adjust the start date as needed
end_date = "2024-12-12"  # Adjust the end date as needed

pathlib.Path("data").mkdir(exist_ok=True)  # Create a directory to store dataq
# Loop through tickers to download and save data
for name, ticker in tickers.items():
    # Download historical data
    data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
    data.columns = data.columns.get_level_values(0)

    # Save the data to a CSV file
    file_name = f"data/{name}.csv"
    data.to_csv(file_name)
    print(f"{name} data saved to {file_name}")
