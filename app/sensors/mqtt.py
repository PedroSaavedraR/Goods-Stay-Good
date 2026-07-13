import json
import threading
import time

import paho.mqtt.client as mqtt

from logger import log


BROKER = "localhost"
TOPIC = "zwave/#"


# -----------------------------
# Shared sensor state
# -----------------------------

class MQTTState:

    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.motion = False
        self.motion_timestamp = None
        self.lock = threading.Lock()

    def snapshot(self):
        """Return a consistent dict copy of the latest sensor values."""
        with self.lock:
            return {
                "temperature": self.temperature,
                "humidity": self.humidity,
                "motion": self.motion,
                "motion_timestamp": self.motion_timestamp,
            }

    def update(self, topic, payload):
        with self.lock:
            value = payload.get("value")
            timestamp = payload.get("time", time.time())
            if "Air_temperature" in topic:
                self.temperature = value

            elif topic.endswith("/Humidity"):
                self.humidity = value

            elif "Motion_sensor_status" in topic:
                self.motion = bool(value)
                self.motion_timestamp = timestamp
                log.info("Motion update: %s", self.motion)


mqtt_state = MQTTState()


# -----------------------------
# MQTT client callbacks
# -----------------------------

def on_connect(client, userdata, flags, reason_code, properties=None):
    log.info("MQTT connected to %s", BROKER)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except Exception:
        return

    if not isinstance(payload, dict):
        return

    mqtt_state.update(msg.topic, payload)


# -----------------------------
# Start listener immediately
# -----------------------------

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_start()