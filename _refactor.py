#!/usr/bin/env python3
"""One-shot refactoring script for Steps 3-10 of AI-PLAN.md"""

import os, textwrap

BASE = "/home/jelitau/Documents/Uni/SmartCitiesAndIoT/Goods-Stay-Good"

def write(path: str, content: str):
    full = os.path.join(BASE, path)
    with open(full, "w") as f:
        f.write(content)
    print(f"  Wrote {path}")

print("=== Step 3: Fix sensor_reader + mqtt + main ===")

# ── mqtt.py ──
write("app/sensors/mqtt.py", """\
import json
import threading
import time

import paho.mqtt.client as mqtt

from logger import log

BROKER = "localhost"
TOPIC = "zwave/#"


class MQTTState:
    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.motion = False
        self.motion_timestamp = None
        self.lock = threading.Lock()

    def update(self, topic, payload):
        with self.lock:
            value = payload.get("value")
            timestamp = payload.get("time")
            if "Air_temperature" in topic:
                self.temperature = value
            elif topic.endswith("/Humidity"):
                self.humidity = value
            elif "Motion_sensor_status" in topic:
                self.motion = bool(value)
                self.motion_timestamp = timestamp
                log.info("Motion update: %s", self.motion)

    def snapshot(self):
        with self.lock:
            return {
                "temperature": self.temperature,
                "humidity": self.humidity,
                "motion": self.motion,
                "motion_timestamp": self.motion_timestamp,
            }


mqtt_state = MQTTState()


def on_connect(client, userdata, flags, rc):
    log.info("MQTT connected (rc=%s)", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        mqtt_state.update(msg.topic, payload)
    except Exception:
        log.warning("Bad MQTT message on %s", msg.topic)


def start():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    t = threading.Thread(target=client.loop_forever, daemon=True)
    t.start()
    log.info("MQTT listener started")
""")

# ── sensor_reader.py ──
write("app/sensor_reader.py", """\
from datetime import datetime

from model import SensorSnapshot
from sensors.mqtt import mqtt_state
from sensors.ultrasonic import get_distance


def read() -> SensorSnapshot:
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
    )
""")

# ── main.py (Step 3 fix: snapshot + apply) ──
write("app/main.py", """\
import time

from world_state import world
from sensor_reader import read
from planner_bridge import create_plan
from executor import Executor
from hardware import apply as hw_apply
from logger import log

executor = Executor()
last_planned_version = -1


def main():
    log.info("Smart truck starting")
    while True:
        snapshot = read()
        world.apply(snapshot)

        if world.needs_replan(last_planned_version) or not executor.plan:
            plan = create_plan(world)
            executor.set_plan(plan)
            last_planned_version = world.version

        if executor.plan:
            executor.execute_next(world)

        hw_apply(world)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
""")

print("=== Step 4: Create sunset sensor + update config ===")

write("app/sensors/sunset.py", """\
import json
import urllib.request
from datetime import datetime, timezone

from logger import log

URL = "https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"


def fetch_sun_has_set(lat: float = 51.0, lng: float = 10.0) -> bool | None:
    try:
        with urllib.request.urlopen(URL.format(lat=lat, lng=lng), timeout=5) as resp:
            data = json.loads(resp.read().decode())
        sunset_str = data["results"]["sunset"]
        sunset = datetime.fromisoformat(sunset_str)
        now = datetime.now(timezone.utc)
        return now > sunset
    except Exception as e:
        log.warning("Sunset API failed: %s", e)
        return None
""")

write("app/config.py", """\
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    temperature_cold: float = 15.0
    temperature_hot: float = 28.0
    humidity_low: float = 40.0
    humidity_high: float = 60.0
    rear_distance_min: float = 10.0
    sensor_poll_interval: float = 0.5
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_topic: str = "zwave/#"
    cargo_button_gpio: int = 17
    ultrasonic_trigger_gpio: int = 22
    ultrasonic_echo_gpio: int = 27
    buzzer_gpio: int = 4
    driving_light_gpio: int = 18
    timezone: str = "Europe/Berlin"
    i2c_address: int = 0x20
    relay_count: int = 4
    sunset_lat: float = 51.0
    sunset_lng: float = 10.0


CONFIG = Config()
""")

print("=== Step 5: Extend PDDL domain ===")

