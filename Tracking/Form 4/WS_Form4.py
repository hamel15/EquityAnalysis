import websocket
import json
import pandas as pd
from datetime import datetime

# Define the WebSocket URL and your API key
api_key = 'ca463e956b32cb96b919e9af4444456049e47f3ab961bc9fac41c6fe2ed5c1ad'
ws_url = f'wss://stream.sec-api.io?apiKey={api_key}'

# DataFrame to hold the Form 4 filings
form4_data = pd.DataFrame()

def on_message(ws, message):
    data = json.loads(message)
    # Filter for Form 4 filings
    if data.get('formType') == '4':
        print('Form 4 filing received:', data)
        global form4_data
        # Append to the DataFrame
        form4_data = form4_data.append(data, ignore_index=True)

def on_error(ws, error):
    print('Error:', error)

def on_close(ws, close_status_code, close_msg):
    print('### closed ###')
    # Check if DataFrame is not empty
    if not form4_data.empty:
        filename = f'Form_4_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
        form4_data.to_excel(f'C:\\Users\\tdham\\PycharmProjects\\EquityAnalysis\\Tracking\\Form 4\\Results\\{filename}', index=False)
    else:
        print("No Form 4 filings received, no file saved.")


def on_open(ws):
    print('Connection opened')

websocket.enableTrace(True)
ws = websocket.WebSocketApp(ws_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()
