import websocket

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("Connected to server")

url = "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket"
ws = websocket.WebSocketApp(url,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            on_open=on_open)

ws.run_forever()
