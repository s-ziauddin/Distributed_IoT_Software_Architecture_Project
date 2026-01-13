from flask_restful import Resource
from flask import jsonify
import json
import os
from flask import request, Response
# in memory storage
robot_data = {}

class RobotDataResource(Resource):
    #HTTP REST resource to serve robot data.
    def post(self,robot_id):  # to receive data from user service
        payload = request.json
        robot_data[robot_id] = payload
        return {"status": "success"}, 201

    def get(self, robot_id): # to send data to api user
        data = robot_data.get(robot_id)
        if data:
            return data
        return {"message": "No data found"}, 404
