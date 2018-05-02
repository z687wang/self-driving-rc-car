from socket import *
import RPi.GPIO as GPIO

print "Self-Driving Car Motor Module"

GPIO.setmode(GPIO.BCM)

#Signal pin defination

GPIO.setmode(GPIO.BCM)

#LED port defination
LED0 = 10
LED1 = 9
LED2 = 25

#Morot drive port defination
ENA = 13	#//L298 Enalbe A
ENB = 20	#//L298 Enable B
IN1 = 19	#//Motor port 1
IN2 = 16	#//Motor port 2
IN3 = 21	#//Motor port 3
IN4 = 26	#//Motor port 4

#Servo port defination
SER1 = 11	#Servo1
SER2 = 8	#Servo2
SER3 = 7	#Servo3
SER4 = 5	#Servo4
SER7 = 6	#Vertical servo  port servo7 
SER8 = 12	#Horizontal servo port servo8

#Ultrasonic port defination
ECHO = 4	#Ultrasonic receiving foot position  
TRIG = 17	#Ultrasonic sending foot position

#Infrared sensor port defination
IR_R = 18	#Right line following infrared sensor
IR_L = 27	#Left line following infrared sensor
IR_M = 22	#Middle obstacle avoidance infrared sensor
IRF_R = 23	#Right object tracking infrared sensror
IRF_L = 24	#Left object tracking infrardd sensor
global Cruising_Flag
Cruising_Flag = 0	#//Current circulation mode
global Pre_Cruising_Flag
Pre_Cruising_Flag = 0 	#//Precycling mode
Left_Speed_Hold = 255	#//Define left speed variable
Right_Speed_Hold = 255	#//Define right speed variable

#Pin type setup and initialization

GPIO.setwarnings(False)

#led initialized to 000

GPIO.setup(LED0,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.HIGH)

#motor initialized to LOW

GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

#Servo pin type set

GPIO.setup(SER1,GPIO.OUT)#Servo1
GPIO.setup(SER2,GPIO.OUT)#Servo2
GPIO.setup(SER3,GPIO.OUT)#Servo3
GPIO.setup(SER4,GPIO.OUT)#Servo4
GPIO.setup(SER7,GPIO.OUT)#Horizontal servo port servo7
GPIO.setup(SER8,GPIO.OUT)#Vertical servo port servo8
Servo7=GPIO.PWM(SER7,50) #50HZ
Servo7.start(90)
Servo8=GPIO.PWM(SER8,50) #50HZ
Servo8.start(90)

# Motor Control

def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port


def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,False)#Headlight's anode to 5V, cathode to IO port
	
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port
def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)
	GPIO.output(LED1,True)#Headlight's anode to 5V, cathode to IO port
	GPIO.output(LED2,True)#Headlight's anode to 5V, cathode to IO port

#Servo angle drive function   
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