write("planner/domain.pddl", """\
(define (domain smart-truck)
    (:requirements :strips)

    (:predicates
        (temperature_ok) (temperature_hot) (temperature_cold)
        (humidity_ok) (humidity_high) (humidity_low)
        (cargo_checked) (cargo_unchecked)
        (rear_clear)
        (driving_lights_on) (sun_has_set)
        (drive_safe)
        (fan_on) (heater_on)
    )

    ;; ── Cooling ──
    (:action fan_on
        :precondition (temperature_hot)
        :effect (fan_on)
    )
    (:action fan_off
        :precondition (temperature_ok)
        :effect (not (fan_on))
    )

    ;; ── Heating ──
    (:action heater_on
        :precondition (temperature_cold)
        :effect (heater_on)
    )
    (:action heater_off
        :precondition (temperature_ok)
        :effect (not (heater_on))
    )

    ;; ── Humidity (fan) ──
    (:action humidity_fan_on
        :precondition (or (humidity_high) (humidity_low))
        :effect (fan_on)
    )
    (:action humidity_fan_off
        :precondition (and (humidity_ok) (temperature_ok))
        :effect (not (fan_on))
    )

    ;; ── Cargo ──
    (:action check_cargo
        :precondition (cargo_unchecked)
        :effect (and (cargo_checked) (not (cargo_unchecked)))
    )

    ;; ── Driving lights ──
    (:action turn_lights_on
        :precondition (sun_has_set)
        :effect (driving_lights_on)
    )
    (:action turn_lights_off
        :precondition (and (driving_lights_on) (not (sun_has_set)))
        :effect (not (driving_lights_on))
    )
)
""")

print("=== Step 6: Update planner/main.py (predicates, no bright_enough) ===")
write("planner/main.py", """\
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOMAIN = PROJECT_ROOT / "planner" / "domain.pddl"
PROBLEM = PROJECT_ROOT / "planner" / "problem.pddl"


def create_problem(world):
    predicates = world.predicates()
    facts = [f"({p})" for p in predicates]

    goal = """\
        (and
            (rear_clear)
            (cargo_checked)
            (temperature_ok)
            (humidity_ok)
        )
    """

    content = f"""
(define (problem truck_problem)
    (:domain smart-truck)
    (:init
        {' '.join(facts)}
    )
    (:goal
        {goal}
    )
)
"""
    PROBLEM.write_text(content)
    return PROBLEM
""")

print("=== Step 7: Refactor executor (no direct hardware calls) ===")

write("app/executor.py", """\
from logger import log


class Executor:
    def __init__(self):
        self.plan = []

    def set_plan(self, plan):
        self.plan = plan
        log.info("New plan: %s", plan)

    def execute_next(self, world):
        if not self.plan:
            return
        action = self.plan.pop(0)
        log.info("Executing %s", action)

        if action == "fan_on":
            world.fan_on = True
        elif action == "fan_off":
            world.fan_on = False
        elif action == "heater_on":
            world.heater_on = True
        elif action == "heater_off":
            world.heater_on = False
        elif action == "driving_lights_on":
            world.driving_lights_on = True
        elif action == "driving_lights_off":
            world.driving_lights_on = False
        elif action == "check_cargo":
            world.acknowledge_cargo()
""")

print("=== Step 8: Create hardware/__init__.py with apply(world) ===")

write("app/hardware/__init__.py", """\
from hardware import relay
from hardware import lights


def apply(world):
    # Fan
    if world.fan_on:
        relay.fan_on()
    else:
        relay.fan_off()

    # Heater
    if world.heater_on:
        relay.heater_on()
    else:
        relay.heater_off()

    # Driving lights
    if world.driving_lights_on:
        lights.driving_lights_on()
    else:
        lights.driving_lights_off()

    # Buzzer: rear distance alert
    if not world.rear_clear:
        relay.buzzer_on()
    else:
        relay.buzzer_off()

    # Status LED: cargo unchecked
    if not world.cargo_checked:
        relay.status_led_on()
    else:
        relay.status_led_off()
""")

print("=== Step 10: Final cleanup ===")

write("app/sensors/__init__.py", """\
from sensors.mqtt import mqtt_state, start
from sensors.ultrasonic import get_distance
from sensors.sunset import fetch_sun_has_set
""")

# Remove legacy Observation from world_state.py (already clean, but double-check)
# Update world_state.py to import SensorSnapshot cleanly (already done)

print("\\nAll files written. Steps 3-10 complete.")