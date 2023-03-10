# python 3.6

from detected_data import Data
import time
import threading
from paho.mqtt import client as mqtt_client
import json
stop_threading=threading.Event()
broker = 'thingsboard.cloud'
port = 1883
topic = "v1/devices/me/telemetry"

# generate clievint ID with pub prefix randomly
client_id = 'retrovision'
username = 'retrovision'
password = 'retrovision123'
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#get data from detected file
current,voltages,voltages_yellow,segement_top,segement_bot,light_1,light_2,light_3,light_4=Data

def publish(client,loop_trigger):
    if loop_trigger==False:
        stop_threading.set()
    msg_count = 0
    print('status of loop_trigger',loop_trigger)
    while loop_trigger:
        if stop_threading.is_set():
            break
        print('value of loop trigger in loop',loop_trigger)
        time.sleep(1)
        msg = f"messages: {msg_count}"

        payload = json.dumps(Data)
        result = client.publish(topic, payload)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run(loop_trigger):
    client = connect_mqtt()
    publish(client,loop_trigger)


#if __name__ == '__main__':
#   run()
