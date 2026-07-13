"""Hardware layer — mirrors WorldState to physical GPIO/relays."""
from logger import log

# HW modules (will fail gracefully on non-RPi during import)
try:
    from hardware import relay
    from hardware import lights
    from hardware import buzzer
    HW_READY = True
except Exception as exc:
    log.warning("Hardware init failed (expected on non-RPi): %s", exc)
    HW_READY = False


_prev_fan_on: bool | None = None
_prev_heater_on: bool | None = None
_prev_lights_on: bool | None = None
_prev_buzzer_on: bool | None = None
_prev_led_on: bool | None = None


def apply(world):
    """Read WorldState and set physical outputs accordingly."""
    if not HW_READY:
        return

    global _prev_fan_on, _prev_heater_on, _prev_lights_on, _prev_buzzer_on, _prev_led_on

    # Fan
    if world.fan_on != _prev_fan_on:
        if world.fan_on:
            relay.fan_on()
        else:
            relay.fan_off()
        _prev_fan_on = world.fan_on

    # Heater
    if world.heater_on != _prev_heater_on:
        if world.heater_on:
            relay.heater_on()
        else:
            relay.heater_off()
        _prev_heater_on = world.heater_on

    # Driving lights
    if world.driving_lights_on != _prev_lights_on:
        if world.driving_lights_on:
            lights.driving_lights_on()
        else:
            lights.driving_lights_off()
        _prev_lights_on = world.driving_lights_on

    # Buzzer (relay 2)
    if world.buzzer_on != _prev_buzzer_on:
        if world.buzzer_on:
            relay.buzzer_on()
        else:
            relay.buzzer_off()
        _prev_buzzer_on = world.buzzer_on

    # Status LED (relay 1)
    if world.status_led_on != _prev_led_on:
        if world.status_led_on:
            relay.status_led_on()
        else:
            relay.status_led_off()
        _prev_led_on = world.status_led_on