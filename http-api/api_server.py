from flask import Flask
from flask_restful import Api
from Resource.robot_data_resource import RobotDataResource
from Resource.robot_command_resource import RobotCommandResource
import yaml
import os

# --- Create Flask app and register resources ---
def create_app():
    # api_prefix = "/api/v1/iot/inventory"
    # host = "0.0.0.0"
    # port = "7070"
    api_prefix = os.getenv("API_PREFIX", "/api/v1/iot/inventory")
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "7070"))
    app = Flask(__name__)
    api = Api(app)

   

    api.add_resource(
        RobotDataResource,
        f"{api_prefix}/device/<int:robot_id>/robotdata",
        endpoint="device_robot_data",
        methods=["GET" ,"POST"]
    )
    api.add_resource(
        RobotCommandResource,
        f"{api_prefix}/device/robot/command",
        endpoint="device_command",
        methods=["GET","POST"]
    )

    return app, host,port

# --- Run server ---
if __name__ == "__main__":
    app,host,port = create_app()
    print(f"🚀 Starting Flask REST API at{host}:{port}")
    app.run(host=host, port=port)
