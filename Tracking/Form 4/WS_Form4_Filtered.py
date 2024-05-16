import websocket
import json
import pandas as pd
import threading
from datetime import datetime

# Define the WebSocket URL and your API key
api_key = 'ca463e956b32cb96b919e9af4444456049e47f3ab961bc9fac41c6fe2ed5c1ad'
ws_url = f'wss://stream.sec-api.io?apiKey={api_key}'

# List of tickers to filter for
ticker_list = [
    "AMZN", "ANGO", "ARHS", "ARKK", "ARWR", "ASO", "BBW", "BE", "BF/A", "BJRI", "BLMN",
    "BORR", "BOWL", "CAKE", "CAL", "CAR", "CAVA", "CBRL", "CCL", "CDLX", "CHUY", "COLM",
    "CTRN", "CURV", "DBI", "DKS", "DLTR", "DRI", "DXLG", "EAT", "ETD", "EYE", "FL", "FLWS",
    "FND", "FNKO", "FOSL", "FUN", "FWRG", "GIII", "GSHD", "HIBB", "HRMY", "HVT", "IWM",
    "JILL", "KRUS", "KSS", "KTB", "LE", "LOCO", "LOVE", "M", "MTCH", "NU", "ODD", "ONON",
    "OXY", "PAR", "PARA", "PRKS", "PTLO", "QQQ", "RCM", "RRGB", "SCS", "SCVL", "SFIX",
    "SG", "SHAK", "SN", "SNAP", "SONO", "SPY", "SQ", "STKS", "TLYS", "TPR", "TSLA", "TSVT",
    "TTI", "TTSH", "TV", "TWST", "UBER", "UPWK", "VNCE", "VRA", "XPOF", "XRT", "YETI", "ZUMZ", "ZUO"
]

# DataFrame to hold the Form 4 filings
form4_data = pd.DataFrame(
    columns=['Date', 'Reporter', 'Company', 'Ticker', 'Transaction Type', 'Shares', 'Price Per Share', 'Total Amount'])

def save_data():
    global form4_data
    if not form4_data.empty:
        filename = f'Form_4_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
        filepath = f'C:\\Users\\tdham\\PycharmProjects\\EquityAnalysis\\Tracking\\Form 4\\Results\\{filename}'
        form4_data.to_excel(filepath, index=False)
        print(f"File saved: {filepath}")
        form4_data = pd.DataFrame(
            columns=['Date', 'Reporter', 'Company', 'Ticker', 'Transaction Type', 'Shares', 'Price Per Share', 'Total Amount'])
    else:
        print("No Form 4 filings to save.")

def on_message(ws, message):
    global form4_data
    try:
        data = json.loads(message)
        for item in (data if isinstance(data, list) else [data]):
            if item.get('formType') == '4' and item.get('issuer', {}).get('ticker', '') in ticker_list:
                extract_and_append_data(item)

        if len(form4_data) >= 1:
            save_data()

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except Exception as e:
        print("An error occurred:", e)

def extract_and_append_data(item):
    global form4_data
    transaction_date = item.get('filedAt', 'N/A')
    reporter = item.get('reportingOwner', {}).get('ownerName', 'N/A')
    company = item.get('issuer', {}).get('issuerName', 'N/A')
    ticker = item.get('issuer', {}).get('ticker', 'N/A')
    transaction_type = item.get('transactionCode', 'N/A')
    shares = item.get('transactionAmounts', {}).get('shares', 'N/A')
    price_per_share = item.get('transactionPricePerShare', {}).get('value', 'N/A')
    total_amount = item.get('transactionAmounts', {}).get('totalAmount', 'N/A')

    new_row = {
        'Date': transaction_date,
        'Reporter
