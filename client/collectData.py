import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import socket
import time
import os
from .remoteControl import RemoteControl

class CollectData:
    def __init__(self):
        self.video_server_socket = socket.socket()
        self.video_server_socket.bind(('', 9001))
        self.video_server_socket.listen(0)

        self.video_connection = self.video_server_socket.accept()[0].makefile('rb')
        self.connect_state = True
