#This at the moment is for demonstration, it have a simple LED and a Fake temp sensor pushing data to HA, where it can be grabbed to put into Flask
import paho.mqtt.client as mqtt
import json
import time
import os

# --- Configuration ---
MQTT_BROKER = "127.0.0.1" #"192.168.50.38" #IP of HA server will need to be updated according
MQTT_USER = "mqtt-user" #Special Username for HA MQTT protocol
MQTT_PASS = "mqtt" #Pass for Special User
TOPIC_SENSOR = "home/pi/sensor" #The [location] / [device] [sensor type], must match the configuration.yaml file in HA
TOPIC_COMMAND = "home/pi/led/set"

#TO SAVE LOCAL TO LOCAL JSON FILE FOR TESTING
DATA_FILE = "sensor_data.json"

# --- Callbacks ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully to Broker!")
        client.subscribe(TOPIC_COMMAND)
    else:
        print(f"Failed to connect. Code: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received command from HA: {payload}")
    if payload == "ON":
        print("LED ON")
    elif payload == "OFF":
        print("LED OFF")

# --- Setup ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # Use CallbackAPIVersion.VERSION2 for py version 3.13
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

# Tries to connect if the broker is offline for a min rather than crashing. 
client.reconnect_delay_set(min_delay=1, max_delay=30)
print(f"Attempting to connect to {MQTT_BROKER}...")

try:
    print(f"Connecting to {MQTT_BROKER}...")
    client.connect(MQTT_BROKER, 1883, 60) 
except Exception as e:
    print(f"Broker not found at {MQTT_BROKER}. OFFLINE MODE! TRYING TO RECONNECT")

# starts loop even if it failed it will auto retry. 
client.loop_start()

try:
    while True:
        fake_temp = 70.5 
        client.publish(TOPIC_SENSOR, json.dumps({"temperature": fake_temp}), retain=True)

        #TESTING PUSHS TO JSON FILE
        with open(DATA_FILE, "w") as f:
            json.dump({"temperature": fake_temp}, f)

        print(f"Sent: {fake_temp}°F")
        time.sleep(10)
except KeyboardInterrupt:
    #CLEANUP
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    print("Shutting down...")
    client.disconnect()
