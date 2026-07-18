from smbus import SMBus

from logger import log


# PCAL9535A

ADDRESS = 0x20

CONFIG0 = 0x06
CONFIG1 = 0x07

OUTPUT0 = 0x02
OUTPUT1 = 0x03


bus = SMBus(1)


# Configure both ports as outputs

bus.write_byte_data(
    ADDRESS,
    CONFIG0,
    0x00
)

bus.write_byte_data(
    ADDRESS,
    CONFIG1,
    0x00
)


#
# Relay mapping:
#
# 1 -> cargo status LED
# 2 -> driving lights
# 3 -> fan
# 4 -> heating lamp
#

OUTPUT_STATE = 0xFF


def _write(value):
    global OUTPUT_STATE

    OUTPUT_STATE = value

    bus.write_byte_data(
        ADDRESS,
        OUTPUT0,
        value
    )


def _set_relay(number, enabled):
    global OUTPUT_STATE

    bit = 1 << (number - 1)

    if enabled:
        # Relay board is active LOW
        OUTPUT_STATE &= ~bit
    else:
        OUTPUT_STATE |= bit

    _write(
        OUTPUT_STATE
    )

    log.info(
        "Relay %s -> %s",
        number,
        enabled
    )


# Public API


def cargo_led_on():
    _set_relay(
        1,
        True
    )


def cargo_led_off():
    _set_relay(
        1,
        False
    )


def driving_lights_on():
    _set_relay(
        2,
        True
    )


def driving_lights_off():
    _set_relay(
        2,
        False
    )


def fan_on():
    _set_relay(
        3,
        True
    )


def fan_off():
    _set_relay(
        3,
        False
    )


def heating_lamp_on():
    _set_relay(
        4,
        True
    )


def heating_lamp_off():
    _set_relay(
        4,
        False
    )
