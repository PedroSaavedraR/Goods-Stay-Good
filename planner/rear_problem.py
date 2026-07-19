from pathlib import Path


OUTPUT = Path(__file__).parent / "problem.pddl"


def generate(world):

    facts = []

    if world.buzzer_on:
        facts.append("(buzzer_on)")


    if world.rear_clear:
        facts.append("(rear_clear)")


    problem = f"""
(define (problem smart-truck)

    (:domain smart-truck)

    (:init
        {' '.join(facts)}
    )

    (:goal
        (and
            (rear_clear)
            (not (buzzer_on))
        )
    )
)
"""

    OUTPUT.write_text(problem)
