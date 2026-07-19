from pathlib import Path


OUTPUT = Path(__file__).parent / "problem.pddl"


def generate(world):

    facts = []


    if world.cargo_might_be_unstable:
        facts.append(
            "(cargo_might_be_unstable)"
        )


    if world.cargo_led_on:
        facts.append(
            "(cargo_led_on)"
        )


    problem = f"""
(define (problem smart-truck)

    (:domain smart-truck)

    (:init
        {' '.join(facts)}
    )

    (:goal
        (and
            (not (cargo_might_be_unstable))
            (not (cargo_led_on))
        )
    )
)
"""


    OUTPUT.write_text(problem)
