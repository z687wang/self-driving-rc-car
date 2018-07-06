import time
import RPi.GPIO as GPIO
import datetime
import json
import math

class SpeedDetectSensor:
    def __init__(self):
        self.ao = 5
        self.do = 12
        self.counter = 0
        self.rpm = 0
        self.kmPerHour = 0
        self.elapse = 0
        self.pulse = 0
        self.startTimer = time.time()
        self.distMeas = 0.00
        self.radius = 10
    
    def initGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.do, GPIO.IN, GPIO.PUD_UP)

    def calculateElapse(self, channel):
        self.pulse += 1
        self.elapse = time.time() - self.startTimer
        start_timer = time.time()
    
    def calculateSpeed(self, r_cm):
        if self.elapse != 0:
            print("good")
            self.rpm = 1 / self.elapse * 60
            circCm = (2 * math.pi)
            distKM = circCm / 100000
            kmPerSec = distKM / self.elapse
            self.kmPerHour = kmPerSec * 3600
            self.distMeas = (distKM * self.pulse) * 1000 / 20
            return self.kmPerHour

    def init_interrupt(self):
        GPIO.add_event_detect(self.do, GPIO.FALLING, callback=self.calculateElapse, bouncetime= 20)
    
    def getSpeed(self):
        self.initGPIO()
        self.init_interrupt()
        speed = self.calculateSpeed(self.radius)
        print(speed)
        GPIO.cleanup()
        return json.dumps({"speed": speed})
    
    def __del__(self):
        GPIO.cleanup()