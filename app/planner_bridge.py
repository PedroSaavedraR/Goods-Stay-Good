import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

FAST_DOWNWARD = BASE_DIR / "fast-downward"
PLANNER_DIR = BASE_DIR / "planner"


def plan():

    subprocess.run(
        [
            "./fast-downward.py",
            str(PLANNER_DIR / "domain.pddl"),
            str(PLANNER_DIR / "problem.pddl"),
            "--search",
            "astar(lmcut())"
        ],
        cwd=FAST_DOWNWARD,
        check=True,
    )

    plan_file = FAST_DOWNWARD / "sas_plan"

    if not plan_file.exists():
        return None


    with open(plan_file) as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith(";"):
                continue

            action = (
                line
                .replace("(", "")
                .replace(")", "")
            )

            return action.split()[0]

    return None
