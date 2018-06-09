import time
import RPi.GPIO as GPIO
import datetime
import json


class Motor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.ENA = 13
        self.ENB = 20
        self.IN1 = 19
        self.IN2 = 16
        self.IN3 = 21
        self.IN4 = 26
        self.IR_R = 18
        self.IR_L = 27
        GPIO.setup(self.ENA,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN1,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN2,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.ENB,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN3,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN4,GPIO.OUT,initial=GPIO.LOW)
    
    def Motor_Backward(self):
        print('motor backward')
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, True)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, True)
        GPIO.output(self.IN4, False)

    def Motor_Forward(self):
        print('motor_forward')
        GPIO.output(self.ENA,True)
        GPIO.output(self.ENB,True)
        GPIO.output(self.IN1,False)
        GPIO.output(self.IN2,True)
        GPIO.output(self.IN3,False)
        GPIO.output(self.IN4,True)

    def Motor_TurnRight(self):
        print('motor_turnright')
        GPIO.output(self.ENA,True)
        GPIO.output(self.ENB,True)
        GPIO.output(self.IN1,True)
        GPIO.output(self.IN2,False)
        GPIO.output(self.IN3,False)
        GPIO.output(self.IN4,True)

    def Motor_TurnLeft(self):
        print('motor_turnleft')
        GPIO.output(self.ENA,True)
        GPIO.output(self.ENB,True)
        GPIO.output(self.IN1,False)
        GPIO.output(self.IN2,True)
        GPIO.output(self.IN3,True)
        GPIO.output(self.IN4,False)

    def Motor_Stop(self):
        print('motor_stop')
        GPIO.output(self.ENA,False)
        GPIO.output(self.ENB,False)
        GPIO.output(self.IN1,False)
        GPIO.output(self.IN2,False)
        GPIO.output(self.IN3,False)
        GPIO.output(self.IN4,False)

    def Control(message) {
        if message == 'Forward':
            self.Motor_Forward()
        elif message == 'Stop':
            self.Motor_Stop()
        elif message == 'Backward':
            self.Motor_Backward()
        elif message == 'Right':
            self.Motor_TurnRight()
            time.sleep(0.1)
            self.Motor_Stop()
        elif message == 'Left':
            self.Motor_TurnLeft()
            self.Motor_Stop()
    } 