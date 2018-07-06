# -*- coding: utf-8 -*-

import time
import binascii
import RPi.GPIO as GPIO
from smbus import SMBus
XRservo = SMBus(1)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

time.sleep(2)
XRservo.XiaoRGEEK_SetServo(0x08,90)	
print('ser1= 90')
time.sleep(0.5)
XRservo.XiaoRGEEK_SetServo(0x01,30)	
print('ser1= 30°并存储')
time.sleep(0.1)
XRservo.XiaoRGEEK_SaveServo()
time.sleep(0.5)
XRservo.XiaoRGEEK_SetServo(0x01,90)
print('ser1= 90°')
time.sleep(0.5)
XRservo.XiaoRGEEK_SetServo(0x01,150)
print('ser1= 150°')
time.sleep(1.5)
XRservo.XiaoRGEEK_ReSetServo()
print('恢复存储的角度30°')

'''
整个程序功能为：
	舵机转动到90°
	舵机转动到30°，并存储，
	依次隔0.5s，转动到90°及150°
	隔1.5s后，恢复存储的角度30°
	程序结束
'''