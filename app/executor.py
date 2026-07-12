from logger import log

from hardware import relay
from hardware import lights


class Executor:


    def __init__(self):

        self.plan = []


    def set_plan(self, plan):

        self.plan = plan

        log.info(
            "New plan: %s",
            plan
        )



    def execute_next(self, world):

        if not self.plan:
            return


        action = self.plan.pop(0)


        log.info(
            "Executing %s",
            action
        )


        if action == "fan_on":

            relay.fan_on()

            world.fan_on = True



        elif action == "fan_off":

            relay.fan_off()

            world.fan_on = False



        elif action == "heater_on":

            relay.heater_on()

            world.heater_on = True



        elif action == "heater_off":

            relay.heater_off()

            world.heater_on = False


        elif action == "driving_lights_on":

            lights.driving_lights_on()

            world.driving_lights_on = True



        elif action == "driving_lights_off":

            lights.driving_lights_off()

            world.driving_lights_on = False


        elif action == "check_cargo":

            world.acknowledge_cargo()




