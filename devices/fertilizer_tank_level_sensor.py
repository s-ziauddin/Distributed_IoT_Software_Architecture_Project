from .sensor import Sensor
import time
import random
import math

#Fertilizer tank level sensor simulation

class Fertilizer_Tank_Level_Sensor(Sensor):
    def __init__(self,device_id,tank_capacity):
        super().__init__(device_id , "Fertilizer_Tank_Level_sensor")
        self.tank_capacity = tank_capacity
        self.activation_signal = 0
        self.timestamp = time.ctime()
        self.Level = "FULL"
        self.internal_Cal = [self.tank_capacity,self.tank_capacity*0.5,0]
        self.current_value = tank_capacity
        self.dead_level = 0
        
            
        
    def read_value(self,activation_signal):
        # based on activation signal received for water sprinkler it starts to decease its value.
        if  activation_signal == 1 and self.current_value >=0:
            self.current_value = self.current_value - 1
            if self.current_value <= self.internal_Cal[0] and self.current_value > self.internal_Cal[1] :
                self.Level = "FULL"
                self.dead_level = 0
            elif self.current_value <= self.internal_Cal[1] and self.current_value > self.internal_Cal[2]:
                self.Level = "HALF"
                self.dead_level = 0
            elif self.current_value == self.internal_Cal[2]:
                self.Level = "LOW"
                self.dead_level = 1
        
            self.timestamp = time.ctime()

        return {
                "Fertilizer_Tank_level": self.Level,
                "dead level": self.dead_level,
                "tank capacity": round(self.current_value,2)
                }
                
