from ObstacleDetect.ObstacleDetect import ObstacleDetectionSensor
from PathTracing.PathTracing import PathTracingSensor
from SpeedDetect.SpeedDetect import SpeedDetectSensor
import time

try:
    speed = SpeedDetectSensor()
    #obs = ObstacleDetectionSensor()
    #path = PathTracingSensor()
    
    while True:
        #path.getTrack()
        #obs.detect()
        speed.getSpeed()
        time.sleep(1)
except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
	1+1
