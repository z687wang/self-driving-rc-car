import tornado.websocket
from tornado.ioloop import PeriodicCallback

from Ultrasonic import UltrsonicSensor

class UltrasonicHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
        
    def on_message(self, message):
        if message == "ultra":
            self.sensor = UltrsonicSensor()
            self.ultra_loop = PeriodicCallback(self.ultra_loop, 1000)
            self.ultra_loop.start()
        else:
            print("UltraHandler - Unsupported function: " + message)
    
    def ultra_loop(self):
        data  = self.sensor.all_data()
        try:
            self.write_message(data)
        except tornado.websocket.WebSocketClosedError:
            self.ultra_loop.stop()
