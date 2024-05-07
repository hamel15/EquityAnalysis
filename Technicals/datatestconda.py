from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'G99W064UC2NCTP1R'
ts = TimeSeries(key=api_key, output_format='pandas')

# Replace 'AAPL' with the symbol of the stock you're interested in
symbol = 'AAPL'

# Get historical data
data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')

# Calculate momentum (Rate of Change) for a specific period (e.g., 14 days)
period = 14

# Shift the close prices by the period to calculate momentum starting from the (period + 1)-th day
data['Momentum'] = (data['4. close'] - data['4. close'].shift(period)) / data['4. close'].shift(period) * 100

# Print the first few rows of the data to confirm
print(data.head())

# Plot the momentum values
plt.plot(data.index, data['Momentum'], label='Momentum')
plt.xlabel('Date')
plt.ylabel('Momentum')
plt.title('Momentum for {}'.format(symbol))
plt.legend()
plt.show()
