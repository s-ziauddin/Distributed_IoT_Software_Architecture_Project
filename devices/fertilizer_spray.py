from .actuator import Actuator
import time
import random

OFF = "OFF"
ON = "ON"

# Fertilizer Spray turns on depending on the value of 
class Fertilizer_Spray(Actuator):
    def __init__(self,device_id, threshold):               
        super().__init__(device_id,"Water_Sprinkler")
        self.Output = OFF
        self.timestamp = time.ctime()
        self.threshold = threshold
        self.sensor_val = 0
        self.activation_signal = 0
    
       
        

    def Status(self,sensor_val ,dead_level):
        if sensor_val > self.threshold and dead_level == 0:
            self.Output = ON
            self.activation_signal = 1
        else:
            self.Output = OFF
            self.activation_signal = 0

        return{
            "fertilizer spray is": self.Output,
            "activation_signal": self.activation_signal
            }
        
        
