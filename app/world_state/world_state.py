import json
from enum import Enum
from pathlib import Path


class Temperature(Enum):
    COLD = "COLD"
    OK = "OK"
    HOT = "HOT"


class WorldState:

    def __init__(self):

        self.config = self._load_config()

        # Actuator state
        self.fan_on = False
        self.heater_on = False

        # Sensor-derived state
        self.temperature = Temperature.OK


    def _load_config(self):

        path = Path(__file__).parent / "config.json"

        with open(path) as f:
            return json.load(f)


    def update_from_sensors(self, sensors):

        temp = sensors.temperature

        limits = self.config["temperature"]

        if temp < limits["cold_limit"]:
            self.temperature = Temperature.COLD

        elif temp > limits["hot_limit"]:
            self.temperature = Temperature.HOT

        else:
            self.temperature = Temperature.OK


    def fan_enabled(self):
        self.fan_on = True

    def fan_disabled(self):
        self.fan_on = False

    def heater_enabled(self):
        self.heater_on = True

    def heater_disabled(self):
        self.heater_on = False
