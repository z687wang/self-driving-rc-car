import RPi.GPIO as GPIO
import time

sensor = 8
sensor_1 = 12
buzzer = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.output(buzzer, True)
print "IR Sensor Ready....."
print " "

try: 
   while True:
      if GPIO.input(sensor):
          GPIO.output(buzzer, False)
          print "Object Detected"
          while GPIO.input(sensor):
              time.sleep(0.2)
      else:
          GPIO.output(buzzer, True)
except KeyboardInterrupt:
    GPIO.cleanup()
