import time
import traceback

from world_state import world
from sensor_reader import read
from planner_bridge import create_plan
from executor import Executor
from hardware import apply as hardware_apply
from logger import log


executor = Executor()
last_planned_version = -1


def main():
    log.info("Smart truck starting")

    while True:
        try:
            # 1. Read sensors → update world
            snapshot = read()
            world.apply(snapshot)

            # 2. Replan if world changed or no plan exists
            if world.needs_replan(last_planned_version) or not executor.plan:
                plan = create_plan(world)
                executor.set_plan(plan)
                last_planned_version = world.version

            # 3. Execute one action per tick
            if executor.plan:
                executor.execute_next(world)

            # 4. Mirror world state to physical hardware
            hardware_apply(world)

        except Exception as exc:
            log.error("Main loop error: %s", exc)
            log.debug(traceback.format_exc())

        time.sleep(0.5)


if __name__ == "__main__":
    main()