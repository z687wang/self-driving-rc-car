from Ultrasonic.Ultrasonic import UltrsonicSensor
import time

try:
    ult = UltrsonicSensor()
    while True:
        ult.bottom_right_data()
        time.sleep(0.5)
except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
	1+1
