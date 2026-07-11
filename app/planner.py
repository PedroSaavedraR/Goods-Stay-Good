from world_state import world, Temperature, CargoState



def create_plan():

    plan = []


    # -------------------------
    # Temperature management
    # -------------------------

    if world.temperature == Temperature.HOT:

        if not world.fan_on:

            plan.append(
                "turn-on-fan"
            )


    elif world.temperature == Temperature.COLD:

        if not world.heater_on:

            plan.append(
                "turn-on-heater"
            )


    elif world.temperature == Temperature.OK:

        # temperature recovered

        if world.fan_on:

            plan.append(
                "turn-off-fan"
            )


        if world.heater_on:

            plan.append(
                "turn-off-heater"
            )



    # -------------------------
    # Cargo stability
    # -------------------------

    if world.cargo == CargoState.UNSTABLE:

        if not world.warning_on:

            plan.append(
                "turn-on-warning"
            )


    else:

        if world.warning_on:

            plan.append(
                "turn-off-warning"
            )



    return plan
