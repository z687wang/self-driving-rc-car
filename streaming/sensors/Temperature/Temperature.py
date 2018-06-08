import time  
from w1thermsensor import W1ThermSensor 
import json

class TemperatureSensor:
  def __init__(self):
    self.sensor = W1ThermSensor()

  def getTemperature(self):
    temperature_in_celsius = self.sensor.get_temperature()
    temperature_in_fahrenheit = self.sensor.get_temperature(W1ThermSensor.DEGREES_F)
    temperature_in_all_units = self.sensor.get_temperatures([
        W1ThermSensor.DEGREES_C,
        W1ThermSensor.DEGREES_F,
        W1ThermSensor.KELVIN])
    print(temperature_in_celsius)
    
    return json.dumps(temperature_in_all_units)