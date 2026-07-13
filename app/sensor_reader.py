from datetime import datetime

from model import SensorSnapshot
from sensors.mqtt import mqtt_state
from sensors.ultrasonic import get_distance
from sensors.sunset import sunset_checker


def read():
    data = mqtt_state.snapshot()

    motion_ts = data["motion_timestamp"]
    if motion_ts is not None:
        motion_datetime = datetime.utcfromtimestamp(motion_ts)
    else:
        motion_datetime = None

    return SensorSnapshot(
        temperature=data["temperature"],
        humidity=data["humidity"],
        motion_detected=data["motion"],
        motion_timestamp=motion_datetime,
        rear_distance=get_distance(),
        sun_has_set=sunset_checker.sun_has_set(),
    )
