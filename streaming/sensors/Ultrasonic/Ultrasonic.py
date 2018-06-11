import time
import RPi.GPIO as GPIO
import datetime
import json


class UltrsonicSensor:
    
    def __init__(self):
        GPIO.setwarnings(False)
        self.top_right_echo = 4
        self.top_right_trig = 17
        self.top_left_echo = 18
        self.top_left_trig = 27
        self.bottom_right_echo = 2
        self.bottom_right_trig = 3
        self.bottom_left_echo = 14
        self.bottom_left_trig = 15
        GPIO.setmode(GPIO.BCM)
        

    def measure(self, ECHO, TRIG):
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        start  = time.time()

        while GPIO.input(ECHO) == 0:
            start = time.time()
        
        while GPIO.input(ECHO) == 1:
            stop = time.time()
        
        elapsed = stop - start
        SOUND_SPEED = 343
        MtoCM = 100
        distance = (elapsed * SOUND_SPEED * MtoCM) / 2 
        
        return distance

    def top_right_data(self):
        res = self.measure(self.top_right_echo, self.top_right_trig)
        return json.dumps({ "top_right_distance": res })
    
    def top_left_data(self):
        res = self.measure(self.top_left_echo, self.top_left_trig)
        return json.dumps({ "top_left_distance": res })

    def bottom_left_data(self):
        res = self.measure(self.bottom_left_echo, self.bottom_left_trig)
        return json.dumps({ "bottom_left_distance": res })
    
    def bottom_right_data(self):
        res = self.measure(self.bottom_right_echo, self.bottom_right_trig)
        return json.dumps({ "bottom_right_distance": res })
    
    def all_data(self):
        res1 = self.measure(self.top_right_echo, self.top_right_trig)
        res2 = self.measure(self.top_left_echo, self.top_left_trig)
        res3 = self.measure(self.bottom_left_echo, self.bottom_left_trig)
        res4 = self.measure(self.bottom_right_echo, self.bottom_right_trig)
        print(res1, res2, res3, res4)
        return ({ "top_right_distance": res1, "top_left_distance": res2, "bottom_left_distance": res3, "bottom_right_distance": res4})

    def __del__(self):
        GPIO.cleanup()