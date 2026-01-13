from .sensor import Sensor
import time
import random
import math

# Battery level sensor simulation

class Battery_Level_Sensor(Sensor):
    def __init__(self,device_id):
        super().__init__(device_id , "Battery_Level_sensor")
        self.battery_capacity = 12 
        self.timestamp = time.ctime()
        self.Level = None
        
        
        
        
        
    def read_value(self):
            if self.battery_capacity >= 9:
                self.battery_capacity = self.battery_capacity - 0.00000001
                if self.battery_capacity <= 12 and self.battery_capacity >= 11.5:
                    self.Level = "FULL"
                elif self.battery_capacity <= 11.5 and self.battery_capacity >= 11:
                        self.Level = "HALF"
                elif self.battery_capacity <= 10.5:
                        self.Level = "LOW"
        
            self.timestamp = time.ctime()

            return (self.Level)
                
