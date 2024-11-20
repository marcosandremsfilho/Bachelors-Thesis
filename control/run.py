from gpio_control import GpioControl
from mqtt_connection import Mqtt

rasp = GpioControl([35])
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

mqtt = Mqtt(THINGSBOARD_HOST, ACCESS_TOKEN, requests)
mqtt.configure()

last_value = None
mqtt.connect()

try:
    while True:
        gpio_state = rasp.get_gpio(35)
        if gpio_state != last_value:
            print("Sending data . . .")
            mqtt.send_telemetry_data("led_ativo", gpio_state)
        last_value = gpio_state
except KeyboardInterrupt:
    mqtt.disconnect()


