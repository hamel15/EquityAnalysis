import os
import requests
import pandas as pd
import datetime

# Define API key
API_KEY = "MaOslbBiDM4Cbv6il5DNiK1bakuOWDj4"

# Define base URL for API requests
BASE_URL = "https://api.polygon.io"

# Define directory to save financial statements
SAVE_DIR = "C:\\Users\\tdham\\PycharmProjects\\Financial Statements"

def fetch_balance_sheet(ticker):
    url = f"{BASE_URL}/v2/reference/financials/{ticker}?type=Q&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if 'results' not in data:
        print(f"Error fetching balance sheet for {ticker}")
        return None
    # Sort the results by filing date to get the most recent balance sheet
    results = sorted(data['results'], key=lambda x: x['calendarDate'], reverse=True)
    df = pd.DataFrame(results[:1])  # Select the most recent balance sheet
    return df

def save_statement(df, ticker):
    # Create directory if it doesn't exist
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    # Add timestamp to filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Save balance sheet as CSV
    filename = os.path.join(SAVE_DIR, f"{ticker}_balance_sheet_{timestamp}.csv")
    df.to_csv(filename, index=False)
    print(f"Balance sheet saved to: {filename}")

# Example usage
ticker = "AAPL"
balance_sheet_df = fetch_balance_sheet(ticker)
if balance_sheet_df is not None:
    save_statement(balance_sheet_df, ticker)
