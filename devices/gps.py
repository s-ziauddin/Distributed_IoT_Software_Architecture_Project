from .sensor import Sensor
import time
import random
import math



class GPS(Sensor):
    def __init__(self,device_id):
        super().__init__(device_id , "GPS")
        self.latitude = random.uniform(0.0, 10.0)
        self.longitude = random.uniform(0.0,10.0)
        self.altitude = 0.0
        self.timestamp = time.ctime()
        
    def geo_location(self):

       self.latitude = 10.0 + self.latitude
       self.longitude = 40.0 + self.longitude
    
       return{ "latitude" : self.latitude,
                "longitude": self.longitude,
                "altitude": 0.0
                }
                
