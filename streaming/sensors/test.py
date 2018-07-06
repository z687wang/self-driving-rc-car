from ObstacleDetect.ObstacleDetect import ObstacleDetectionSensor
from PathTracing.PathTracing import PathTracingSensor
from SpeedDetect.SpeedDetect import SpeedDetectSensor
from Temperature.Temperature import TemperatureSensor
from SpeedDetect.SpeedDetect import SpeedDetectSensor

import time

try:
    #speed = SpeedDetectSensor()
    #obs = ObstacleDetectionSensor()
    #path = PathTracingSensor()
    #temp = TemperatureSensor()
    speed = SpeedDetectSensor()    
    # while True:
    #     #path.getTrack()
    #     #obs.detect()
    #     speed
    #     time.sleep(1)
    speed.getSpeed()
except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
	1+1
