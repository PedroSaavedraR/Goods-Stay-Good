#!/usr/bin/env python3

from smbus import SMBus
import time

ADDR = 0x20
bus = SMBus(1)

# PCAL9535A registers
CONFIG0 = 0x06
CONFIG1 = 0x07
OUTPUT0 = 0x02
OUTPUT1 = 0x03

# Set both ports as outputs
bus.write_byte_data(ADDR, CONFIG0, 0x00)
bus.write_byte_data(ADDR, CONFIG1, 0x00)

def write_outputs(port0, port1):
    bus.write_byte_data(ADDR, OUTPUT0, port0)
    bus.write_byte_data(ADDR, OUTPUT1, port1)

print("All relays ON")
write_outputs(0x00, 0x00)
time.sleep(3)

print("All relays OFF")
write_outputs(0xff, 0xff)
time.sleep(2)

print("Cycling outputs")

for i in range(4):
    print("Relay", i + 1, "ON")

    # Try first four bits on port 0
    write_outputs(~(1 << i) & 0xff, 0xff)

    time.sleep(1)

    print("OFF")
    write_outputs(0xff, 0xff)

    time.sleep(1)

print("Done")
