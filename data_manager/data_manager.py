import time
import paho.mqtt.client as mqtt
import json
import threading
from database.data_base import Database
import os

### Configuration variables
broker_ip = os.getenv("BROKER_IP", "my-mosquitto-broker")
broker_port = int(os.getenv("BROKER_PORT", "1883"))
device_id = os.getenv("DEVICE_ID_DATA_MANAGER", "DM1")
client_id = os.getenv("CLIENT_ID_DATA_MANAGER", "DM")

Robot_subs_topic = "device/+/robot"
user_subs_topic = "device/US/command"
account_topic_prefix = "/iot/smart_agriculture/"
Robot_subscribe_topic = account_topic_prefix + Robot_subs_topic
User_subscribe_topic = account_topic_prefix + user_subs_topic
message_limit = 1
global  Data ,Updated_data ,robot_1_data ,robot_2_data ,target_topic ,QoS_level
Data = None
new_data = None
updated_data = False
QoS_level = 0

lock = threading.Lock()
# in memory storage for data manager
db = Database()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):

    print("Connected with result code " + str(rc))
    # Subscribe to the command topic when connected
    client.subscribe(Robot_subscribe_topic,qos=1)
    print(f"Subscribed to topic: {Robot_subscribe_topic}")
    client.subscribe(User_subscribe_topic,qos=2)
    print(f"Subscribed to topic: {User_subscribe_topic}")

def on_message(client, userdata, msg):
    global Data ,updated_data ,target_topic ,QoS_level
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    try:
        topic = msg.topic
        print(topic)
        new_data = json.loads(msg.payload.decode())
        robot_id = new_data.get("Robot_ID")

        if  topic == f"/iot/smart_agriculture/device/{robot_id}/robot":
            # check if new data is received
            if new_data and new_data != Data:
                Data = new_data
                updated_data = True
                db.add_data(robot_id,Data)
                target_topic =f"/iot/smart_agriculture/device/{device_id}/data"
                QoS_level = 1

        if topic == "/iot/smart_agriculture/device/US/command":
            new_data = json.loads(msg.payload.decode())
            robot_id = new_data.get("robot_id")
            if new_data and new_data !=Data:
                    Data= new_data
                    target_topic = f"/iot/smart_agriculture/device/DM1/{robot_id}"
                    updated_data = True
                    QoS_level = 2
    except Exception as e:
        print("Error processing command:", e)

if __name__ == "__main__":
#mqtt_client = mqtt.Client(client_id)
    mqtt_client = mqtt.Client(client_id)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message


    print("Connecting to "+ broker_ip + " port: " + str(broker_port))
    #mqtt_client.connect("localhost", 1883)
    mqtt_client.connect(broker_ip, broker_port)
    
    mqtt_client.loop_start()

# --- Publish Commands ---
    try:
      while True:
        # calling the function to read data received from user connected to api server
        if Data and updated_data:
            for message_id in range(message_limit):
                payload = Data
                payload_string = json.dumps(payload)
                infot = mqtt_client.publish(target_topic, payload_string,QoS_level)
                infot.wait_for_publish()
                print(f"Message Sent: {message_id} Topic: {target_topic} Payload: {payload_string}")
                updated_data = False
                QoS_level = 0
                time.sleep(1)



    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

