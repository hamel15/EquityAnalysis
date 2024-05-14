import websocket
import json
import pandas as pd
import threading
from datetime import datetime

# Define the WebSocket URL and your API key
api_key = 'ca463e956b32cb96b919e9af4444456049e47f3ab961bc9fac41c6fe2ed5c1ad'
ws_url = f'wss://stream.sec-api.io?apiKey={api_key}'

# DataFrame to hold the Form 4 filings
form4_data = pd.DataFrame(
    columns=['Date', 'Reporter', 'Company', 'Transaction Type', 'Shares', 'Price Per Share', 'Total Amount'])


def save_data():
    global form4_data
    if not form4_data.empty:
        filename = f'Form_4_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
        filepath = f'C:\\Users\\tdham\\PycharmProjects\\EquityAnalysis\\Tracking\\Form 4\\Results\\{filename}'
        form4_data.to_excel(filepath, index=False)
        print(f"File saved: {filepath}")
        form4_data = pd.DataFrame(
            columns=['Date', 'Reporter', 'Company', 'Transaction Type', 'Shares', 'Price Per Share',
                     'Total Amount'])  # Clear the DataFrame after saving
    else:
        print("No Form 4 filings to save.")


def on_message(ws, message):
    global form4_data
    try:
        data = json.loads(message)
        print("Received data:", data)

        # Check if the data is a list and handle it appropriately
        if isinstance(data, list):
            for item in data:
                if item.get('formType') == '4':
                    extract_and_append_data(item)
        elif isinstance(data, dict) and data.get('formType') == '4':
            extract_and_append_data(data)

        # Check if it's time to save
        if len(form4_data) >= 1:  # Example condition for saving
            save_data()

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except Exception as e:
        print("An error occurred:", e)


def extract_and_append_data(item):
    global form4_data
    transaction_date = item.get('filedAt', 'N/A')
    reporter = item.get('reportingOwner', {}).get('ownerName', 'N/A')
    company = item.get('companyName', 'N/A')
    transaction_type = item.get('transactionCode', 'N/A')
    shares = item.get('transactionAmounts', {}).get('shares', 'N/A')
    price_per_share = item.get('transactionPricePerShare', {}).get('value', 'N/A')
    total_amount = item.get('transactionAmounts', {}).get('totalAmount', 'N/A')

    # Create a DataFrame row
    new_row = {
        'Date': transaction_date,
        'Reporter': reporter,
        'Company': company,
        'Transaction Type': transaction_type,
        'Shares': shares,
        'Price Per Share': price_per_share,
        'Total Amount': total_amount
    }

    form4_data = pd.concat([form4_data, pd.DataFrame([new_row])], ignore_index=True)
    print('Form 4 filing received:', new_row)


def on_error(ws, error):
    print('Error:', error)


def on_close(ws, close_status_code, close_msg):
    print('### closed ###')
    save_data()  # Save any remaining data when the WebSocket closes


def on_open(ws):
    print('Connection opened')
    # Optionally start periodic saving
    # threading.Timer(3600, save_data).start()


websocket.enableTrace(True)
ws = websocket.WebSocketApp(ws_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()
