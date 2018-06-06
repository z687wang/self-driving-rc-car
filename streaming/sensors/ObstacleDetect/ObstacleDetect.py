import time
import RPi.GPIO as GPIO
import datetime
import json

class ObstacleDetectionSensor:
    def __init__(self):
        self.left = 8
        self.right = 12
        self.buzzer = 6
        GPIO.setmode(GPIO.BCM)
        self.setup()

    def setup(self):
        GPIO.setup(self.left, GPIO.IN)
        GPIO.setup(self.right, GPIO.IN)
        GPIO.setup(self.buzzer, GPIO.OUT)
        GPIO.output(self.buzzer, True)

    def detect(self):
        if GPIO.input(self.left) and GPIO.input(self.right):
            GPIO.output(self.buzzer, False)
            #print(True, True)
            return json.dumps({"left": True, "right": True})
        elif GPIO.input(self.left):
            GPIO.output(self.buzzer, False)
            #print(True, False)
            return json.dumps({"left": True, "right": False})
        elif GPIO.input(self.right):
            GPIO.output(self.buzzer, False)
            #print(False, True)
            return json.dumps({"left": False, "right": True})
        else:
            #print(False, False)
            GPIO.output(self.buzzer, True)
            return json.dumps({"left": False, "right": False})
    
    def __del__(self):
        GPIO.cleanup()