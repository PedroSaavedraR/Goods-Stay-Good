import time

from logger import reset
from sensor_reader import get_observation
from world_state import world
from planner import create_plan
from executor import execute, initialize_hardware
from button import check_button



# -----------------------------
# Startup
# -----------------------------

reset()

initialize_hardware()

print("=== Smart Truck Controller Started ===")


# -----------------------------
# Main control loop
# -----------------------------

while True:


    # Check physical acknowledgement button

    check_button()



    # Read sensors

    observation = get_observation()


    print("\n--- OBSERVATION ---")
    print(observation)



    # Update symbolic world

    world.update(
        observation
    )


    print("\n--- WORLD STATE ---")
    print(world)



    # Ask planner what should happen

    plan = create_plan()



    print("\n--- PLAN ---")
    print(plan)



    # Execute actions

    execute(plan)



    time.sleep(5)
