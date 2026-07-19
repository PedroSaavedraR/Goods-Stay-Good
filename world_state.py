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

class Obstacle(Enum):
    NEAR = "NEAR"
    CLEAR = "CLEAR"

class WorldState:

    def __init__(self):

        self.config = self._load_config()

        # Actuator state
        self.fan_on = False
        self.heater_on = False

        # Sensor-derived state
        self.temperature = Temperature.OK
        self.air_quality = AirQuality.OK
        self.obstacle = Obstacle.CLEAR

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

        #ultrasonic-buzzer
        distance = sensors.rear_distance
        threshold = self.config["ultrasonic"]["threshold_cm"]
        if distance < threshold:
            self.obstacle = Obstacle.NEAR
        else:
            self.obstacle = Obstacle.CLEAR


    # Those functions are called from the app/executor.py
    def fan_enabled(self):
        self.fan_on = True

    def fan_disabled(self):
        self.fan_on = False

    def heater_enabled(self):
        self.heater_on = True

    def heater_disabled(self):
        self.heater_on = False
