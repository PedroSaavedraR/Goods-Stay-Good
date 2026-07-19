import RPi.GPIO as GPIO
from datetime import datetime


PIN = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(
    PIN,
    GPIO.IN,
    pull_up_down=GPIO.PUD_UP
)


last_pressed = None
last_state = GPIO.HIGH


def update():

    global last_pressed
    global last_state

    current = GPIO.input(PIN)


    # detect falling edge manually
    if (
        last_state == GPIO.HIGH
        and current == GPIO.LOW
    ):
        last_pressed = datetime.now()

        print(
            "Cargo button pressed:",
            last_pressed
        )


    last_state = current



def get_last_pressed():
    return last_pressed
