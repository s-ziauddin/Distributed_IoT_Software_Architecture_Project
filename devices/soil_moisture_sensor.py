from .sensor import Sensor
import time
import random
import math



class Soil_Moisture_Sensor(Sensor):
    def __init__(self,device_id):
        super().__init__(device_id , "Soil_Moisture_sensor")
        self.value = random.uniform(400,800)
        self.timestamp = time.ctime()
        
    def read_value(self):
        if self.value >= 400 and self.value <=800:
            self.value += random.uniform(-1, 1)

##        if temp >=10 and temp < 20:
##            self.value = self.value + 0.5
##        elif temp >=20:
##              self.value = self.value - 0.5

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = time.ctime()
        
        

        return {
                "Soil Moisture is": round(self.value,2)
                }
                
