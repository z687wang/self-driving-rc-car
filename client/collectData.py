import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import socket
import time
import os
import threading
from controlWithJoyStick import ControlWithJoyStick

def getAngle(x, y):
    angle = np.arctan2(x, y)
    if (angle <= 0):
        angle = (2 * np.pi + angle)
    return angle * 360 / (2 * np.pi) - 275


class CollectData:
    def __init__(self):
        self.video_server_socket = socket.socket()
        self.video_server_socket.bind(('', 9001))
        self.video_server_socket.listen(0)

        self.video_connection = self.video_server_socket.accept()[0].makefile('rb')
        self.connect_state = True
        self.ctrl = ControlWithJoyStick()
        self.wst = threading.Thread(target=self.ctrl.start)
        self.wst.daemon = True
        self.wst.start()
        self.joystick = pygame.joystick.Joystick(0)
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')
        self.collect_data()


    def collect_data(self):
        self.prev_action = ''
        saved_frame = 0
        total_frame = 0
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 76800))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
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

                    # select lower half of the image
                    roi = image[120:240, :]

                    # save streamed images
                    cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), roi)

                    cv2.imshow('roi_image', roi)
                    # cv2.imshow('image', image)

                    # reshape the roi image into one row array
                    temp_array = roi.reshape(1, 76800).astype(np.float32)

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
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[1]))
                            self.prev_action = self.k[1]
                            saved_frame += 1
                        else:
                            print("CollectData - Turn Left with Angle:", -turnAngle)
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[0]))
                            self.prev_action = self.k[0]
                            saved_frame += 1
                    elif linearKey > 0.001:
                        print("CollectData - Forward")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[2]))
                        self.prev_action = self.k[2]
                        saved_frame += 1

                    elif linearKey < -0.001:
                        print("CollectData - Back")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[3]))
                        self.prev_action = self.k[3]
                        saved_frame += 1

                    elif turnX > 0:
                        print("CollectData - Right")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[1]))
                        self.prev_action = self.k[1]
                        saved_frame += 1

                    elif turnX < 0:
                        print("CollectData - Left")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[0]))
                        self.prev_action = self.k[0]
                        saved_frame += 1

                    elif exitKey > 0:
                        print('CollectData - exit')
                        self.connect_state = False
                        break
                    elif self.prev_action != '':
                        print("CollectData - resume")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.prev_action))
                        saved_frame += 1


            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Streaming duration:', time0)

            print(train.shape)
            print(train_labels.shape)
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)

        finally:
            self.video_server_socket.close()

client = CollectData()