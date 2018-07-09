#!/usr/bin/env python
import argparse
import base64
import hashlib
import os
import time
import threading
import webbrowser
import datetime as dt
import RPi.GPIO as GPIO
from sensors.Ultrasonic.UltrasonicHandler import UltrasonicHandler
from sensors.ObstacleDetect.ObstacleDetect import ObstacleDetectionSensor
from sensors.Ultrasonic.Ultrasonic import UltrsonicSensor
from sensors.Temperature.TemperatureHandler import TemperatureHandler
from sensors.Motor.MotorHandler import MotorHandler
from sensors.Camera.CameraHandler import CameraHandler
from sensors.ObstacleDetect.ObstackeDetectHandler import ObstacleDetectHandler
try:
    import cStringIO as io
except ImportError:
    import io

import tornado.web
import tornado.ioloop
import tornado.websocket
from tornado.ioloop import PeriodicCallback

# Hashed password for comparison and a cookie for login cache
ROOT = os.path.normpath(os.path.dirname(__file__))
with open(os.path.join(ROOT, "password.txt")) as in_file:
    PASSWORD = in_file.read().strip()
COOKIE_NAME = "camp"

class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        if args.require_login and not self.get_secure_cookie(COOKIE_NAME):
            self.redirect("/login")
        else:
            self.render("index.html", port=args.port)


class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.send_error(status_code=403)


# class WebSocket(tornado.websocket.WebSocketHandler):

#     def on_message(self, message):
#         """Evaluates the function pointed to by json-rpc."""

#         if message == "read_camera":
#             self.sio = io.StringIO()
#             camera.start_recording(self.sio, format="mjpeg")
#             self.camloop()
#         else:
#             print("Unsupported function: " + message)

#     def camloop(self):
#         """Sends camera images in an infinite loop."""
#         while True:
#             try:
#                 print(self.sio.getvalue())
#                 self.write_message(base64.b64encode(self.sio.getvalue()))
#             except tornado.websocket.WebSocketClosedError:
#                 camera.stop_recording()
#                 break



parser = argparse.ArgumentParser(description="Starts a webserver that "
                                 "connects to a webcam.")
parser.add_argument("--port", type=int, default=8000, help="The "
                    "port on which to serve the website.")
parser.add_argument("--resolution", type=str, default="high", help="The "
                    "video resolution. Can be high, medium, or low.")
parser.add_argument("--require-login", action="store_true", help="Require "
                    "a password to log in to webserver.")
parser.add_argument("--use-usb", action="store_true", help="Use a USB "
                    "webcam instead of the standard Pi camera.")
parser.add_argument("--usb-id", type=int, default=0, help="The "
                     "usb camera number to display")
args = parser.parse_args()

# if args.use_usb:
#     import cv2
#     from PIL import Image
#     camera = cv2.VideoCapture(args.usb_id)
# else:
#     import picamera
#     destination = '/home/pi/video'
#     filename = os.path.join(destination, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264'))
#     camera = picamera.PiCamera()
#     camera.start_preview()

# resolutions = {"high": (1280, 720), "medium": (640, 480), "low": (320, 240)}
# if args.resolution in resolutions:
#     if args.use_usb:
#         w, h = resolutions[args.resolution]
#         camera.set(3, w)
#         camera.set(4, h)
#     else:
#         camera.resolution = resolutions[args.resolution]
#         camera.framerate = 24
# else:
#     raise Exception("%s not in resolution options." % args.resolution)



handlers = [(r"/", IndexHandler),
            (r"/camera", CameraHandler),
            (r"/ultra", UltrasonicHandler),
            (r"/temperature", TemperatureHandler),
            (r"/obstacle", ObstacleDetectHandler),
            (r"/motor", MotorHandler),
            (r"/static/password.txt", ErrorHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': ROOT})]
application = tornado.web.Application(handlers, cookie_secret=PASSWORD)
application.listen(args.port)

webbrowser.open("http://localhost:%d/" % args.port, new=2)

tornado.ioloop.IOLoop.instance().start()
