import time
import sys
from pathlib import Path

# Allow importing from app/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "app"))

from sensors.mqtt import mqtt_state


def main():

    print("Starting MQTT sensor monitor...")
    print("Waiting for sensor data...\n")

    while True:

        data = mqtt_state.snapshot()

        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"Temperature: {data['temperature']} °C | "
            f"Humidity: {data['humidity']} % | "
            f"Motion: {data['motion']} | "
            f"Motion timestamp: {data['motion_timestamp']}"
        )

        time.sleep(1)


if __name__ == "__main__":
    main()
