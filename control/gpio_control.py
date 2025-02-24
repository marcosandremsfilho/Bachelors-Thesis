import RPi.GPIO as GPIO

class GpioControl:

    GPIO_STATE = {7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 18: False, 22: False, 29: False,
                  31: False, 32: False, 33: False, 35: False, 36: False, 37: False, 38: False, 40: False}
    
    def __init__(self, input_gpios: list = []) -> None:
        self.input_gpios = input_gpios

        self._configure_pins()

    def _update_status(self, actual_pin = None, state = None):
        for pin in self.GPIO_STATE:
            if pin in self.input_gpios:
                self.GPIO_STATE[pin] = True if GPIO.input(pin) else False
        if actual_pin is not None:
            self.GPIO_STATE[actual_pin] = state

    def _configure_pins(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        for pin in self.GPIO_STATE:
            if pin in self.input_gpios:
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            else:
                GPIO.setup(pin, GPIO.OUT)

    def set_gpio(self, pin, state):
        GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
        self._update_status(pin, state)

    def get_gpio(self, pin = None):
        if pin == None:
            self._update_status()
            return self.GPIO_STATE
        self.GPIO_STATE[pin] = True if GPIO.input(pin) else False
        return self.GPIO_STATE[pin]