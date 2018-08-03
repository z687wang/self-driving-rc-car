import numpy as np
import cv2
import pygame
import socket
import threading
from controlWithJoyStick import ControlWithJoyStick
from SensorClient import UltrasonicSensorClient
from writeToCSV import CSVWriter
from enum import Enum
import argparse
import datetime

class Move(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'left'
    RIGHT = 'right'
    STOP = 'stop'

def getAngle(x, y):
    angle = np.arctan2(x, y)
    if (angle <= 0):
        angle = (2 * np.pi + angle)
    return angle * 360 / (2 * np.pi) - 275


class CollectData:
    def __init__(self, ipAdress, videoPort, sensorPort, csvPath, dataPath):
        self.video_server_socket = socket.socket()
        self.video_server_socket.bind(('', int(videoPort)))
        self.video_server_socket.listen(0)
        self.csvPath = csvPath
        self.dataPath = dataPath

        self.video_connection = self.video_server_socket.accept()[0].makefile('rb')
        self.connect_state = True
        self.csvClient = CSVWriter(csvPath)
        self.ctrl = ControlWithJoyStick(ipAdress, sensorPort)
        self.wst = threading.Thread(target=self.ctrl.start)
        self.wst.daemon = True
        self.wst.start()
        self.ultClient = UltrasonicSensorClient(ipAdress, sensorPort)
        self.joystick = pygame.joystick.Joystick(0)
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')
        self.collect_data()


    def collect_data(self):
        self.prev_action = Move.STOP
        saved_frame = 0
        total_frame = 0
        e1 = cv2.getTickCount()
        image_array = []
        label_array = []
        ult_array = []

        try:
            stream_bytes = b" "
            frame = 1
            while self.connect_state:
                data = self.video_connection.read(1024)
                stream_bytes += data
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    # save streamed images
                    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    framePostfix = '{:>05}.jpg'.format(frame)
                    imgPath = self.dataPath + now + framePostfix
                    cv2.imwrite(imgPath, image)
                    image_array.append(imgPath)

                    # cv2.imshow('training mode', image)

                    ult = { 'top_left': self.ultClient.top_left,
                            'top_right': self.ultClient.top_right,
                            'bot_left': self.ultClient.bot_left,
                            'bot_right': self.ultClient.bot_right }
                    ult_array.append(ult)

                    frame += 1
                    total_frame += 1
                    # -------- Get Control Bit ------------
                    linearKey = self.joystick.get_axis(2)
                    stopKey = self.joystick.get_button(0)
                    exitKey = self.joystick.get_button(1)
                    axisX = self.joystick.get_axis(0)
                    axisY = self.joystick.get_axis(1)
                    turnAngle = getAngle(axisX, axisY)
                    turnX, turnY = self.joystick.get_hat(0)

                    if (abs(axisX) > 0.001 and abs(axisY) > 0.001):
                        if (abs(turnAngle) > 90):
                            print("CollectData - Turn Right with Angle:", turnAngle)
                            label_array.append(Move.RIGHT)
                            self.prev_action = Move.RIGHT
                            saved_frame += 1
                        else:
                            print("CollectData - Turn Left with Angle:", -turnAngle)
                            label_array.append(Move.LEFT)
                            self.prev_action = Move.LEFT
                            saved_frame += 1
                    elif linearKey > 0.001:
                        print("CollectData - Forward")
                        label_array.append(Move.FORWARD)
                        self.prev_action = Move.FORWARD
                        saved_frame += 1

                    elif linearKey < -0.001:
                        print("CollectData - Back")
                        label_array.append(Move.BACKWARD)
                        self.prev_action = Move.BACKWARD
                        saved_frame += 1

                    elif turnX > 0:
                        print("CollectData - Right")
                        label_array.append(Move.RIGHT)
                        self.prev_action = Move.RIGHT
                        saved_frame += 1

                    elif turnX < 0:
                        print("CollectData - Left")
                        label_array.append(Move.LEFT)
                        self.prev_action = Move.LEFT
                        saved_frame += 1

                    elif exitKey > 0:
                        print('CollectData - exit')
                        self.connect_state = False
                        break
                    elif self.prev_action != '':
                        # print("CollectData - resume")
                        label_array.append(self.prev_action)
                        saved_frame += 1

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Streaming duration:', time0)
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)
            for image_path, ult_data, label in zip(image_array, ult_array, label_array):
                 self.csvClient.writeToCSV({'img': imgPath, 'topLeftDistance': ult_data['top_left'],
                                           'topRightDistance': ult_data['top_right'],
                                           'botLeftDistance': ult_data['bot_left'],
                                           'botRightDistance': ult_data['bot_right'],
                                           'move': label})

        finally:
            self.video_server_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start collecting training data')
    parser.add_argument('-i', '--ipAdress', required=False, help="ip adress of rc car", default='192.168.5.66')
    parser.add_argument('-v', '--videoPort', required=False, help="port for video streaming", default='9001')
    parser.add_argument('-p', '--sensorPort', required=False, help="port for sensor streaming", default='8000')
    parser.add_argument('-c', '--csvPath', required=False, help="path for csvfile", default='./train_data.csv')
    parser.add_argument('-d', '--dataPath', required=False, help="path for traning data", default='./training_data/')
    args = parser.parse_args()
    print(args)
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S%f")
    print(now)
    client = CollectData(args.ipAdress, args.videoPort, args.sensorPort, args.csvPath, args.dataPath)