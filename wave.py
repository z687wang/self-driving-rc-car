from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading

ECHO = 4
TRIG = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)#ultrasonic module transmitting end pin set trig
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP)#ultrasonic module receiving end pin set echo

def	Get_Distance():
	time.sleep(0.1)
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
				pass
	t1 = time.time()
	while GPIO.input(ECHO):
				pass
	t2 = time.time()
	time.sleep(0.1)
	return (t2-t1)*340/2

DST = Get_Distance()
print(DST)
