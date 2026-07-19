from pathlib import Path

from world_state.world_state import Temperature

OUTPUT = Path(__file__).parent / "problem.pddl"


def generate(world):

    facts = []

    # Heater state
    if world.heater_on:
        facts.append("(heater_on)")
    else:
        facts.append("(not (heater_on))")

    # Fan state
    if world.fan_on:
        facts.append("(fan_on)")
    else:
        facts.append("(not (fan_on))")

    # Temperature state
    if world.temperature == Temperature.COLD:
        facts.append("(temperature_cold)")

    elif world.temperature == Temperature.HOT:
        facts.append("(temperature_hot)")

    else:
        facts.append("(temperature_ok)")


    # Fan requirement caused by temperature
    if world.fan_needed_by_temperature:
        facts.append("(fan_needed_by_temperature)")


    problem = f"""
(define (problem smart-truck)

    (:domain smart-truck)

    (:init
        {' '.join(facts)}
    )

    (:goal
        (and
            (temperature_ok)
            (not (heater_on))
            (not (fan_needed_by_temperature))
        )
    )
)
"""

    OUTPUT.write_text(problem)
