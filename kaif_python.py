import websocket
import json
import threading
import time

ping_interval = 25  # default fallback
sid = None

def on_message(ws, message):
    global ping_interval
    if message.startswith('0'):
        # Extract pingInterval from socket.io handshake
        try:
            data = json.loads(message[1:])
            ping_interval = data.get("pingInterval", 25000) / 1000
            print(f"Received handshake. Ping interval: {ping_interval}s")
        except:
            print("Handshake parsing failed.")

    elif message == '40':
        print("Connected to socket.io server. Sending subscription...")

        subscribe_msg = '42["subscribe_message", {"msg_type": "subscribe_message", "name": "EURUSD_otc", "type": "tick"}]'
        ws.send(subscribe_msg)
        print("Subscribed to EURUSD_otc")

        # Start ping thread
        threading.Thread(target=send_ping, args=(ws,), daemon=True).start()

    elif message == '3':
        print("Received pong")
    elif message.startswith('42'):
        print("✅ Tick Data:", message)
    else:
        print("Received message:", message)

def send_ping(ws):
    while True:
        time.sleep(ping_interval - 5)  # Send ping before timeout
        try:
            ws.send("2")  # This is the socket.io ping message
            print("🔄 Sent ping")
        except:
            print("❌ Failed to send ping")
            break

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed:", close_status_code, close_msg)

def on_open(ws):
    print("WebSocket connection established")

if __name__ == "__main__":
    websocket.enableTrace(False)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://qxbroker.com",
        "Referer": "https://qxbroker.com",
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
