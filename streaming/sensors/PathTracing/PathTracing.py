import time
import RPi.GPIO as GPIO
import datetime
import json

class PathTracingSensor:
    def __init__(self):
        self.track = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.track, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def trackPath(self):
        return GPIO.input(self.track) == GPIO.LOW

    def getTrack(self):
        res = self.trackPath()
        return json.dumps({"onTrack": res})
    
    def __del__(self):
        GPIO.cleanup()