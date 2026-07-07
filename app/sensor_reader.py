import json
import asyncio
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "zwave/#"

# ---------------- STATE ----------------

state = {}

def now_time():
    return datetime.now().strftime("%H:%M:%S")


# ---------------- SENSOR PARSING ----------------

def extract_sensor(topic: str):
    parts = topic.split("/")

    if "sensor_multilevel" in topic:
        return parts[-1]  # Air_temperature, Humidity, etc.

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
    except:
        return

    sensor = extract_sensor(msg.topic)
    if not sensor:
        return

    state[sensor] = {
        "value": payload.get("value"),
        "sensor_time": payload.get("time")
    }


# ---------------- OUTPUT LOOP ----------------

async def loop():
    await asyncio.sleep(1)  # ignore startup burst

    while True:
        print(f"\n[{now_time()}]")

        for k, v in state.items():
            sensor_ts = v.get("sensor_time", 0)
            sensor_str = datetime.fromtimestamp(sensor_ts / 1000).strftime("%H:%M:%S")

            value = v.get("value")

            print(f"{k:<15} {value:<10} at {sensor_str}")

        await asyncio.sleep(1)


# ---------------- MAIN ----------------

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, 1883, 60)
    client.loop_start()

    asyncio.run(loop())


if __name__ == "__main__":
    main()
