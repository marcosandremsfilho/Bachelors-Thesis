from abc import abstractmethod

class GpioInterface:
    @abstractmethod
    def _update_status(self, actual_pin=None, state=None):
        pass

    @abstractmethod
    def _configure_pins(self):
        pass

    @abstractmethod
    def set_gpio(self, pin, state):
        pass

    @abstractmethod
    def get_gpio(self, pin=None):
        pass


