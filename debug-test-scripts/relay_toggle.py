#!/usr/bin/env python3

import time
from smbus import SMBus

# PCAL9535A
ADDRESS = 0x20

CONFIG0 = 0x06
CONFIG1 = 0x07
OUTPUT0 = 0x02

bus = SMBus(1)

# Configure both ports as outputs
bus.write_byte_data(ADDRESS, CONFIG0, 0x00)
bus.write_byte_data(ADDRESS, CONFIG1, 0x00)

# Relay board is active LOW
ALL_ON = 0x00   # All relay outputs low -> all relays ON
ALL_OFF = 0xFF  # All relay outputs high -> all relays OFF

try:
    while True:
        print("Turning On")
        bus.write_byte_data(ADDRESS, OUTPUT0, ALL_ON)
        time.sleep(2)

        print("Turning Off")
        bus.write_byte_data(ADDRESS, OUTPUT0, ALL_OFF)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nExiting - turning all relays off.")
    bus.write_byte_data(ADDRESS, OUTPUT0, ALL_OFF)
