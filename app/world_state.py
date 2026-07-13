from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from config import CONFIG
from logger import log
from model import SensorSnapshot


class TemperatureState(Enum):
    COLD = "cold"
    OK = "ok"
    HOT = "hot"


class HumidityState(Enum):
    LOW = "low"
    OK = "ok"
    HIGH = "high"


@dataclass
class WorldState:

    temperature: float | None = None
    humidity: float | None = None
    rear_distance: float | None = None
    sun_has_set: bool = False

    last_motion: float | None = None
    cargo_last_checked: float = field(
        default_factory=lambda: datetime.now(timezone.utc).timestamp()
    )

    fan_on: bool = False
    heater_on: bool = False
    driving_lights_on: bool = False
    buzzer_on: bool = False
    status_led_on: bool = False

    version: int = 0

    def apply(self, snapshot: SensorSnapshot):
        old_symbols = self.predicates()
        if snapshot.temperature is not None:
            self.temperature = snapshot.temperature
        if snapshot.humidity is not None:
            self.humidity = snapshot.humidity
        if snapshot.rear_distance is not None:
            self.rear_distance = snapshot.rear_distance
        if snapshot.sun_has_set is not None:
            self.sun_has_set = snapshot.sun_has_set
        if snapshot.motion_detected and snapshot.motion_timestamp is not None:
            ts = snapshot.motion_timestamp.timestamp()
            if ts > self.cargo_last_checked:
                self.last_motion = ts
                log.info("Motion detected — cargo needs re-check")
        new_symbols = self.predicates()
        if old_symbols != new_symbols:
            self.version += 1
            log.info("World version %d: %s", self.version, new_symbols)

    def acknowledge_cargo(self):
        self.cargo_last_checked = datetime.now(timezone.utc).timestamp()
        self.last_motion = None
        self.version += 1
        log.info("Cargo checked by driver — version %d", self.version)

    @property
    def temperature_state(self) -> TemperatureState:
        if self.temperature is None:
            return TemperatureState.OK
        if self.temperature < CONFIG.temperature_cold:
            return TemperatureState.COLD
        if self.temperature > CONFIG.temperature_hot:
            return TemperatureState.HOT
        return TemperatureState.OK

    @property
    def humidity_state(self) -> HumidityState:
        if self.humidity is None:
            return HumidityState.OK
        if self.humidity < CONFIG.humidity_low:
            return HumidityState.LOW
        if self.humidity > CONFIG.humidity_high:
            return HumidityState.HIGH
        return HumidityState.OK

    @property
    def rear_clear(self) -> bool:
        if self.rear_distance is None:
            return True
        return self.rear_distance > CONFIG.rear_distance_min

    @property
    def cargo_checked(self) -> bool:
        if self.last_motion is None:
            return True
        return self.last_motion <= self.cargo_last_checked

    @property
    def drive_safe(self) -> bool:
        outdoor_or_lights = (not self.sun_has_set) or self.driving_lights_on
        return outdoor_or_lights and self.rear_clear

    def predicates(self) -> set[str]:
        result = set()
        result.add(f"temperature_{self.temperature_state.value}")
        result.add(f"humidity_{self.humidity_state.value}")
        result.add("cargo_checked" if self.cargo_checked else "cargo_unchecked")
        if self.rear_clear:
            result.add("rear_clear")
        if self.drive_safe:
            result.add("drive_safe")
        if self.driving_lights_on:
            result.add("driving_lights_on")
        if self.sun_has_set:
            result.add("sun_has_set")
        if self.fan_on:
            result.add("fan_on")
        if self.heater_on:
            result.add("heater_on")
        if self.buzzer_on:
            result.add("buzzer_on")
        if self.status_led_on:
            result.add("status_led_on")
        return result

    def goal_reached(self) -> bool:
        return (
            self.drive_safe
            and self.cargo_checked
            and self.temperature_state == TemperatureState.OK
            and self.humidity_state == HumidityState.OK
        )

    def needs_replan(self, planned_version: int) -> bool:
        return self.version != planned_version and not self.goal_reached()


world = WorldState()