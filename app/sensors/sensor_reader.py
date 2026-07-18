from dataclasses import dataclass
from datetime import datetime

from .mqtt import mqtt_state
from .ultrasonic import get_distance
from .sunset import sun_has_set


@dataclass(frozen=True)
class SensorSnapshot:
    temperature: float
    humidity: float
    motion_detected: bool
    motion_timestamp: datetime | None
    rear_distance: float
    sun_has_set: bool


def read() -> SensorSnapshot:
    data = mqtt_state.snapshot()

    motion_timestamp = data["motion_timestamp"]

    if motion_timestamp is not None:
        # Z-Wave MQTT timestamps are in milliseconds (JS convention)
        if motion_timestamp > 1e12:
            motion_timestamp /= 1000.0

        motion_datetime = datetime.utcfromtimestamp(motion_timestamp)
    else:
        motion_datetime = None

    return SensorSnapshot(
        temperature=data["temperature"],
        humidity=data["humidity"],
        motion_detected=data["motion"],
        motion_timestamp=motion_datetime,
        rear_distance=get_distance(),
        sun_has_set=sun_has_set(),
    )
