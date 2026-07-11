from dataclasses import dataclass
from enum import Enum

from logger import log


# -----------------------------
# Symbolic world states
# -----------------------------

class Temperature(Enum):
    COLD = "cold"
    OK = "ok"
    HOT = "hot"


class CargoState(Enum):
    STABLE = "stable"
    UNSTABLE = "unstable"


# -----------------------------
# Observations from sensors
# -----------------------------

@dataclass
class Observation:

    temperature: float | None = None

    humidity: float | None = None

    illuminance: float | None = None

    ultraviolet: float | None = None

    motion: bool = False

    motion_timestamp: str | None = None


# -----------------------------
# World model
# -----------------------------

@dataclass
class WorldState:

    temperature: Temperature = Temperature.OK

    cargo: CargoState = CargoState.STABLE

    fan_on: bool = False

    heater_on: bool = False

    warning_on: bool = False

    last_motion_timestamp: str | None = None

    driver_acknowledged: bool = True


    # -------------------------
    # Update from observations
    # -------------------------

    def update(self, observation: Observation):

        self._update_temperature(
            observation.temperature
        )

        self._update_motion(
            observation
        )


    # -------------------------
    # Temperature handling
    # -------------------------

    def _update_temperature(self, value):

        if value is None:
            return


        if value > 30:

            self._change(
                "temperature",
                Temperature.HOT
            )


        elif value < 18:

            self._change(
                "temperature",
                Temperature.COLD
            )


        else:

            self._change(
                "temperature",
                Temperature.OK
            )


    # -------------------------
    # Motion handling
    # -------------------------

    def _update_motion(self, observation):

        if not observation.motion:
            return


        timestamp = observation.motion_timestamp


        # Ignore repeated PIR messages
        if timestamp == self.last_motion_timestamp:
            return


        self.last_motion_timestamp = timestamp


        self._change(
            "cargo",
            CargoState.UNSTABLE
        )


        self._change(
            "driver_acknowledged",
            False
        )


    # -------------------------
    # Driver action
    # -------------------------

    def acknowledge_cargo(self):

        self._change(
            "cargo",
            CargoState.STABLE
        )

        self._change(
            "driver_acknowledged",
            True
        )

    # -------------------------
    # Actuator state changes
    # -------------------------

    def set_fan(self, value: bool):

        self._change(
            "fan_on",
            value
        )


    def set_heater(self, value: bool):

        self._change(
            "heater_on",
            value
        )


    def set_warning(self, value: bool):

        self._change(
            "warning_on",
            value
        )

    # -------------------------
    # Logging state changes
    # -------------------------

    def _change(self, attribute, value):

        old = getattr(
            self,
            attribute
        )


        if old == value:
            return


        setattr(
            self,
            attribute,
            value
        )


        log(
            f"{attribute}: {old} -> {value}"
        )


# -----------------------------
# Global world instance
# -----------------------------

world = WorldState()
