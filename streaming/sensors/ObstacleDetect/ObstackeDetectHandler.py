import time
import tornado.websocket
from tornado.ioloop import PeriodicCallback
import datetime
import json
from ObstacleDetect import ObstacleDetectionSensor

class ObstacleDetectHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
        
    def on_message(self, message):
        if message == "obstacle":
            self.sensor = ObstacleDetectionSensor()
            self.objDetect_loop = PeriodicCallback(self.obj_loop, 1000)
            self.objDetect_loop.start()
        else:
            print("UltraHandler - Unsupported function: " + message)
    
    def obj_loop(self):
        data  = self.sensor.detect()
        try:
            self.write_message(data)
        except tornado.websocket.WebSocketClosedError:
            self.objDetect_loop.stop()
