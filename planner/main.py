from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


DOMAIN = PROJECT_ROOT / "planner" / "domain.pddl"

PROBLEM = PROJECT_ROOT / "planner" / "problem.pddl"



def create_problem(world):


    symbols = world.symbols()



    facts = []


    for symbol in symbols:

        facts.append(
            f"({symbol})"
        )



    goal = """

        (and

            (rear_clear)

            (cargo_checked)

            (temperature_ok)

            (humidity_ok)

        )

    """



    content = f"""

(define (problem truck_problem)

    (:domain smart-truck)


    (:init

        {' '.join(facts)}

    )


    (:goal

        {goal}

    )

)

"""


    PROBLEM.write_text(
        content
    )



    return PROBLEM
