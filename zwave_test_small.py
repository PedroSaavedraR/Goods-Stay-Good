import json
import paho.mqtt.client as mqtt

state = {
    "temperature": None,
    "humidity": None,
    "lux": None,
    "motion": None
}

def update_state(topic, value):
    if "Air_temperature" in topic:
        state["temperature"] = float(value)
    elif "Humidity" in topic:
        state["humidity"] = float(value)
    elif "Illuminance" in topic:
        state["lux"] = int(value)
    elif "Motion" in topic:
        state["motion"] = value

    print("\n--- SENSOR STATE ---")
    for k, v in state.items():
        print(f"{k}: {v}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        try:
            data = json.loads(payload)
            value = data.get("value", payload)
        except:
            value = payload

        update_state(msg.topic, value)

    except Exception as e:
        print("error:", e)

client = mqtt.Client()
client.on_message = on_message

client.connect("localhost", 1883)
client.subscribe("zwave/nodeID_4/#")

print("Listening to sensor stream...")
client.loop_forever()
