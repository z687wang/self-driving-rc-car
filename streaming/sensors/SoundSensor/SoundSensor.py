import time
import RPi.GPIO as GPIO
import datetime
import json
import math

class SoundSensor:
    def __init__(self):
        self.do = 3
        self.ao = 4