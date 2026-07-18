import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)


import time

from sensors.sensor_reader import read
from world_state.world_state import WorldState

from planner.problem_generator import generate
from planner_bridge import plan
from executor import execute
from hardware import hardware_manager as hardware

def main():

    world = WorldState()

    # Reset physical actuators to match initial WorldState
    hardware.fan_off()
    hardware.heating_lamp_off()

    while True:

        sensors = read()

        world.update_from_sensors(
            sensors
        )

        # Create fresh problem.pddl from current world state
        generate(world)

        # Run planner and get next action
        action = plan()

        print("ACTION FROM PLANNER:", repr(action))

        if action:
            execute(action, world)

        time.sleep(0.5)


if __name__ == "__main__":
    main()
