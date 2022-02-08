import json
import os
from paho.mqtt import client as mqtt_client

mqtt_broker = os.environ.get('MQTT_BROKER') 
mqtt_port = int(os.environ.get('MQTT_PORT'))
mqtt_user = os.environ.get('MQTT_USER') 
mqtt_pass = os.environ.get('MQTT_PASS') 
client_id = 'python-mqtt-16101993'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    return client

def lambda_handler(event, context):
    topic = event['queryStringParameters']['topic']
    action = event['queryStringParameters']['action']
    client = connect_mqtt()
    client.loop_start()
    result = client.publish(f"actuators/{topic}", f"{action}")
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{action}` to topic `actuators/{action}`")
    else:
        print(f"Failed to send message to topic {topic}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error in publishing to mqtt broker')
        }
    return {
        'statusCode': 200,
        'body': json.dumps(f'Success')
    }

