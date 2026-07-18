import time

from sensors.sensor_reader import read
from world_state.world_state import WorldState

from planner_bridge import create_plan
from executor import execute


def main():

    world = WorldState()


    while True:

        sensors = read()

        world.update_from_sensors(
            sensors
        )


        create_plan()


        action = create_plan()


        if action:
            execute(action)


        time.sleep(0.5)



if __name__ == "__main__":
    main()
