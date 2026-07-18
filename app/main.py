import time
import traceback

from world_state import world
from sensor_reader import read
from planner_bridge import create_plan
from executor import Executor
from hardware import apply as hardware_apply
from logger import log

executor = Executor()

def main():
    log.info("Smart truck starting")

    while True:
        try:
            # =====================================
            # 1. SENSOR UPDATE
            # =====================================
            snapshot = read()

            world.apply(snapshot)

            log.info(
                "World: %s",
                world.predicates()
            )

            # =====================================
            # 2. ALWAYS PLAN
            # =====================================

            plan = create_plan(world)

            log.info(
                "New plan: %s",
                plan
            )

            executor.set_plan(plan)

            # =====================================
            # 3. EXECUTE ONE ACTION
            # =====================================

            if executor.plan:
                executor.execute_next(world)

            # =====================================
            # 4. HARDWARE MIRROR
            # =====================================

            hardware_apply(world)

        except Exception as exc:
            log.error(
                "Main loop error: %s",
                exc
            )
            log.debug(
                traceback.format_exc()
            )
        time.sleep(0.5)


if __name__ == "__main__":
    main()
