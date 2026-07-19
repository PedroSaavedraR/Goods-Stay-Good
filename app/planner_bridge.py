import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

FAST_DOWNWARD = BASE_DIR / "fast-downward"
PLANNER_DIR = BASE_DIR / "planner"


def plan():

    try:

        result = subprocess.run(
            [
                "./fast-downward.py",
                str(PLANNER_DIR / "domain.pddl"),
                str(PLANNER_DIR / "problem.pddl"),
                "--search",
                "astar(lmcut())",
            ],
            cwd=FAST_DOWNWARD,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


        # Planner failed or found no solution
        if result.returncode != 0:
            return None


    except Exception:
        return None


    plan_file = FAST_DOWNWARD / "sas_plan"


    if not plan_file.exists():
        return None


    with open(plan_file) as f:

        for line in f:

            line = line.strip()


            if not line or line.startswith(";"):
                continue


            if line.startswith("("):

                action = (
                    line
                    .replace("(", "")
                    .replace(")", "")
                    .strip()
                )

                return action.split()[0]


    return None
