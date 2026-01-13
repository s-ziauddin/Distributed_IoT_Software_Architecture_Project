from .sensor import Sensor
import time
import random
import math

unit = "C"

class Temperature_Sensor(Sensor):
    def __init__(self,device_id):
        super().__init__(device_id , "Temperature_sensor")
        self.value = random.uniform(10, 25)
        self.Unit = unit
        self.timestamp = time.ctime()
        
    def read_value(self):
        if self.value >=10 and self.value <=25:
            self.value += random.uniform(-0.1, 0.1)

##        if temp >=10 and temp < 20:
##            self.value = self.value + 0.5
##        elif temp >=20:
##              self.value = self.value - 0.5

        # Set the timestamp of the last measurement in milliseconds
        self.timestamp = time.ctime()
        
        

        return (f'{round(self.value,2)}{self.Unit}')
