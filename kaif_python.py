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

    # Delay sending until socket.io completes handshake
    def run(*args):
        import time
        time.sleep(1)

        subscribe_msg = '42["subscribe_message", {"msg_type": "subscribe_message", "name": "EURUSD_otc", "type": "tick"}]'
        ws.send(subscribe_msg)
        print("Subscribed to EURUSD_otc")

    import _thread
    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(False)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Origin": "https://qxbroker.com",
        "Referer": "https://qxbroker.com",
        "Cookie": "__cf_bm=Qf4B1EEjPT.iB3XlFdC5WqVFYt71kbdUNj3dhJ2UfX8-1751434744-1.0.1.1-bQ2bkscfkHvuAreqlIYAfssk1NPyAJtLz.p1HSwFUHye20cAOLts.eKyiR6O0Bz58MIGQWD3QMqMxRuBMupmXnB7Xsyjo3zqKKiVtW2lmZQ"
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
