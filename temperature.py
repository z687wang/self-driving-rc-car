import sys
import Adafruit_DHT
import time
import requests
import json

while True:

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #data = {'humidity':humidity,'temperature':temperature}
    #json_data = json.dumps(data)
    #r = requests.post('http://192.168.0.8:1880/payload',json_data)
    print(humidity,temperature)