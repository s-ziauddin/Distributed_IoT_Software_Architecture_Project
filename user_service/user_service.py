import time
import paho.mqtt.client as mqtt
import json
import os
import threading
lock = threading.Lock()
import requests
from database.data_base import Database

global command
## Configuration variables from env.
broker_ip = os.getenv("BROKER_IP", "my-mosquitto-broker")
broker_port = int(os.getenv("BROKER_PORT", "1883"))
device_id = os.getenv("DEVICE_ID_USER_SERVICE", "US")
client_id = os.getenv("CLIENT_ID_USER_SERVICE", "user_01")

api_url = os.getenv("API_URL", "http://api-server:7070/api/v1/iot/inventory/device")
api_user_command_url = os.getenv(
    "API_USER_COMMAND_URL",
    "http://api-server:7070/api/v1/iot/inventory/device/robot/command"
)
# api_url = "http://127.0.0.1:7070/api/v1/iot/inventory/device"
# api_user_command_url = "http://127.0.0.1:7070/api/v1/iot/inventory/device/robot/command"
#default_topic = "device/{}/command".format(device_id)
account_topic_prefix = "/iot/smart_agriculture/"
data_manager_subs_topic = "device/DM1/data"
command_topic = "device/{}/command".format(device_id)
subscribe_topic = account_topic_prefix + data_manager_subs_topic
target_topic = account_topic_prefix + command_topic
message_limit = 1

updated_data_gui = False
updated_data_api = False
command_gui= None
command_api =None
new_data_api =None
new_data_gui= None
robot_data= {}
# in memory storage for user service
db = Database()
api_command_interval = 2.0

def api_user_command():
    global command_api,updated_data_api
    # this function to receive commands send by api user
    try:
        response = requests.get(api_user_command_url,timeout = 2)
        if response.status_code == 200:
            new_data_api = response.json()
            if new_data_api and new_data_api!= command_api:
                command_api = new_data_api
                updated_data_api = True
                return command_api ,updated_data_api
        else:
            updated_data_api =False
    except requests.exceptions.RequestException as e:
        print(f"[user service] Could not connect to API server: {e}")
        updated_data_api = False
    return command_api ,updated_data_api

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the command topic when connected
    client.subscribe(subscribe_topic,qos=1)
    print(f"Subscribed to topic: {subscribe_topic}")

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        robot_id = data.get("Robot_ID")
        db.add_data(robot_id,data)
        robot_data_url = f"{api_url}/{robot_id}/robotdata"
        print(f'[user service] robot data: {robot_id} Sending HTTP POST Request to: {robot_data_url}')
        # sending data to api server
        create_device_response = requests.post(robot_data_url, json=data)
        if create_device_response.status_code == 201:
            print(f"[user service] Robot data sent to api user.")
        else:
            print(f"[user service] Failed to send robot data to api user. Status code: {create_device_response.status_code} Response: {create_device_response.text}")
        print(data)

    except requests.exceptions.RequestException as e:
        print(f"[user service] Could not send data to API server: {e}")
if __name__== "__main__":
    #mqtt_client = mqtt.Client(client_id)
    mqtt_client = mqtt.Client(client_id)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message


    print("Connecting to "+ broker_ip + " port: " + str(broker_port))
    #mqtt_client.connect("localhost", 1883)
    mqtt_client.connect(broker_ip, broker_port)
    
    mqtt_client.loop_start()
    last_time = time.time()
# --- Publish Commands ---
    try:
        while True:
            current_time = time.time()
            # reading user command from api user
            if current_time - last_time >= api_command_interval:
                command_api, updated_data_api = api_user_command()
                print(f"[user servce] command received from api user {command_api}")
                last_time = current_time


            for message_id in range(message_limit):
                if updated_data_api and command_api:
                    payload = command_api
                    payload_string = json.dumps(payload)
                    target_topic = account_topic_prefix + command_topic
                    with lock:
                        infot = mqtt_client.publish(target_topic, payload_string,qos =1)
                        infot.wait_for_publish()
                        print(f"[user service] Message Sent: {message_id} Topic: {target_topic} Payload: {payload_string} sent to data manager")
                    time.sleep(1)
                    updated_data_api = False
    
    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
