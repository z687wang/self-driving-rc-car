import time
import RPi.GPIO as GPIO
import datetime
import json

class ObstacleDetectionSensor:
    def __init__(self):
        self.left = 8
        self.right = 12
        self.buzzer = 6
        GPIO.setup(self.left, GPIO.IN)
        GPIO.setup(self.right, GPIO.IN)
        GPIO.setup(self.buzzer, GPIO.OUT)
        GPIO.output(self.buzzer, True)

    def detect(self, pin):
        GPIO.setmode(GPIO.BCM)
        if GPIO.input(self.left) and GPIO.input(self.right):
            GPIO.output(self.buzzer, False)
            return json.dumps({"left": True, "right": True})
        elif GPIO.input(self.left):
            GPIO.output(self.buzzer, False)
            return json.dumps({"left": True, "right": False})
        elif GPIO.input(self.right):
            GPIO.output(self.buzzer, False)
            return json.dumps({"left": False, "right": True})
        else:
            return json.dumps({"left": False, "right": False})
    
    def __del__(self):
        GPIO.cleanup()