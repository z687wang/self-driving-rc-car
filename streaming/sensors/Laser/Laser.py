import time
import RPi.GPIO as GPIO
import datetime
import json


class Lazer:
    def __init__(self):
        self.lazer = 23
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.lazer, GPIO.OUT)
        GPIO.output(self.lazer, GPIO.HIGH)

    def pause(self):
        GPIO.output(self.lazer, GPIO.LOW)