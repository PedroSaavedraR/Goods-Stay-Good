import time


from world_state import world

from sensor_reader import read

from planner_bridge import create_plan

from executor import Executor

from logger import log


executor = Executor()
last_planned_version = -1


def main():

    log.info(
        "Smart truck starting"
    )


    while True:


        observation = read()


        world.update(
            observation
        )


        # only create a new plan
        # when required

        if (
            world.needs_replan(last_planned_version)
            or not executor.plan
        ):

            plan = create_plan(
                world
            )

            executor.set_plan(
                plan
            )

            last_planned_version = world.version



        # one action only

        if executor.plan:

            executor.execute_next(
                world
            )

        time.sleep(
            0.5
        )



if __name__ == "__main__":

    main()
        )



if __name__ == "__main__":

    main()
