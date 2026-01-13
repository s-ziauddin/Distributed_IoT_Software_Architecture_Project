from .device import Device

class Actuator(Device):
    def __init__(self, device_id,device_type):
        super().__init__(device_id,device_type)
        self.status = None
        self.timestamp = None
        
    def Status(self):
        return (f"Status : {self.status}")
        
