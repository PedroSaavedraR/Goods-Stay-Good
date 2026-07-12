from dataclasses import dataclass
from datetime import datetime


@dataclass
class SensorSnapshot:
    """Raw sensor reading — no logic, no thresholds."""

    temperature: float | None = None
    humidity: float | None = None
    rear_distance: float | None = None

    motion_detected: bool = False
    motion_timestamp: datetime | None = None

    sun_has_set: bool | None = None


@dataclass
class Plan:
    """A sequence of action names from the planner."""

    actions: list[str]