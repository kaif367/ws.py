import websocket
import threading
import json
import time

# Globals
ping_interval = 25  # Default; will be updated from server handshake


def send_ping(ws):
    while True:
        time.sleep(ping_interval)
        try:
            ws.send('2')
            print("🔄 Sent ping")
        except Exception as e:
            print("Ping failed:", e)
            break


def on_open(ws):
    print("WebSocket connection established")


def on_message(ws, message):
    global ping_interval

    try:
        if isinstance(message, bytes):
            message = message.decode('utf-8')

        if message.startswith('0'):
            # Initial handshake
            data = json.loads(message[1:])
            ping_interval = data.get("pingInterval", 25000) / 1000
            print(f"Received handshake. Ping interval: {ping_interval}s")

        elif message == '40':
            print("Connected to socket.io server. Sending subscription...")
            subscribe_msg = '42["subscribe_message", {"msg_type": "subscribe_message", "name": "AUDCHF_otc", "type": "tick"}]'
            ws.send(subscribe_msg)
            print("Subscribed to AUDCHF_otc")
            threading.Thread(target=send_ping, args=(ws,), daemon=True).start()

        elif message == '3':
            print("✅ Received pong")

        elif message.startswith('42'):
            try:
                json_data = json.loads(message[2:])
                event_type, payload = json_data
                if event_type == "tick":
                    print("✅ Tick:", payload)
            except Exception:
                print("⚠️ Unknown 42 message:", message)

        elif message.startswith('451-'):
            print("⚠️ Binary placeholder message (ignored):", message)

        else:
            print("📩 Received message:", message)

    except Exception as e:
        print("❌ Error:", e)


def on_error(ws, error):
    print("❌ WebSocket Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("🔌 Connection closed:", close_status_code, close_msg)


if __name__ == "__main__":
    url = "wss://ws.qxbroker.com/socket.io/?EIO=3&transport=websocket"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://qxbroker.com",
    }

    ws = websocket.WebSocketApp(
        url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    print("📡 Connecting...")
    ws.run_forever()
