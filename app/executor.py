def execute(plan):

    print("\n--- EXECUTING PLAN ---")

    for action in plan:

        if action == "turn-on-cooler":
            print("Cooling system ON")

        elif action == "cool-cargo":
            print("Reducing cargo temperature")

        elif action == "turn-off-cooler":
            print("Cooling system OFF")


        elif action == "turn-on-heater":
            print("Heating system ON")

        elif action == "heat-cargo":
            print("Increasing cargo temperature")

        elif action == "turn-off-heater":
            print("Heating system OFF")


        elif action == "send-alert":
            print("ALERT: Possible cargo movement detected")


        else:
            print(f"Unknown action: {action}")

    print("--- DONE ---")
