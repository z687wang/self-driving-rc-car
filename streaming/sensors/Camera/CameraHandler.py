import picamera
import os
import struct
import datetime as dt
import tornado.websocket
import io

class CameraHandler(tornado.websocket.WebSocketHandler):
       
    def streaming(self):
        for img in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port=True):
            try:
                self.write_message(self.stream.read(), binary=True)
            except tornado.websocket.WebSocketClosedError:
                self.camera.stop_recording()
                break
    
    def on_message(self, message):
        if message == "read_camera":
            self.stream = io.BytesIO()
            self.destination = '/home/pi/video'
            self.filename = os.path.join(self.destination, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264'))
            self.camera = picamera.PiCamera()
            self.resolutions = {"high": (1280, 720), "medium": (640, 480), "low": (320, 240)}
            self.camera.resolution = self.resolutions["medium"]

            self.streaming()
        else:
            print("CameraHandler - Unsupported function: " + message)
    