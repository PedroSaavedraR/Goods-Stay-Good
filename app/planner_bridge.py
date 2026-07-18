import subprocess


def create_plan():

    subprocess.run(
        [
            "./fast-downward.py",
            "domain.pddl",
            "problem.pddl",
            "--search",
            "astar(lmcut())"
        ],
        cwd="../fast-downward"
    )


    with open(
        "../fast-downward/plan"
    ) as f:

        for line in f:

            if line.startswith(";"):
                continue

            return line.strip().replace(
                ")",
                ""
            ).replace(
                "(",
                ""
            )


    return None
