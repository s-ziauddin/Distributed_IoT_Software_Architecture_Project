""" this class is for data managers , in memory database."""
import json
import threading
import time

class Database:
    def __init__(self):
        self.data = {}   
        self.lock = threading.Lock()

    def add_data(self, robot_id, data):
        
        with self.lock:
            self.data[robot_id] = data
           

    def read_data(self, robot_id=None):
        #Read all data or specific robot's data.
        with self.lock:
            if robot_id:
                return json.dumps(self.data.get(robot_id, {}),indent=4)
            return self.data

    def delete_data(self, robot_id):
        #Delete data for a specific robot."""
        with self.lock:
            if robot_id in self.data:
                del self.data[robot_id]

    
