import time
import RPi.GPIO as GPIO
import datetime
import json


class HumanDetectSensor:
    def __init__(self):
        self.sensor = 24
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.sensor, GPIO.IN)
    
    def DetectHuman(self):
        return GPIO.input(self.sensor) == GPIO.LOW

    def getData(self):
        res = self.DetectHuman()
        return json.dumps({"DetectHuman": res})

    def __del__(self):
        GPIO.cleanup()