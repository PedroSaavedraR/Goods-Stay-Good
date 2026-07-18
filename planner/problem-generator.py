from pathlib import Path


DOMAIN = "domain.pddl"
OUTPUT = "problem.pddl"


def generate(
    temperature,
    fan_on,
    heater_on,
):

    facts = []


    if fan_on:
        facts.append("(fan_on)")

    if heater_on:
        facts.append("(heater_on)")


    if temperature == "HOT":
        facts.append("(temperature_hot)")

    elif temperature == "COLD":
        facts.append("(temperature_cold)")

    else:
        facts.append("(temperature_ok)")


    problem = f"""
(define (problem heating-problem)

    (:domain heating-cooling)

    (:init
        {' '.join(facts)}
    )


    (:goal
        (and
            (temperature_ok)
            (not(heater_on))
            (not(fan_on))
        )
    )
)
"""


    Path(OUTPUT).write_text(problem)


if __name__ == "__main__":

    generate(
        temperature="HOT",
        fan_on=False,
        heater_on=False,
    )
