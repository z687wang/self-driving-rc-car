import websocket
import cv2
import base64
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_open(ws):
        ws.send("read_camera")
   
cap = cv2.VideoCapture()   
def on_message(ws, message):
        print(message.data)
        #ret, frame = cap.read(message.data)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            ws.close()

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


if __name__ == "__main__":
    hostname = "192.168.5.66"
    port = "8000"
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f'ws://{hostname}:{port}/camera',
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()