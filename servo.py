from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading


GPIO.setmode(GPIO.BCM)

LED0 = 10
LED1 = 9
LED2 = 25
SER1 = 11#Servo1
SER2 = 8#Servo2
SER3 = 7#Servo3
SER4 = 5#Servo4
SER7 = 6#Vertical servo  port servo7
SER8 = 12#Horizontal servo port se      rvo8


GPIO.setup(SER1,GPIO.OUT)#Servo1
GPIO.setup(SER2,GPIO.OUT)#Servo2
GPIO.setup(SER3,GPIO.OUT)#Servo3
GPIO.setup(SER4,GPIO.OUT)#Servo4
GPIO.setup(SER7,GPIO.OUT)#Horizontal servo port servo7
GPIO.setup(SER8,GPIO.OUT)#Vertical servo port servo8
Servo7=GPIO.PWM(SER7,50) #50HZ
Servo7.start(0)
Servo8=GPIO.PWM(SER8,50) #50HZ
Servo8.start(0)



def SetServo7Angle(angle_from_protocol):
    angle=hex(eval('0x'+angle_from_protocol))
    angle=int(angle,16)
    Servo7.ChangeDutyCycle(2.5 + 10 * angle / 180) #set horizontal servo rotation angle
    GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
    GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
    GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
    time.sleep(0.01)
    GPIO.output(LED0,True)#Headlight's anode to 5V, cathode to IO port
    GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
    GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
def SetServo8Angle(angle_from_protocol):
    angle=hex(eval('0x'+angle_from_protocol))
    angle=int(angle,16)
    Servo8.ChangeDutyCycle(2.5 + 10 * angle / 180) #Set vertical servo rotation angel
    GPIO.output(LED0,False)#Headlight's anode to 5V, cathode to IO port
    GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
    GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
    time.sleep(0.01)
    GPIO.output(LED0,True)#Headlight's anode to 5V, cathode to IO port
    GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
    GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port

SetServo7Angle('0')
