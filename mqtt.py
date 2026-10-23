import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.connect(HOST, PORT)
        self.client.loop_start()

    def publish(self, topic, payload):
        self.client.publish(topic, payload)
        print("Published")

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

