# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:09:24 2018

@author: tonyz
"""

import websocket
import threading

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### Connected ###")

class RemoteControl:
    def __init__(self, host, port, tail):
        url = "ws://"+host+":"+port+tail
        print(url)
        self.ws = websocket.WebSocketApp(url,
                                         on_open = on_open,
                                         on_message=on_message,
                                         on_error = on_error,
                                         on_close = on_close)
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()

    def forward(self):
        self.ws.send('forward')

    def backward(self):
        self.ws.send('backward')

    def left(self):
        self.ws.send('left')

    def right(self):
        self.ws.send('right')

    def stop(self):
        self.ws.send('stop')

    def exit(self):
        self.ws.keep_running = False