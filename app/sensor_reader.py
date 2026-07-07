import json
import paho.mqtt.client as mqtt


BROKER = "localhost"
TOPIC = "zwave/#"


# ---------------- STATE ----------------

state = {}


# ---------------- SENSOR PARSING ----------------

def extract_sensor(topic: str):

    parts = topic.split("/")

    if "sensor_multilevel" in topic:
        return parts[-1]

    if "sensor_binary" in topic:
        return "motion"

    return None


# ---------------- MQTT CALLBACKS ----------------

def on_connect(client, userdata, flags, reason_code, properties):

    print("[MQTT] connected")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    try:
        payload = json.loads(msg.payload.decode())

    except Exception:
        return


    sensor = extract_sensor(msg.topic)

    if not sensor:
        return


    state[sensor] = {
        "value": payload.get("value"),
        "sensor_time": payload.get("time")
    }


# ---------------- PUBLIC API ----------------

def get_sensor_snapshot():

    mapping = {
        "Air_temperature": "temperature",
        "Humidity": "humidity",
        "Illuminance": "illuminance",
        "Ultraviolet": "ultraviolet",
        "motion": "motion",
    }


    snapshot = {}

    for source, target in mapping.items():

        if source in state:
            snapshot[target] = state[source]["value"]

    return snapshot


# ---------------- START MQTT ----------------

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)

client.loop_start()
