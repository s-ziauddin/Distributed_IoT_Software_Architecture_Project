from .device import Device

class Sensor(Device):
    def __init__(self,device_id,device_type):
        super().__init__(device_id, device_type)
        self.value = 0
        self.timestamp = None
      
        
    def read_value(self):
        return self.value
