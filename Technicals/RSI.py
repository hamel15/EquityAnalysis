import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from alpha_vantage.timeseries import TimeSeries

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'G99W064UC2NCTP1R'
symbol = 'AAPL'

# Initialize Alpha Vantage API
ts = TimeSeries(key=api_key, output_format='pandas')

# Retrieve historical daily stock data for AAPL
data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')  # 'compact' for last 100 data points

# Convert index to DateTimeIndex
data.index = pd.to_datetime(data.index)

# Calculate daily price changes
data['delta'] = data['4. close'].diff()

# Calculate gains and losses
data['gain'] = np.where(data['delta'] > 0, data['delta'], 0)
data['loss'] = np.where(data['delta'] < 0, -data['delta'], 0)

# Calculate average gains and losses over a specified period (usually 14 days)
period = 30  # Increased window size
data['avg_gain'] = data['gain'].rolling(window=period, min_periods=1).mean()
data['avg_loss'] = data['loss'].rolling(window=period, min_periods=1).mean()

# Calculate relative strength (RS)
data['rs'] = data['avg_gain'] / data['avg_loss']

# Calculate Relative Strength Index (RSI)
data['rsi'] = 100 - (100 / (1 + data['rs']))

# Select data from April 1, 2024, onwards
start_date = '2024-04-01'
data_from_april_1 = data.loc[start_date:]

# Drop rows with NaN values
data_from_april_1 = data_from_april_1.dropna()

# Plot RSI
plt.figure(figsize=(10, 5))
plt.plot(data_from_april_1.index, data_from_april_1['rsi'], label='RSI', color='blue')
plt.title('Relative Strength Index (RSI) for {} - Since April 1, 2024'.format(symbol))
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()
plt.grid(True)

# Convert start date to numeric representation for plotting
start_date_num = mdates.datestr2num(start_date)

# Set x-axis limits to start from April 1, 2024
plt.xlim(start_date_num, data_from_april_1.index.max())

plt.show()
