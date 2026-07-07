from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
DOMAIN_FILE = PROJECT_ROOT / "planner" / "domain.pddl"


def create_plan(sensor_data):
    """
    Converts sensor data into a list of actions.

    Temporary rule-based version.
    Later this function will:
    1. generate a PDDL problem file
    2. call Fast Downward
    3. read sas_plan
    """

    plan = []

    temperature = sensor_data.get("temperature")
    motion = sensor_data.get("motion")


    # Cargo temperature handling

    if temperature is not None:

        if temperature > 30:
            plan.extend([
                "turn-on-cooler",
                "cool-cargo",
                "turn-off-cooler"
            ])

        elif temperature < 18:
            plan.extend([
                "turn-on-heater",
                "heat-cargo",
                "turn-off-heater"
            ])


    # Cargo movement handling

    if motion:
        plan.append("send-alert")


    return plan
