import RPi.GPIO as GPIO
import time

sensor = 24
buzzer = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.output(buzzer,False)
print "Initialzing PIR Sensor......"
time.sleep(2)
print "PIR Ready..."
print " "

try: 
   while True:
      if GPIO.input(sensor):
          #GPIO.output(buzzer,True)
          print "Motion Detected"
          time.sleep(0.2)
      else:
          print"Non Detected"
          #GPIO.output(buzzer,False)


except KeyboardInterrupt:
    GPIO.cleanup()
