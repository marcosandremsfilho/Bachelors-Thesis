from gpio_control import GpioInterface
from interfaces.communication_interface import CommunicationInterface

class GpioCommunicationBridge:
    """Handles communication between MQTT topics and GPIO control."""

    def __init__(self, comm_handler: CommunicationInterface, gpio_obj: GpioInterface) -> None:
        """
        Initializes the controller with MQTT and GPIO handler instances.
        Args:
            comm_handler (CommunicationInterface): An instance responsible for communication.
            gpio_obj (Gpio): An instance responsible for GPIO control.
        """
        self.comm_handler = comm_handler
        self.gpio_obj = gpio_obj

    def detect_pin_change(self, last_gpios_state):
        """
        Compares the current GPIO states with the last known states and detects any changes.
        Args:
            last_gpios_state (dict): Dictionary containing the previous state of GPIO pins.
        Returns:
            tuple:
                - dict: A dictionary with only the pins that changed and their new values.
                - dict: The current full GPIO state dictionary.
        """
        diff = {}

        current_gpios_state = self.gpio_obj.get_gpio()

        if current_gpios_state != last_gpios_state:
            for gpio_state in list(current_gpios_state.keys()):
                if current_gpios_state[gpio_state] != last_gpios_state[gpio_state]:
                    diff[gpio_state] = current_gpios_state[gpio_state]
        return diff, current_gpios_state.copy()

    def track_gpio_and_publish(self):
        """
        Continuously monitors GPIO pins and publishes any detected changes to the MQTT broker.
        """
        last_gpios_state = self.gpio_obj.get_gpio()

        try:
            while True:
                diff, last_gpios_state = self.detect_pin_change(last_gpios_state)
                if diff != {}:
                    for gpio in list(diff.keys()):
                        print("Sending data . . .")
                        self.comm_handler.send((str(gpio), diff[gpio]))
                diff = {}
        except KeyboardInterrupt:
            self.comm_handler.disconnect()

    def run_setup(self):
        """
        Initializes the MQTT connection and starts the GPIO monitoring loop.
        """
        self.comm_handler.configure()
        self.comm_handler.connect()

        self.track_gpio_and_publish()
