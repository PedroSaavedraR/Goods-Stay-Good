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


    problem = f"""
(define (problem smart-truck)

    (:domain heating-cooling)

    (:init
        {' '.join(facts)}
    )

    (:goal
        (and
            (temperature_ok)
            (not (heater_on))
            (not (fan_on))
            (not (bad_air))
        )
    )
)
"""


    OUTPUT.write_text(problem)


if __name__ == "__main__":
    print("This file is meant to be called by main.py")
