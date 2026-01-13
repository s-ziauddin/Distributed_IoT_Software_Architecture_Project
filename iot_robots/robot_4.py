import time
import paho.mqtt.client as mqtt
from model.robot import Robot
import json


# Configuration variables
device_id = "4"
client_id = "clientId0004-Producer"
broker_ip = "172.17.48.99"     # WSL host address
broker_port = 1883
default_topic = "device/{}/robot".format(device_id)
account_topic_prefix = "/iot/smart_agriculture/"
command_topic = "device/DM1/{}".format(device_id)
subscribe_topic = account_topic_prefix + command_topic
message_limit = 1000
WS_thre = 500
FS_thre = 500
user_command = "stop"
def robot_parameter(WS_thre,FS_thre,user_command):
    # creating a robot
    default_WS_thre = WS_thre
    default_FS_thre = FS_thre
    default_user_command = user_command
    robot = Robot(4,500,default_WS_thre,500,default_FS_thre,default_user_command)
    return robot
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    #Subscribe to the command topic when connected
    client.subscribe(subscribe_topic,qos=1)
    print(f"Subscribed to topic: {subscribe_topic}")

def on_message(client, userdata, msg):
    global robot_4 , WS_thre, FS_thre, user_command
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    try:
        command = json.loads(msg.payload.decode())
        # getting user commands.
        if command.get("action") == "start":
            user_command = command.get("action")
            #update robot parameters
            robot_4 = robot_parameter(WS_thre,FS_thre,user_command)
            print("STARTING")
        elif command.get("action") == "stop":
            user_command = command.get("action")
            #update robot parameters
            robot_4 = robot_parameter(WS_thre,FS_thre,user_command)
            print("STOPPED")
        elif command.get("action") == "config":
            WS_thre = command.get("water_spray_thre")
            FS_thre = command.get("ferti_spray_thre")
            print(WS_thre)
            print(FS_thre)
            #update robot parameters
            robot_4 = robot_parameter(WS_thre,FS_thre,user_command)
        else:
            print("Unknown command:", command)
    except Exception as e:
        print("Error processing command:", e)

mqtt_client = mqtt.Client(client_id)
#mqtt_client = mqtt.Client("R01")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Set Account Username & Password
#mqtt_client.username_pw_set(username, password)

print("Connecting to "+ broker_ip + " port: " + str(broker_port))
mqtt_client.connect(broker_ip, broker_port)
#mqtt_client.connect("localhost", 1883)

mqtt_client.loop_start()

# calling a robot
robot_4 = robot_parameter(WS_thre,FS_thre,user_command)

for message_id in range(message_limit):
    
    payload = robot_4.Robot_Status()
    payload_string = json.dumps(payload)
    target_topic = account_topic_prefix + default_topic
    #target_topic = "robot/R01/status"
    infot = mqtt_client.publish(target_topic, payload_string,qos=1)
    infot.wait_for_publish()
    print(f"Message Sent: {message_id} Topic: {target_topic} Payload: {payload_string}")
    time.sleep(5)

mqtt_client.loop_stop()
