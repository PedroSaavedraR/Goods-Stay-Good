import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import time
from collections import deque

from sensors.sensor_reader import read
from world_state.world_state import WorldState

from planner_bridge import plan

from planner import (
    temperature_problem,
    air_problem,
    fan_cleanup_problem,
    lights_problem,
    rear_problem,
    cargo_problem,
)

from executor import execute

from hardware import hardware_manager as hardware

from dashboard import server as dashboard



def disable_all_actuators():

    print("Disabling all actuators...")

    hardware.fan_off()
    hardware.heating_lamp_off()
    hardware.driving_lights_off()
    hardware.buzzer_off()
    hardware.cargo_led_off()



controllers = [
    temperature_problem,
    air_problem,
    lights_problem,
    rear_problem,
    fan_cleanup_problem,
    cargo_problem,
]



controller_history = {

    "temperature_problem":
        deque(maxlen=50),

    "air_problem":
        deque(maxlen=50),

    "lights_problem":
        deque(maxlen=50),

    "rear_problem":
        deque(maxlen=50),

    "fan_cleanup_problem":
        deque(maxlen=50),

    "cargo_problem":
        deque(maxlen=50),

}



controller_plans = {

    "temperature_problem": "unknown",
    "air_problem": "unknown",
    "lights_problem": "unknown",
    "rear_problem": "unknown",
    "fan_cleanup_problem": "unknown",
    "cargo_problem": "unknown",

}



def dashboard_world(world):

    return {

        "fan_on":
            world.fan_on,

        "heater_on":
            world.heater_on,

        "driving_lights_on":
            world.driving_lights_on,

        "buzzer_on":
            world.buzzer_on,


        "temperature":
            str(world.temperature),

        "air_quality":
            str(world.air_quality),

        "outside_bright_enough":
            world.outside_bright_enough,

        "rear_clear":
            world.rear_clear,


        "fan_needed_by_temperature":
            world.fan_needed_by_temperature,

        "fan_needed_by_air":
            world.fan_needed_by_air,


        "cargo_might_be_unstable":
            world.cargo_might_be_unstable,

        "cargo_led_on":
            world.cargo_led_on,


        "last_motion_timestamp":
            str(world.last_motion_timestamp),

        "last_cargo_confirmation_timestamp":
            str(world.last_cargo_confirmation_timestamp),

    }



def update_dashboard(world):

    dashboard.update(

        world=dashboard_world(world),

        config=world.config,

        controllers={

            name: {

                "plan":
                    controller_plans[name],

                "history":
                    list(controller_history[name]),

            }

            for name in controller_plans

        }

    )



def main():

    world = WorldState()

    dashboard.start()

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


            print("WORLD:")
            print(" temperature:", world.temperature)
            print(" air:", world.air_quality)
            print(" fan_on:", world.fan_on)
            print(
                " fan_needed_by_temperature:",
                world.fan_needed_by_temperature
            )
            print(
                " fan_needed_by_air:",
                world.fan_needed_by_air
            )
            print(
                " cargo_unstable:",
                world.cargo_might_be_unstable
            )
            print(
                " cargo_led:",
                world.cargo_led_on
            )
            print(
                " last_motion:",
                world.last_motion_timestamp
            )
            print(
                " last_confirm:",
                world.last_cargo_confirmation_timestamp
            )



            for controller in controllers:


                # Convert:
                # planner.temperature_problem
                #
                # into:
                # temperature_problem

                controller_name = (
                    controller.__name__
                    .split(".")[-1]
                )


                print()
                print("------------------------------")
                print(
                    "CONTROLLER:",
                    controller_name
                )


                controller.generate(world)


                action = plan()



                if action:

                    print(
                        "ACTION:",
                        action
                    )


                    controller_plans[controller_name] = [
                        action
                    ]


                    controller_history[controller_name].append(
                        action
                    )


                    execute(
                        action,
                        world
                    )


                else:

                    print(
                        "ACTION: at goal state"
                    )


                    controller_plans[controller_name] = [
                        "at goal state"
                    ]



            update_dashboard(world)


            time.sleep(0.5)



    except KeyboardInterrupt:

        print("\nCTRL+C received.")



    finally:

        disable_all_actuators()



if __name__ == "__main__":
    main()
