import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'G99W064UC2NCTP1R'
symbols = ['AAPL', 'MSFT', 'NVDA', 'TSLA']

# Initialize Alpha Vantage API
ts = TimeSeries(key=api_key, output_format='pandas')

# Initialize dictionaries to store RSI values for each symbol
rsi_values = {}

# Retrieve historical daily stock data for each symbol
for symbol in symbols:
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')  # 'compact' for last 100 data points

    # Calculate daily price changes
    data['delta'] = data['4. close'].diff()

    # Calculate gains and losses
    data['gain'] = np.where(data['delta'] > 0, data['delta'], 0)
    data['loss'] = np.where(data['delta'] < 0, -data['delta'], 0)

    # Calculate average gains and losses over a specified period (usually 14 days)
    period = 14
    data['avg_gain'] = data['gain'].rolling(window=period, min_periods=1).mean()
    data['avg_loss'] = data['loss'].rolling(window=period, min_periods=1).mean()

    # Calculate relative strength (RS)
    data['rs'] = data['avg_gain'] / data['avg_loss']

    # Calculate Relative Strength Index (RSI)
    data['rsi'] = 100 - (100 / (1 + data['rs']))

    # Store the most recent RSI value for each symbol
    rsi_values[symbol] = data['rsi'].iloc[-1]

# Print the most recent RSI value for each symbol
for symbol, rsi_value in rsi_values.items():
    print("Most recent RSI for {}: {:.2f}".format(symbol, rsi_value))
