from smbus import SMBus

from logger import log


# -----------------------------
# PCAL9535A
# -----------------------------

ADDRESS = 0x20


CONFIG0 = 0x06
CONFIG1 = 0x07

OUTPUT0 = 0x02
OUTPUT1 = 0x03


bus = SMBus(1)


# Configure both ports as output

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



# -----------------------------
# Relay mapping
# -----------------------------

#
# Relay numbers:
#
# 1 -> cargo status LED
# 2 -> buzzer
# 3 -> fan
# 4 -> heating lamp
#


OUTPUT_STATE = 0xFF



def write(value):

    global OUTPUT_STATE

    OUTPUT_STATE = value


    bus.write_byte_data(
        ADDRESS,
        OUTPUT0,
        value
    )



def set_relay(number, enabled):

    global OUTPUT_STATE


    bit = 1 << (number - 1)


    if enabled:

        # Relay board is active LOW

        OUTPUT_STATE &= ~bit


    else:

        OUTPUT_STATE |= bit



    write(
        OUTPUT_STATE
    )


    log.info(
        "Relay %s -> %s",
        number,
        enabled
    )



# -----------------------------
# Public functions
# -----------------------------


def status_led_on():

    set_relay(
        1,
        True
    )


def status_led_off():

    set_relay(
        1,
        False
    )



def buzzer_on():

    set_relay(
        2,
        True
    )


def buzzer_off():

    set_relay(
        2,
        False
    )



def fan_on():

    set_relay(
        3,
        True
    )


def fan_off():

    set_relay(
        3,
        False
    )



def heater_on():

    set_relay(
        4,
        True
    )


def heater_off():

    set_relay(
        4,
        False
    )
