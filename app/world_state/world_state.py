import json
from enum import Enum
from pathlib import Path

class Temperature(Enum):
    COLD = "COLD"
    OK = "OK"
    HOT = "HOT"
# Bad air quality = humidity out of bounds, e.g. too dry or too moist
class AirQuality(Enum):
    BAD = "BAD"
    OK = "OK"

class WorldState:

    def __init__(self):

        self.config = self._load_config()

        # Actuator state
        self.fan_on = False
        self.heater_on = False
        self.driving_lights_on = False

        # Sensor-derived state
        self.temperature = Temperature.OK
        self.air_quality = AirQuality.OK
        self.outside_bright_enough = True


    def _load_config(self):

        path = Path(__file__).parent / "config.json"

        with open(path) as f:
            return json.load(f)


    def update_from_sensors(self, sensors):
        # Temperature
        temp = sensors.temperature

        limits = self.config["temperature"]

        if temp < limits["cold_limit"]:
            self.temperature = Temperature.COLD

        elif temp > limits["hot_limit"]:
            self.temperature = Temperature.HOT

        else:
            self.temperature = Temperature.OK

        # Humidity
        humidity = sensors.humidity

        limits = self.config["humidity"]

        if (
            humidity < limits["low_limit"]
            or humidity > limits["high_limit"]
        ):
            self.air_quality = AirQuality.BAD

        else:
            self.air_quality = AirQuality.OK

        # Daylight
        self.outside_bright_enough = not sensors.sun_has_set





    # Those functions are called from the app/executor.py
    def fan_enabled(self):
        self.fan_on = True

    def fan_disabled(self):
        self.fan_on = False

    def heater_enabled(self):
        self.heater_on = True

    def heater_disabled(self):
        self.heater_on = False

    def driving_lights_enabled(self):
        self.driving_lights_on = True

    def driving_lights_disabled(self):
        self.driving_lights_on = False
