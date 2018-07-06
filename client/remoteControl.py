# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:09:24 2018

@author: tonyz
"""

import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import time
import os
import websocket
import _thread

host = '192.168.5.66'
port = '8000'
tail = '/motor'
send = True

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("###connected###")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://"+host+":"+port+tail,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    pygame.init()
    while send:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                key_input = pygame.key.get_pressed()
                # simple orders
                if key_input[pygame.K_UP]:
                    print("Forward")
                    ws.send("forward")
                elif key_input[pygame.K_DOWN]:
                    print("Reverse")
                    ws.send("stop")
                elif key_input[pygame.K_RIGHT]:
                    print("Right")
                    ws.send("right")
                elif key_input[pygame.K_LEFT]:
                    print("Left")
                    ws.send("left")
                elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                    print('exit')
                    send=False
                    break
            elif event.type == pygame.KEYUP:
                    1+1