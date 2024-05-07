from alpha_vantage.timeseries import TimeSeries
import numpy as np

# Alpha Vantage API key
api_key = 'G99W064UC2NCTP1R'

# Ticker symbol of the stock
symbol = 'AAPL'

# Initialize Alpha Vantage TimeSeries object
ts = TimeSeries(key=api_key, output_format='pandas')

# Get historical stock data
data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')

# Extract adjusted close prices
prices = data['4. close'].values

# Create an array of indices as the independent variable (e.g., time)
X = np.arange(len(prices)).reshape(-1, 1)

# Perform linear regression
coefficients = np.polyfit(X.flatten(), prices, 1)

# Print the regression coefficients
print("Regression Coefficients (slope, intercept):", coefficients)
