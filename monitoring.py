import asyncio
from aiohttp import ClientSession
from zwave_js_server.client import Client
from zwave_js_server.model.node import Node
from zwave_js_server.model.value import Value

# --- CONFIGURATION ---
TARGET_NODE_ID = 4            # The Node ID of your MultiSensor 6
REFRESH_INTERVAL = 5          # How often to print the values (in seconds)
SERVER_URL = "ws://localhost:3000"
# ---------------------

sensor_data = {
    "Air temperature": "Waiting...",
    "Humidity": "Waiting...",
    "Motion state": "Waiting...",
    "Illuminance": "Waiting...",
    "Ultraviolet": "Waiting...",
    "Seismic intensity": "Waiting..."
}

async def display_loop():
    """Loops forever, printing the current data snapshot at the specified interval."""
    while True:
        await asyncio.sleep(REFRESH_INTERVAL)
        print("\n--- Aeotec MultiSensor 6 Snapshot ---")
        for sensor, val in sensor_data.items():
            # Standardizing labels for clean terminal output
            label = "Vibration" if sensor == "Seismic intensity" else sensor
            label = "Motion" if sensor == "Motion state" else label
            print(f"│ {label:<16} : {val}")
        print("-------------------------------------")

async def main():
    async with ClientSession() as session:
        client = Client(SERVER_URL, session)
        print(f"Connecting to Z-Wave JS Server at {SERVER_URL}...")
        await client.connect()
        await client.initialize()
        print("Connected successfully!")

        driver = client.driver

        # 1. Seed the initial values upon starting the script
        node = driver.controller.nodes.get(TARGET_NODE_ID)
        if node:
            for value in node.values.values():
                if value.property_name in sensor_data:
                    sensor_data[value.property_name] = f"{value.value} {value.metadata.unit or ''}".strip()
        else:
            print(f"Warning: Node ID {TARGET_NODE_ID} not found on this network.")

        # 2. Set up a listener to update our memory state whenever a sensor reports in
        def on_value_update(event_type, value: Value):
            if value.node.node_id == TARGET_NODE_ID and value.property_name in sensor_data:
                # Format the value with its unit (e.g., "22.5 °C" or "True")
                unit = value.metadata.unit or ""
                sensor_data[value.property_name] = f"{value.value} {unit}".strip()

        driver.controller.on("value updated", on_value_update)

        # 3. Spin up the background display loop alongside the Z-Wave listener
        asyncio.create_task(display_loop())

        # Keep the script open to receive WebSocket events
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")