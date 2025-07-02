import websocket
import json

EURUSD_OTC_ID = 71  # Replace with actual OTC ID if needed

def on_message(ws, message):
    if message.startswith('42["instrument/update"'):
        try:
            msg_json = json.loads(message[2:])
            data = msg_json[1]
            if data.get("id") == EURUSD_OTC_ID:
                print("EURUSD_otc Price:", data["price"])
        except Exception as e:
            print("Parsing error:", e)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    print("WebSocket connection established")
    ws.send('40')  # handshake
    ws.send(f'42["instrument/subscribe", {{"id": {EURUSD_OTC_ID}}}]')

def main():
    websocket.enableTrace(False)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    ws = websocket.WebSocketApp(
        "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket",
        header=[f"{k}: {v}" for k, v in headers.items()],
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()

if __name__ == "__main__":
    main()
