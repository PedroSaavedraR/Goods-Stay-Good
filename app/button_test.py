import time

import RPi.GPIO as GPIO

from hardware import hardware_manager as hardware


BUTTON_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(
    BUTTON_PIN,
    GPIO.IN,
    pull_up_down=GPIO.PUD_UP,
)


led_on = False
last_toggle = time.time()

print("Button test running.")
print("LED toggles every 10 s.")
print("Press button to turn LED OFF.")
print("CTRL+C to quit.")

try:
    while True:

        now = time.time()

        # Every 10 seconds: turn LED on
        if now - last_toggle >= 10:
            hardware.cargo_led_on()
            led_on = True
            last_toggle = now
            print("LED ON")

        # Poll button
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:

            if led_on:
                hardware.cargo_led_off()
                led_on = False
                print("BUTTON -> LED OFF")

            # Wait until button released
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.02)

            # Debounce
            time.sleep(0.2)

        time.sleep(0.02)

except KeyboardInterrupt:
    pass

finally:
    hardware.cargo_led_off()
    GPIO.cleanup()
