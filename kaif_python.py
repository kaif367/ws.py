import websocket

def on_message(ws, message):
    print("MESSAGE:", message)

def on_error(ws, error):
    print("ERROR:", error)

def on_close(ws, close_status_code, close_msg):
    print("CLOSED:", close_status_code, close_msg)

def on_open(ws):
    print("Connected to Quotex WebSocket")

def main():
    url = "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Origin": "https://qxbroker.com",
        "Referer": "https://qxbroker.com/",
    }

    ws = websocket.WebSocketApp(
        url,
        header=[f"{k}: {v}" for k, v in headers.items()],
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    ws.run_forever()

if __name__ == "__main__":
    main()
