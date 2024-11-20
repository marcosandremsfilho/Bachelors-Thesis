import paho.mqtt.client as mqtt
import json

class Mqtt:
    TOPIC_TELEMETRY = "v1/devices/me/telemetry"
    TOPIC_REQUEST = "v1/devices/me/rpc/request/"
    TOPIC_RESPONSE = "v1/devices/me/rpc/response/"
    TOPIC_ATTRIBUTE = "v1/devices/me/attributes"
    
    def __init__(self, thingsboard_host: str, access_token: str, requests = None) -> None:
        self.thingsboard_host = thingsboard_host
        self.access_token = access_token
        self.requests = requests

    def configure(self):
        self.client = mqtt.Client()

        self.client.on_connect = self._on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.access_token)
        self.client.connect(self.thingsboard_host, 1883, 60)

    def connect(self):
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
    
    def connect_forever(self):
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        print("Running on message . . .")
        print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))

        msg_code = msg.topic.replace(self.TOPIC_REQUEST, "")

        data = json.loads(msg.payload.decode("utf-8"))
        print(data)

        call_back_method = data['method']
        requests_names = self.requests.keys()
        if call_back_method in requests_names:
            ret = self.requests[call_back_method](data)
            self.send_attribute_data(ret)
            self.send_request_data(msg_code, ret)
        
    def _on_connect(self, client, userdata, rc, *extra_params):
        self.client.subscribe('v1/devices/me/rpc/request/+')
        if rc["session present"]:
            print("Trying to reconnect . . .")
            self.client.reconnect()
        print(f"Connected with code {rc}")

    def send_telemetry_data(self, device: str, data):
        payload = json.dumps({device: data})
        self.client.publish(self.TOPIC_TELEMETRY, payload)

    def send_attribute_data(self, data):
        payload = json.dumps(data)
        self.client.publish(self.TOPIC_ATTRIBUTE, payload)

    def send_request_data(self, msg_code, data):
        payload = json.dumps(data)
        self.client.publish(self.TOPIC_RESPONSE + msg_code, payload)

