from flask_restful import Resource, reqparse
import json
import os
from flask import request, Response
global command_data
command_data = {}

class RobotCommandResource(Resource):
    """HTTP REST resource to send commands to robots"""
    def post(self):  # to receive data from api server
        payload = request.json
        robot_id = payload.get("robot_id")
        command_data[robot_id] = payload
        return {"status": "success"}, 201


    def get(self): # to send data to user service
        if command_data:
            data = list(command_data.keys())[0]
            latest_command = command_data[data]
            command_data.clear()
            return latest_command
        return {"message": "No data found"}, 404
