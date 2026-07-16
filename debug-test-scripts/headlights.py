#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO

# GPIO18 (BCM numbering)
DRIVING_LIGHT_PIN = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(
    DRIVING_LIGHT_PIN,
    GPIO.OUT
)

try:
    while True:
        print("Headlights ON")
        GPIO.output(
            DRIVING_LIGHT_PIN,
            GPIO.HIGH
        )

        time.sleep(2)

        print("Headlights OFF")
        GPIO.output(
            DRIVING_LIGHT_PIN,
            GPIO.LOW
        )

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping - turning headlights OFF")

    GPIO.output(
        DRIVING_LIGHT_PIN,
        GPIO.LOW
    )

finally:
    GPIO.cleanup()
