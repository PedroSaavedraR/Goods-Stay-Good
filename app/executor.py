from hardware.relay import relay_on, relay_off

from world_state import world


def execute(plan):

    print("\n--- EXECUTING PLAN ---")


    for action in plan:


        if action == "turn-on-fan":

            if not world.fan_on:

                print("Fan ON")

                relay_on(1)

                world.set_fan(True)



        elif action == "turn-off-fan":

            if world.fan_on:

                print("Fan OFF")

                relay_off(1)

                world.set_fan(False)



        elif action == "turn-on-heater":

            if not world.heater_on:

                print("Heater ON")

                relay_on(2)

                world.set_heater(True)



        elif action == "turn-off-heater":

            if world.heater_on:

                print("Heater OFF")

                relay_off(2)

                world.set_heater(False)



        elif action == "turn-on-warning":

            if not world.warning_on:

                print("Warning light ON")

                relay_on(3)

                world.set_warning(True)



        elif action == "turn-off-warning":

            if world.warning_on:

                print("Warning light OFF")

                relay_off(3)

                world.set_warning(False)



        else:

            print(
                f"Unknown action: {action}"
            )


    print("--- DONE ---")

def initialize_hardware():

    print("\n--- INITIALIZING HARDWARE ---")

    # Force safe startup state

    relay_off(1)
    relay_off(2)
    relay_off(3)


    world.set_fan(False)

    world.set_heater(False)

    world.set_warning(False)


    print("--- HARDWARE READY ---")
