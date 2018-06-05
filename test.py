from drive import Motor_Backward
from drive import Motor_Forward
from drive import Motor_TurnLeft
from drive import Motor_TurnRight
from drive import Motor_Stop
import time
import sys
while True:#making a loop
    try: 
        str = sys.stdin.read(1)
        if (str == "w"):
            Motor_Forward()
        if (str == "s"):
            Motor_Stop()
        if (str == 'a'):
            Motor_TurnLeft()
        if (str == 'd'):
            Motor_TurnRight()
        if (str == 'q'):
            Motor_Backward()
    except:
        break #if user pressed other than the given key the loop will break