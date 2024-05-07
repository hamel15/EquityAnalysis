import os
import yfinance as yf
import pandas as pd

def calculate_macd(symbol):
    # Download historical data
    data = yf.download(symbol, start="2020-01-01", end="2024-01-01")

    # Calculate MACD
    data['26EMA'] = data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()
    data['12EMA'] = data['Close'].ewm(span=12, min_periods=0, adjust=False).mean()
    data['MACD'] = data['12EMA'] - data['26EMA']
    data['Signal_Line'] = data['MACD'].ewm(span=9, min_periods=0, adjust=False).mean()

    # Calculate 200-day SMA
    data['200SMA'] = data['Close'].rolling(window=200).mean()

    # Get the last MACD, Signal Line, 200-day SMA, and latest price values
    last_macd = data['MACD'].iloc[-1]
    last_signal_line = data['Signal_Line'].iloc[-1]
    last_200sma = data['200SMA'].iloc[-1]
    latest_price = data['Close'].iloc[-1]

    print(f"MACD: {last_macd}, Signal Line: {last_signal_line}, 200-day SMA: {last_200sma}, Latest Price: {latest_price}")

    # Determine buy or sell signal
    if last_macd > 0 and last_signal_line > 0 and last_signal_line > last_macd and latest_price > last_200sma:
        signal = "Buy Signal"
    elif last_macd < 0 and last_signal_line < 0 and last_signal_line < last_macd and latest_price < last_200sma:
        signal = "Sell Signal"
    else:
        signal = "No Clear Signal"

    return last_macd, last_signal_line, last_200sma, latest_price, signal

def main():
    tickers = ['ODD', 'MSFT', 'GOOGL', 'AMZN']
    data_list = []

    for ticker in tickers:
        result = calculate_macd(ticker)
        if result:
            macd, signal_line, sma_200, latest_price, signal = result
            data_list.append([ticker, macd, signal_line, sma_200, latest_price, signal])
        else:
            print(f"Failed to retrieve data for {ticker}")

    # Create DataFrame
    df = pd.DataFrame(data_list, columns=['Ticker', 'MACD', 'Signal Line', '200-day SMA', 'Latest Price', 'Signal'])

    # Export to Excel
    export_path = r"C:\Users\tdham\OneDrive\Documents\Python Exports\MacD 200D"
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    excel_file = os.path.join(export_path, "MACD_200D_signals.xlsx")
    df.to_excel(excel_file, index=False)

    print(f"Data exported to: {excel_file}")

if __name__ == "__main__":
    main()
