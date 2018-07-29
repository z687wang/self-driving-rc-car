import numpy as np
import websocket
import threading
import json

class UltrasonicSensorClient:

    def ultraSonicHandler(self, ws, message):
        data = json.loads(message)
        self.top_left = data['top_left_distance']
        self.top_right = data['top_right_distance']
        self.bot_left = data['bottom_left_distance']
        self.bot_right = data['bottom_right_distance']
        print(self.top_left, self.top_right, self.bot_left, self.bot_right)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        ws.send("ultra")
        print("### Connected ###")

    def __init__(self, host, port):
        self.bot_right = 0
        self.bot_left = 0
        self.top_right = 0
        self.top_left = 0
        self.ultrasonicUrl = "ws://"+host+":"+port+"/ultra"
        self.ultraClient = websocket.WebSocketApp(self.ultrasonicUrl, on_open = self.on_open,
                                         on_message=self.ultraSonicHandler,
                                         on_error = self.on_error,
                                         on_close = self.on_close)

        self.wst = threading.Thread(target=self.ultraClient.run_forever)
        self.wst.daemon = True
        self.wst.start()


class ObstacleDetectClient:

    def obstacleHandler(self, ws, message):
        data = json.loads(message)
        self.left_obstacle = data['left']
        self.right_obstacle = data['right']

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        ws.send("obstacle")
        print("### Connected ###")

    def __init__(self, host, port):
        self.left_obstacle = False
        self.right_obstacle = False
        self.objDetUrl = "ws://"+host+":"+port+"/obstacle"
        self.obstacleClient = websocket.WebSocketApp(self.objDetUrl, on_open = self.on_open,
                                         on_message=self.obstacleHandler,
                                         on_error = self.on_error,
                                         on_close = self.on_close)

        self.wst = threading.Thread(target=self.obstacleClient.run_forever)
        self.wst.daemon = True
        self.wst.start()







test = UltrasonicSensorClient('192.168.5.66', '8000')
# test = ObstacleDetectClient('192.168.5.66', '8000')
#
# while True:
#     print(test.left_obstacle)
#     print(test.right_obstacle)
#     # print(test.bot_right)
#     # print(test.top_left)