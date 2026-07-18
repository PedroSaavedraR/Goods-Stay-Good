from hardware import hardware_manager as hardware


def execute(action, world):

    if action == "turn_fan_on":
        hardware.fan_on()
        world.fan_enabled()

    elif action == "turn_fan_off":
        hardware.fan_off()
        world.fan_disabled()

    elif action == "turn_heater_on":
        hardware.heating_lamp_on()
        world.heater_enabled()

    elif action == "turn_heater_off":
        hardware.heating_lamp_off()
        world.heater_disabled()

    elif action in (
        "cool_down",
        "heat_up"
    ):
        # Environment changes.
        # Nothing to trigger.
        pass

    else:
        raise ValueError(
            f"Unknown action: {action}"
        )
