import time
import binascii
import RPi.GPIO as GPIO
from smbus import SMBus 
XRservo = SMBus(1)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

time.sleep(2)
XRservo.XiaoRGEEK_SetServo(0x01, 90)
print 'serv1=90'
time.sleep(0.5)
XRservo.XiaoRGEEK_SetServo(0x01, 30)
print 'serv1=30 and save'
time.sleep(0.1)
XRservo.XiaoRGEEK_SetServo()
time.sleep(0.5)
XRservo.XiaoRGEEK_SetServo(0x01, 90)
print 'serv1=90'
time.sleep(0.5)
XRservo.XiaoRGEEK_SetServo(0x01, 150)
print 'serv1=150'
time.sleep(1.5)
XRservo.XiaoRGEEK_SetServo()
print 'set to zero'