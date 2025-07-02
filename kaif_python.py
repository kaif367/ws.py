import websocket

def on_message(ws, message):
    print("Message received:", message)

def on_open(ws):
    print("Connected to Quotex WebSocket")

url = "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket"
ws = websocket.WebSocketApp(url, on_message=on_message)
ws.run_forever()