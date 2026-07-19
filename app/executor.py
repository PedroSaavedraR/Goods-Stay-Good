from hardware import hardware_manager as hardware


def execute(action, world):

    if action in ("turn_fan_on_temperature", "turn_fan_on_air",):
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

    elif action == "turn_driving_lights_on":
        hardware.driving_lights_on()
        world.driving_lights_enabled()

    elif action == "turn_driving_lights_off":
        hardware.driving_lights_off()
        world.driving_lights_disabled()

    elif action in (
        "cool_down",
        "heat_up",
        "clean_air"
    ):
        # Environment changes.
        # Nothing to trigger.
        pass

    else:
        raise ValueError(
            f"Unknown action: {action}"
        )
