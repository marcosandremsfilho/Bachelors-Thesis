import paho.mqtt.client as mqtt
import json
from interfaces.communication_interface import CommunicationInterface


class MqttConnection:
    TOPIC_TELEMETRY = "v1/devices/me/telemetry"
    TOPIC_REQUEST = "v1/devices/me/rpc/request/"
    TOPIC_RESPONSE = "v1/devices/me/rpc/response/"
    TOPIC_ATTRIBUTE = "v1/devices/me/attributes"

    def __init__(self, thingsboard_host: str, access_token: str, requests=None) -> None:
        """
        Initialize the MqttConnection with the ThingsBoard host address and device access token.

        Args:
            thingsboard_host: The MQTT broker address.
            access_token: The authentication token for the device.
            requests: Optional dictionary of callable methods to handle incoming requests.
        """
        self.thingsboard_host = thingsboard_host
        self.access_token = access_token
        self.requests = requests

    def configure(self):
        """
        Configures the MQTT client with authentication and connection callbacks.
        """
        self.client = mqtt.Client()

        self.client.on_connect = self._on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.access_token)
        self.client.connect(self.thingsboard_host, 1883, 60)

    def connect(self):
        """
        Starts a background network loop to handle MQTT communication.
        """
        self.client.loop_start()

    def disconnect(self):
        """
        Stops the background network loop.
        """
        self.client.loop_stop()

    def connect_forever(self):
        """
        Starts a blocking network loop to keep the client connected indefinitely.
        """
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        """
        Callback function triggered when a message is received.
        Parses incoming RPC requests and dispatches them accordingly.
        """
        print("Running on message . . .")
        print("Topic: " + msg.topic + "\nMessage: " + str(msg.payload))

        msg_code = msg.topic.replace(self.TOPIC_REQUEST, "")

        data = json.loads(msg.payload.decode("utf-8"))
        print(data)

        call_back_method = data["method"]
        requests_names = self.requests.keys()
        if call_back_method in requests_names:
            ret = self.requests[call_back_method](data)
            self.send_attribute_data(ret)
            self.send_request_data(msg_code, ret)

    def _on_connect(self, client, userdata, rc, *extra_params):
        """
        Callback function triggered upon connection.
        Subscribes to RPC request topics and handles reconnection if necessary.
        """
        self.client.subscribe("v1/devices/me/rpc/request/+")
        if rc["session present"]:
            print("Trying to reconnect . . .")
            self.client.reconnect()
        print(f"Connected with code {rc}")

    def send_telemetry_data(self, device: str, data):
        """
        Publishes telemetry data to the ThingsBoard server.

        Args:
            device: The device identifier.
            data: The data payload to send.
        """
        payload = json.dumps({device: data})
        self.client.publish(self.TOPIC_TELEMETRY, payload)

    def send_attribute_data(self, data):
        """
        Publishes attribute data to the ThingsBoard server.
        """
        payload = json.dumps(data)
        self.client.publish(self.TOPIC_ATTRIBUTE, payload)

    def send_request_data(self, msg_code, data):
        """
        Publishes a response to a previously received RPC request.

        Args:
            msg_code: The request code extracted from the incoming topic.
            data: The response data payload.
        """
        payload = json.dumps(data)
        self.client.publish(self.TOPIC_RESPONSE + msg_code, payload)


class MqttAdapter(CommunicationInterface):
    def __init__(self, mqtt: MqttConnection) -> None:
        """
        Initialize the adapter with an MqttConnection instance.
        """
        self.mqtt = mqtt

    def configure(self):
        """
        Calls the configure method of the underlying MqttConnection instance.
        """
        self.mqtt.configure()

    def connect(self):
        """
        Establishes a persistent MQTT connection using loop_forever.
        """
        self.mqtt.connect()

    def disconnect(self):
        """
        Stops the MQTT client's network loop.
        """
        self.mqtt.disconnect()

    def send(self, data):
        """
        Sends telemetry data through the underlying MqttConnection.

        Args:
            data: A tuple containing the device identifier and the data to send.
        """
        device, device_data = data
        self.mqtt.send_telemetry_data(device, device_data)

    def receive(self):
        """
        Placeholder method for receiving data.
        """
        pass
