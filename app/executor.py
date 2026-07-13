from logger import log


class Executor:

    def __init__(self):
        self.plan: list[str] = []

    def set_plan(self, plan: list[str]):
        self.plan = list(plan)
        log.info("New plan: %s", self.plan)

    def execute_next(self, world):
        if not self.plan:
            return

        action = self.plan.pop(0)
        log.info("Executing %s", action)

        if action == "fan_on":
            world.fan_on = True

        elif action == "fan_off":
            world.fan_on = False

        elif action == "heater_on":
            world.heater_on = True

        elif action == "heater_off":
            world.heater_on = False

        elif action == "turn_lights_on":
            world.driving_lights_on = True

        elif action == "turn_lights_off":
            world.driving_lights_on = False

        elif action == "check_cargo":
            world.acknowledge_cargo()

        elif action == "buzzer_on":
            world.buzzer_on = True

        elif action == "buzzer_off":
            world.buzzer_on = False

        elif action == "status_led_on":
            world.status_led_on = True

        elif action == "status_led_off":
            world.status_led_on = False

        else:
            log.warning("Unknown action: %s", action)

        world.version += 1