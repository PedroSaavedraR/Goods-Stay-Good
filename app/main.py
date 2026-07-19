import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import time

from sensors.sensor_reader import read
from world_state.world_state import WorldState

from planner_bridge import plan

from planner import (
    temperature_problem,
    air_problem,
    fan_cleanup_problem,
    lights_problem,
    rear_problem,
)

from executor import execute

from hardware import hardware_manager as hardware


def disable_all_actuators():

    print("Disabling all actuators...")

    hardware.fan_off()
    hardware.heating_lamp_off()
    hardware.driving_lights_off()
    hardware.buzzer_off()


controllers = [
    temperature_problem,
    air_problem,
    lights_problem,
    rear_problem,
    fan_cleanup_problem,
]


def main():

    world = WorldState()

    disable_all_actuators()

    try:

        while True:

            print("\n==============================")
            print("NEW CONTROL LOOP")
            print("==============================")


            sensors = read()

            world.update_from_sensors(
                sensors
            )


            for controller in controllers:

                controller_name = controller.__name__

                print()
                print("------------------------------")
                print("CONTROLLER:", controller_name)


                controller.generate(world)


                action = plan()


                if action:

                    print(
                        "ACTION:",
                        action
                    )

                    execute(
                        action,
                        world
                    )

                else:

                    print(
                        "ACTION: no plan"
                    )


    except KeyboardInterrupt:

        print("\nCTRL+C received.")


    finally:

        disable_all_actuators()


if __name__ == "__main__":
    main()
