import time

from sensor_reader import get_sensor_snapshot
from planner import create_plan
from executor import execute


while True:

    sensors = get_sensor_snapshot()

    print("\n--- SENSOR DATA ---")
    print(sensors)


    plan = create_plan(sensors)

    print("\n--- PLAN ---")
    print(plan)


    execute(plan)


    time.sleep(5)
