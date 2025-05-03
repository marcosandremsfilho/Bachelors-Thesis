from abc import abstractmethod
import RPi.GPIO as GPIO


class GpioInterface:
    @abstractmethod
    def _update_status(self, actual_pin=None, state=None):
        pass

    @abstractmethod
    def _configure_pins(self):
        pass

    @abstractmethod
    def detect_pin_change(self):
        pass

    @abstractmethod
    def set_gpio(self, pin, state):
        pass

    @abstractmethod
    def get_gpio(self, pin=None):
        pass


class Gpio(GpioInterface):
    GPIO_STATE = {
        7: False,
        11: False,
        12: False,
        13: False,
        15: False,
        16: False,
        18: False,
        22: False,
        29: False,
        31: False,
        32: False,
        33: False,
        35: False,
        36: False,
        37: False,
        38: False,
        40: False,
    }

    def __init__(self, input_gpios: list = []) -> None:
        self.input_gpios = input_gpios

        self._configure_pins()

    def _update_status(self, actual_pin=None, state=None):
        """
        Update the GPIO_STATE dictionary to reflect the current state of the pins.
            - If 'actual_pin' and 'state' are provided, update only that pin (used during write operations).
            - Otherwise, read all input pins and update their current states.
        """
        for pin in self.GPIO_STATE:
            if pin in self.input_gpios:
                self.GPIO_STATE[pin] = True if GPIO.input(pin) else False
        if actual_pin is not None:
            self.GPIO_STATE[actual_pin] = state

    def _configure_pins(self):
        """
        Configure the GPIO pins on the Raspberry Pi.
            - Input pins (from 'self.input_gpios') are set with pull-down resistors.
            - All other pins are configured as output.
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        for pin in self.GPIO_STATE:
            if pin in self.input_gpios:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                GPIO.setup(pin, GPIO.OUT)

    def set_gpio(self, pin, state):
        """
        Set the given GPIO pin to HIGH or LOW.
        Args:
            pin (int): GPIO pin number.
            state (bool): Desired state (True for HIGH, False for LOW).
        """
        GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
        self._update_status(pin, state)

    def get_gpio(self, pin=None):
        """
        Get the state of GPIO pins.
        Args:
            pin (int, optional): If specified, returns the state of the given pin.
                                 If None, returns the state of all monitored pins.
        Returns:
            bool or dict: The state of a specific pin or a dictionary of all pins.
        """
        if pin == None:
            self._update_status()
            return self.GPIO_STATE
        self.GPIO_STATE[pin] = True if GPIO.input(pin) else False
        return self.GPIO_STATE[pin]
