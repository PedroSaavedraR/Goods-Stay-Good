import json
import paho.mqtt.client as mqtt

from world_state import Observation


BROKER = "localhost"
TOPIC = "zwave/#"


# -----------------------------
# Raw MQTT state
# -----------------------------

state = {}


# -----------------------------
# Sensor parsing
# -----------------------------

def extract_sensor(topic: str):

    parts = topic.split("/")


    if "sensor_multilevel" in topic:
        return parts[-1]


    if "sensor_binary" in topic:
        return "motion"


    return None



# -----------------------------
# MQTT callbacks
# -----------------------------

def on_connect(client, userdata, flags, reason_code, properties):

    print("[MQTT] connected")

    client.subscribe(TOPIC)



def on_message(client, userdata, msg):

    try:

        payload = json.loads(
            msg.payload.decode()
        )

    except Exception:

        return


    sensor = extract_sensor(
        msg.topic
    )


    if not sensor:
        return


    state[sensor] = {

        "value": payload.get("value"),

        "sensor_time": payload.get("time")
    }



# -----------------------------
# Convert raw data -> observation
# -----------------------------

def get_observation():

    mapping = {

        "Air_temperature": "temperature",

        "Humidity": "humidity",

        "Illuminance": "illuminance",

        "Ultraviolet": "ultraviolet",

    }


    values = {}


    for source, target in mapping.items():

        if source in state:

            values[target] = state[source]["value"]



    motion = False
    motion_time = None


    if "motion" in state:

        motion = bool(
            state["motion"]["value"]
        )

        motion_time = state["motion"]["sensor_time"]



    return Observation(

        temperature=values.get(
            "temperature"
        ),

        humidity=values.get(
            "humidity"
        ),

        illuminance=values.get(
            "illuminance"
        ),

        ultraviolet=values.get(
            "ultraviolet"
        ),

        motion=motion,

        motion_timestamp=motion_time
    )



# -----------------------------
# Start MQTT listener
# -----------------------------

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)


client.on_connect = on_connect

client.on_message = on_message


client.connect(
    BROKER,
    1883,
    60
)


client.loop_start()
