import random
import paho.mqtt.client as mqtt
import json

# Define connection parameters
protocol = "mqtt"
host = "broker.hivemq.com"
port = 1883
client_id = f"ucol_iot_client_{random.randint(10**3, 10**4-1)}"  # More readable random ID generation
topic = "ucol/iot/gabriel"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected!")
        client.subscribe(topic)
    else:
        print(f"Connection error: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Temperatura: {data['temperature']}°C")
        print(f"Humedad: {data['humidity']}%")
        print("-" * 10)
    except json.JSONDecodeError as e:
        print(f"Error parsing message: {e}")

def on_error(client, userdata, exc):
    print(f"Client error: {exc}")

# Create a new MQTT client instance
client = mqtt.Client(client_id)

# Set callbacks for connection, message, and error events
client.on_connect = on_connect
client.on_message = on_message
client.on_error = on_error

# Connect to the MQTT broker
client.connect(host, port)

# Keep the client running in a loop
while True:
    client.loop_start()
