from smbus import SMBus

ADDRESS = 0x20

CONFIG0 = 0x06
CONFIG1 = 0x07
OUTPUT0 = 0x02
OUTPUT1 = 0x03

bus = SMBus(1)

# Configure expander pins as outputs
bus.write_byte_data(ADDRESS, CONFIG0, 0x00)
bus.write_byte_data(ADDRESS, CONFIG1, 0x00)


def set_outputs(value):
    """
    value:
    bit 0 -> relay 1
    bit 1 -> relay 2
    bit 2 -> relay 3
    bit 3 -> relay 4
    """

    bus.write_byte_data(ADDRESS, OUTPUT0, value)


def relay_on(number):
    """
    number: 1-4
    """

    current = 0x0F
    current &= ~(1 << (number - 1))

    set_outputs(current)


def relay_off(number):
    current = 0x0F
    set_outputs(current)


def all_off():
    set_outputs(0x0F)


if __name__ == "__main__":
    import time

    print("Relay 1 ON")
    relay_on(1)

    time.sleep(5)

    print("Relay 1 OFF")
    relay_off(1)
