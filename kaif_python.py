import websocket
import json

# Unique ID of EURUSD_otc — make sure to verify it during runtime
EURUSD_OTC_ID = 71

def on_message(ws, message):
    if message.startswith('42["instrument/update"'):
        try:
            msg_json = json.loads(message[2:])
            data = msg_json[1]
            if data.get("id") == EURUSD_OTC_ID:
                print("Live Price EURUSD_otc:", data["price"])
        except Exception as e:
            print("Error parsing message:", e)

def on_error(ws, error):
    print("WebSocket Error:", error)

def on_close(ws):
    print("WebSocket Closed")

def on_open(ws):
    print("Connected to Quotex WebSocket")
    ws.send('40')  # WebSocket handshake
    ws.send(f'42["instrument/subscribe", {{"id": {EURUSD_OTC_ID}}}]')

def main():
    websocket.enableTrace(False)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    ws = websocket.WebSocketApp(
        "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket",
        header=[f"{key}: {value}" for key, value in headers.items()],
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()

if __name__ == "__main__":
    main()
