from pathlib import Path

from world_state.world_state import Temperature, AirQuality


OUTPUT = Path(__file__).parent / "problem.pddl"


def generate(world):

    facts = []

    # Actuator state
    if world.fan_on:
        facts.append("(fan_on)")

    if world.heater_on:
        facts.append("(heater_on)")

    if world.driving_lights_on:
        facts.append("(driving_lights_on)")

    if world.buzzer_on:
        facts.append("(buzzer_on)")



    # Temperature state
    if world.temperature == Temperature.HOT:
        facts.append("(temperature_hot)")

    elif world.temperature == Temperature.COLD:
        facts.append("(temperature_cold)")

    else:
        facts.append("(temperature_ok)")


    # Air quality state
    if world.air_quality == AirQuality.BAD:
        facts.append("(bad_air)")

    # Daylight state
    if world.outside_bright_enough:
        facts.append("(outside_bright_enough)")

    # Rear distance state
    if world.rear_clear:
        facts.append("(rear_clear)")

    # -------------------------
    # Goal state
    # -------------------------

    goal = [
        "(temperature_ok)",
        "(not (heater_on))",
        "(not (fan_on))",
        "(not (bad_air))",
        "(rear_clear)",
        "(not (buzzer_on))",
    ]

    if world.outside_bright_enough:
        goal.append(
            "(not (driving_lights_on))"
        )
    else:
        goal.append(
            "(driving_lights_on)"
        )


    problem = f"""
(define (problem smart-truck)

    (:domain smart-truck)

    (:init
        {' '.join(facts)}
    )

    (:goal
        (and
            {' '.join(goal)}
        )
    )
)
"""

    OUTPUT.write_text(problem)


if __name__ == "__main__":
    print("This file is meant to be called by main.py")
