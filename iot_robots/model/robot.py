from devices.device import Device
from devices.actuator import Actuator
from devices.sensor import Sensor
from devices.temperature_sensor import Temperature_Sensor
from devices.soil_moisture_sensor import Soil_Moisture_Sensor
from devices.battery_level_sensor import Battery_Level_Sensor
from devices.water_sprinkler import Water_Sprinkler
from devices.water_tank_level_sensor import Water_Tank_Level_Sensor
from devices.fertilizer_tank_level_sensor import Fertilizer_Tank_Level_Sensor
from devices.fertilizer_spray import Fertilizer_Spray
from devices.soil_nutrient_sensor import Soil_Nutrient_Sensor
from devices.gps import GPS
import time
import json

class Robot:
    def __init__(self,robot_id,water_tank_capacity,water_spray_threshold,fertilizer_tank_capacity,fertilizer_spray_threshold,user_command):
        self.robot_id = robot_id
        self.timestamp = time.ctime()
        # create sensors automatically
        self.soil_sensor = Soil_Moisture_Sensor(f"{robot_id}_SMS")
        self.soil_nutrient_sensor = Soil_Nutrient_Sensor(f"{robot_id}_SNS")
        self.battery_sensor = Battery_Level_Sensor(f"{robot_id}_BT_Level")
        self.temperature_sensor = Temperature_Sensor(f"{robot_id}_Temp_sensor")
        self.water_tank_level_sensor = Water_Tank_Level_Sensor(f"{robot_id}_WTLS",water_tank_capacity)
        self.water_sprinkler = Water_Sprinkler(f"{robot_id}_Water_sprinkler",water_spray_threshold)
        self.fertilizer_tank_level_sensor = Fertilizer_Tank_Level_Sensor(f"{robot_id}_FTLS",fertilizer_tank_capacity)
        self.fertilizer_spray = Fertilizer_Spray(f"{robot_id}_fertilizer_spray",fertilizer_spray_threshold)
        self.default_WT_dead_lvl = 0   # initial default dead lvl = 0 means water is above low level
        self.default_FT_dead_lvl = 0   # initial default dead lvl = 0 means chemical is above low level
        self.GPS = GPS(f"{robot_id}_GPS")
        self.user_command = user_command
        

    def Robot_Status(self):
        temp_data =  self.temperature_sensor.read_value()
        SMS_data = self.soil_sensor.read_value()
        SNS_data = self.soil_nutrient_sensor.read_value()
        BT_level = self.battery_sensor.read_value()
        water_spray =  self.water_sprinkler.Status(SMS_data["Soil Moisture is"],self.default_WT_dead_lvl)
        WTLS = self.water_tank_level_sensor.read_value(water_spray["activation_signal"])
        FT_spray = self.fertilizer_spray.Status(SNS_data["Soil Nutrient is"], self.default_FT_dead_lvl)
        FTLS = self.fertilizer_tank_level_sensor.read_value(FT_spray["activation_signal"])
        location = self.GPS.geo_location()
        WT_dead_lvl = WTLS["dead level"]   # reading the low level of water tank in order to stop water spray automatically when low level is reached , regardless of the soil moisture sensor value
        FT_dead_lvl = FTLS["dead level"]
        if WT_dead_lvl == 1:   
            self.default_WT_dead_lvl = WT_dead_lvl
        if FT_dead_lvl == 1:
            self.default_FT_dead_lvl = FT_dead_lvl
        if self.user_command == "start":
            status = "moving"
        elif self.user_command == "stop":
            status = "stop"
        return {
            "Robot_ID" : self.robot_id,
             "Temperature": temp_data,
             "Soil Moisture": SMS_data["Soil Moisture is"],
             "Soil Nutrient": SNS_data["Soil Nutrient is"],
            "Battery Level" : BT_level,
            "Water Level Tank": WTLS["Water_Tank_level"],
            "Water Sprinkler" : water_spray["Water Sprinkler is"],
            "Fertilizer tank level":FTLS["Fertilizer_Tank_level"],
            "Fertilizer spray" : FT_spray["fertilizer spray is"],
            "location": location,
            "status": status,
            "Time" : time.ctime()
            }
       
        
