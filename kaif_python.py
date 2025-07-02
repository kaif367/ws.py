import websocket

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("### Connection closed ###")

def on_open(ws):
    print("Connected to Quotex WebSocket")

def main():
    url = "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket"
    ws = websocket.WebSocketApp(url,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close,
                                 on_open=on_open)
    ws.run_forever()

if __name__ == "__main__":
    main()
