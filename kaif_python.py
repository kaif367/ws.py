import websocket
import json

def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed:", close_status_code, close_msg)

def on_open(ws):
    print("WebSocket connection established")

    # Send subscription message for EURUSD_otc
    subscribe_msg = {
        "msg_type": "subscribe_message",
        "name": "EURUSD_otc",
        "type": "tick"
    }
    ws.send(json.dumps(subscribe_msg))

if __name__ == "__main__":
    websocket.enableTrace(True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Origin": "https://qxbroker.com",
        "Referer": "https://qxbroker.com",
        "Cookie": "__cf_bm=YOUR_BROWSER_COOKIE_HERE"
    }

    header_list = [f"{k}: {v}" for k, v in headers.items()]

    ws = websocket.WebSocketApp(
        "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket",
        header=header_list,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()
