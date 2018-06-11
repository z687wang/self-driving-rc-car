import tornado.websocket
from tornado.ioloop import PeriodicCallback

from Temperature import TemperatureSensor

class TemperatureHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True 

    def on_message(self, message):
        if message == "temperature":
            self.sensor = TemperatureSensor()
            self.temp_loop = PeriodicCallback(self.temp_loop, 2000)
            self.temp_loop.start()
        else:
            print("TemperatureHandler - Unsupported function: " + message)
    
    def temp_loop(self):
        data  = self.sensor.getTemperature()
        try:
            self.write_message(data)
        except tornado.websocket.WebSocketClosedError:
            self.temp_loop.stop()
