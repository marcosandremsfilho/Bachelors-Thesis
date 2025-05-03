from gpio_control import Gpio
from mqtt_connection import MqttAdapter, MqttConnection
from communication_gpio_controller import GpioCommunicationBridge

rasp = Gpio([35])
THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'BrxR1Srk8KjnPu2lBXJq'

def set_gpio_status(data, *args):
    print("Setting GPIO status . . .")
    rasp.set_gpio(data['params']['pin'], data['params']['enabled'])
    return rasp.get_gpio()

def get_gpio_status(*args):
    return rasp.get_gpio()

requests = {
    'setGpioStatus': set_gpio_status,
    'getGpioStatus': get_gpio_status
}

mqtt = MqttAdapter(MqttConnection(THINGSBOARD_HOST, ACCESS_TOKEN, requests))

GpioCommunicationBridge(mqtt, rasp).run_setup()
