from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROBLEM = PROJECT_ROOT / "planner" / "problem.pddl"


def create_problem(world):

    facts = []

    for predicate in sorted(world.predicates()):
        facts.append(
            f"({predicate})"
        )


    content = f"""
(define (problem smart-truck-problem)

    (:domain smart-truck)


    (:init

        {' '.join(facts)}

    )


    (:goal

        (and

            (cargo_stable)

            (temperature_ok)

            (humidity_ok)

            (drive_safe)

        )

    )

)
"""


    PROBLEM.write_text(content)

    return PROBLEM
