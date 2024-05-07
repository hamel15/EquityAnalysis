import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'G99W064UC2NCTP1R'

# Initialize Alpha Vantage API
ts = TimeSeries(key=api_key, output_format='pandas')

# Specify the symbol and time period
symbol = 'AAPL'
interval = 'daily'  # Daily interval

# Get historical stock data
data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')  # 'compact' for last 100 data points

# Calculate 20-day Simple Moving Average (SMA) and standard deviation
data['20SMA'] = data['4. close'].rolling(window=20).mean()
data['std'] = data['4. close'].rolling(window=20).std()

# Calculate upper and lower Bollinger Bands
data['UpperBand'] = data['20SMA'] + (2 * data['std'])
data['LowerBand'] = data['20SMA'] - (2 * data['std'])

# Slice the DataFrame to include only the last 10 days
data_last_10_days = data.tail(10)

# Plot the closing price and Bollinger Bands
plt.figure(figsize=(12, 6))
plt.plot(data_last_10_days.index, data_last_10_days['4. close'], label='Closing Price', color='blue')
plt.plot(data_last_10_days.index, data_last_10_days['20SMA'], label='20-day SMA', color='black', linestyle='--')
plt.plot(data_last_10_days.index, data_last_10_days['UpperBand'], label='Upper Band', color='red', linestyle='--')
plt.plot(data_last_10_days.index, data_last_10_days['LowerBand'], label='Lower Band', color='green', linestyle='--')
plt.fill_between(data_last_10_days.index, data_last_10_days['UpperBand'], data_last_10_days['LowerBand'], color='gray', alpha=0.2)
plt.title('Bollinger Bands for AAPL (Last 10 Days)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
