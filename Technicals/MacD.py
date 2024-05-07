import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to fetch historical price data
def fetch_price_data(symbol, api_key):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2020-01-01/2024-05-05?unadjusted=true&sort=asc&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df.set_index('t', inplace=True)
    return df

# Function to calculate MACD
def calculate_macd(df):
    df['12ema'] = df['c'].ewm(span=12, min_periods=12).mean()
    df['26ema'] = df['c'].ewm(span=26, min_periods=26).mean()
    df['MACD'] = df['12ema'] - df['26ema']
    df['Signal Line'] = df['MACD'].ewm(span=9, min_periods=9).mean()
    return df

# Function to calculate Slow Stochastic
def calculate_slow_stochastic(df):
    df['Lowest Low'] = df['l'].rolling(14).min()
    df['Highest High'] = df['h'].rolling(14).max()
    df['%K'] = (df['c'] - df['Lowest Low']) / (df['Highest High'] - df['Lowest Low']) * 100
    df['%D'] = df['%K'].rolling(3).mean()
    return df

# Function to calculate RSI
def calculate_rsi(df):
    delta = df['c'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi
    return df

# Function to plot indicators
def plot_indicators(df, symbol):
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8), sharex=True)

    # MACD plot
    df[['MACD', 'Signal Line']].tail(14).plot(ax=axes[0])
    axes[0].set_title(f'MACD for {symbol}')
    axes[0].set_xlim(df.index[-14], df.index[-1])  # Limit x-axis to last 14 periods

    # Slow Stochastic plot
    df[['%K', '%D']].tail(14).plot(ax=axes[1])
    axes[1].set_title(f'Slow Stochastic for {symbol}')
    axes[1].set_xlim(df.index[-14], df.index[-1])  # Limit x-axis to last 14 periods

    # RSI plot
    df['RSI'].tail(14).plot(ax=axes[2])
    axes[2].set_title(f'RSI for {symbol}')
    axes[2].set_xlim(df.index[-14], df.index[-1])  # Limit x-axis to last 14 periods

    plt.tight_layout()
    plt.show()

# Main function
def main():
    # Polygon API key
    api_key = 'MaOslbBiDM4Cbv6il5DNiK1bakuOWDj4'

    # Symbol
    symbol = 'ODD'

    # Fetch historical price data
    df = fetch_price_data(symbol, api_key)

    # Calculate indicators
    df = calculate_macd(df)
    df = calculate_slow_stochastic(df)
    df = calculate_rsi(df)

    # Plot indicators
    plot_indicators(df, symbol)

if __name__ == "__main__":
    main()
