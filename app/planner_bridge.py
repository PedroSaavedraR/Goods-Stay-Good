import sys
from pathlib import Path
# Ensure project root is on sys.path so 'import planner.main' works
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import subprocess


from planner.main import create_problem


FAST_DOWNWARD = (
    PROJECT_ROOT
    /
    "fast-downward"
    /
    "fast-downward.py"
)



DOMAIN = (
    PROJECT_ROOT
    /
    "planner"
    /
    "domain.pddl"
)




def create_plan(world):


    problem = create_problem(
        world
    )



    result = subprocess.run(

        [

            "python3",

            str(FAST_DOWNWARD),

            str(DOMAIN),

            str(problem),

            "--search",

            "astar(lmcut)"

        ],

        capture_output=True,

        text=True

    )



    if result.returncode != 0:

        print(
            result.stderr
        )

        return []



    actions = []



    reading = False



    for line in result.stdout.splitlines():


        if "Plan:" in line:

            reading = True

            continue



        if reading:


            line = line.strip()


            if not line:

                continue



            if line[0].isdigit():

                action = (
                    line
                    .split(":")[1]
                    .strip()
                )


                actions.append(
                    action.strip("()")
                )



    return actions
