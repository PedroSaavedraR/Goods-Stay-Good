from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone

from logger import log


# -----------------------------
# Symbolic states
# -----------------------------

class TemperatureState(Enum):
    COLD = "cold"
    OK = "ok"
    HOT = "hot"


class HumidityState(Enum):
    LOW = "low"
    OK = "ok"
    HIGH = "high"


class CargoState(Enum):
    CHECKED = "checked"
    UNCHECKED = "unchecked"


# -----------------------------
# Raw sensor observation
# -----------------------------

@dataclass
class Observation:

    temperature: float | None = None
    humidity: float | None = None

    illuminance: float | None = None

    rear_distance: float | None = None

    motion: bool = False
    motion_timestamp: float | None = None

    outdoor_bright: bool | None = None


# -----------------------------
# World model
# -----------------------------

@dataclass
class WorldState:

    temperature: TemperatureState = TemperatureState.OK

    humidity: HumidityState = HumidityState.OK

    cargo: CargoState = CargoState.CHECKED


    rear_clear: bool = False

    driving_lights_on: bool = False


    fan_on: bool = False
    heater_on: bool = False


    cargo_last_checked: float = field(
        default_factory=lambda: datetime.now(timezone.utc).timestamp()
    )


    last_motion: float | None = None


    changed: bool = True


    # -------------------------
    # Sensor update
    # -------------------------

    def update(self, obs: Observation):

        old = self.symbols()


        self.update_temperature(
            obs.temperature
        )

        self.update_humidity(
            obs.humidity
        )

        self.update_rear(
            obs.rear_distance
        )

        self.update_motion(
            obs.motion,
            obs.motion_timestamp
        )


        if obs.outdoor_bright is not None:
            self.outdoor_bright = obs.outdoor_bright


        new = self.symbols()

        self.changed = old != new


        if self.changed:
            log.info(
                "World changed: %s",
                new
            )


    # -------------------------
    # Rules
    # -------------------------

    def update_temperature(self, value):

        if value is None:
            return

        if value < 15:
            self.temperature = TemperatureState.COLD

        elif value > 28:
            self.temperature = TemperatureState.HOT

        else:
            self.temperature = TemperatureState.OK


    def update_humidity(self, value):

        if value is None:
            return

        if value < 40:
            self.humidity = HumidityState.LOW

        elif value > 60:
            self.humidity = HumidityState.HIGH

        else:
            self.humidity = HumidityState.OK



    def update_rear(self, distance):

        if distance is None:
            return

        self.rear_clear = distance > 10



    def update_motion(self, motion, timestamp):

        if not motion:
            return


        self.last_motion = timestamp


        # Cargo can become unsafe
        # only after a NEW motion event

        if timestamp and timestamp > self.cargo_last_checked:

            self.cargo = CargoState.UNCHECKED

            log.info(
                "Cargo marked unchecked because of motion"
            )



    # -------------------------
    # Driver interaction
    # -------------------------

    def acknowledge_cargo(self):

        self.cargo = CargoState.CHECKED

        self.cargo_last_checked = (
            datetime.now(timezone.utc)
            .timestamp()
        )

        log.info(
            "Cargo checked by driver"
        )


    # -------------------------
    # PDDL conversion
    # -------------------------

    def symbols(self):

        result = set()


        result.add(
            self.temperature.value
        )

        result.add(
            self.humidity.value
        )

        result.add(
            "cargo_checked"
            if self.cargo == CargoState.CHECKED
            else "cargo_unchecked"
        )


        if self.rear_clear:
            result.add(
                "rear_clear"
            )


        if self.driving_lights_on:
            result.add(
                "driving_lights_on"
            )


        if self.fan_on:
            result.add(
                "fan_on"
            )


        if self.heater_on:
            result.add(
                "heater_on"
            )


        return result



    def goal_reached(self):

        return (
            self.rear_clear
            and self.cargo == CargoState.CHECKED
            and self.temperature == TemperatureState.OK
            and self.humidity == HumidityState.OK
        )



# global world object

world = WorldState()
