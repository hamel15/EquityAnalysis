from alpha_vantage.timeseries import TimeSeries

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'G99W064UC2NCTP1R'

# Initialize Alpha Vantage API
ts = TimeSeries(key=api_key, output_format='pandas')

# Specify the symbols for which you want to retrieve the data
symbols = ['HIBB', 'BJRI', 'DXLG', 'PAR', 'VRA']

# Get the closing prices for April 18
for symbol in symbols:
    data, meta_data = ts.get_quote_endpoint(symbol=symbol)
    close_price = data['05. price']  # Close price
    print("Close price for {} on April 22: {}".format(symbol, close_price))
