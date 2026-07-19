from pathlib import Path


OUTPUT = Path(__file__).parent / "problem.pddl"


def generate(world):

    facts = []

    if world.driving_lights_on:
        facts.append("(driving_lights_on)")


    if world.outside_bright_enough:
        facts.append("(outside_bright_enough)")


    problem = f"""
(define (problem smart-truck)

    (:domain smart-truck)

    (:init
        {' '.join(facts)}
    )

    (:goal
        (and
            {
                "(not (driving_lights_on))"
                if world.outside_bright_enough
                else "(driving_lights_on)"
            }
        )
    )
)
"""

    OUTPUT.write_text(problem)
