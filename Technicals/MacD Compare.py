import yfinance as yf


def calculate_macd(symbol):
    # Download historical data
    data = yf.download(symbol, start="2020-01-01", end="2024-01-01")

    # Calculate MACD
    data['26EMA'] = data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()
    data['12EMA'] = data['Close'].ewm(span=12, min_periods=0, adjust=False).mean()
    data['MACD'] = data['12EMA'] - data['26EMA']
    data['Signal_Line'] = data['MACD'].ewm(span=9, min_periods=0, adjust=False).mean()

    # Get the last MACD and Signal Line values
    last_macd = data['MACD'].iloc[-1]
    last_signal_line = data['Signal_Line'].iloc[-1]

    print(f"MACD: {last_macd}, Signal Line: {last_signal_line}")

    # Determine buy or sell signal
    if last_macd > 0 and last_signal_line > 0:
        if last_macd < last_signal_line:
            signal = "Buy Signal"
        else:
            signal = "No Clear Signal"
    elif last_macd < 0 and last_signal_line < 0:
        if last_macd > last_signal_line:
            signal = "Sell Signal"
        else:
            signal = "No Clear Signal"
    else:
        signal = "No Clear Signal"

    return last_macd, last_signal_line, signal


def main():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    for ticker in tickers:
        result = calculate_macd(ticker)
        if result:
            macd, signal_line, signal = result
            print(f"Ticker: {ticker}, MACD: {macd}, Signal Line: {signal_line}, Signal: {signal}")
        else:
            print(f"Failed to retrieve data for {ticker}")


if __name__ == "__main__":
    main()
