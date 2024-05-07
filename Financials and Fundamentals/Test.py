import websocket
import json

def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error occurred:", error)

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    auth_data = {
        "action": "auth",
        "params": "MaOslbBiDM4Cbv6il5DNiK1bakuOWDj4"
    }
    ws.send(json.dumps(auth_data))

def main():
    # Define the WebSocket endpoint
    ws_endpoint = "wss://socket.polygon.io/stocks"

    # Create a WebSocket connection
    ws = websocket.WebSocketApp(ws_endpoint,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Define the headers
    ws.header = {'Authorization': 'Bearer MaOslbBiDM4Cbv6il5DNiK1bakuOWDj4'}

    # Open the WebSocket connection
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    main()
