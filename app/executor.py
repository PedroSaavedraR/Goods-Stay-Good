from hardware.relay import relay_on, relay_off


def execute(plan):

    print("\n--- EXECUTING PLAN ---")

    for action in plan:

        if action == "turn-on-cooler":
            print("Cooling system ON")
            relay_on(1)

        elif action == "turn-off-cooler":
            print("Cooling system OFF")
            relay_off(1)

        elif action == "turn-on-heater":
            print("Heating system ON")
            relay_on(2)

        elif action == "turn-off-heater":
            print("Heating system OFF")
            relay_off(2)

        elif action == "send-alert":
            print("Cargo movement detected")
            relay_on(3)

        else:
            print(f"Unknown action: {action}")
