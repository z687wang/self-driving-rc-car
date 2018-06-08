import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
pin=24
GPIO.setup(pin, GPIO.IN)         #Read output from PIR motion sensor
while True:
    i=GPIO.input(pin)
    if i==0:                 #When output from motion sensor is LOW
        print "No intruders",i
        time.sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print "Intruder detected",i
    time.sleep(0.1)