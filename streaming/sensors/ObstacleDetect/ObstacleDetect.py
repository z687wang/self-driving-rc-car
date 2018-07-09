import time
import RPi.GPIO as GPIO
import datetime
import json

class ObstacleDetectionSensor:
    def __init__(self):
        self.left = 9
        self.right = 25 
        GPIO.setmode(GPIO.BCM)
        self.setup()

    def setup(self):
        GPIO.setup(self.left, GPIO.IN)
        GPIO.setup(self.right, GPIO.IN)

    def detect(self):
        if GPIO.input(self.left) and GPIO.input(self.right):
            #print(True, True)
            return json.dumps({"left": True, "right": True})
        elif GPIO.input(self.left):
            #print(True, False)
            return json.dumps({"left": True, "right": False})
        elif GPIO.input(self.right):
            #print(False, True)
            return json.dumps({"left": False, "right": True})
        else:
            #print(False, False)
            return json.dumps({"left": False, "right": False})
    
    def __del__(self):
        GPIO.cleanup()