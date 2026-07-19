from pathlib import Path

OUTPUT = Path(__file__).parent / "problem.pddl"


def generate(world):

    facts = []


    if world.fan_on:
        facts.append("(fan_on)")


    if world.fan_needed_by_temperature:
        facts.append("(fan_needed_by_temperature)")


    if world.fan_needed_by_air:
        facts.append("(fan_needed_by_air)")


    problem = f"""
(define (problem smart-truck)

    (:domain smart-truck)

    (:init
        {' '.join(facts)}
    )

    (:goal
        (and
            (not (fan_on))
        )
    )
)
"""

    OUTPUT.write_text(problem)
