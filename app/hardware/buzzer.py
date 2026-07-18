import RPi.GPIO as GPIO

from logger import log


PIN = 4
FREQUENCY = 500  # Hz


GPIO.setmode(GPIO.BCM)

GPIO.setup(
    PIN,
    GPIO.OUT
)


_pwm = GPIO.PWM(
    PIN,
    FREQUENCY
)


def on():
    log.info("Buzzer ON")

    _pwm.start(
        50  # duty cycle %
    )


def off():
    log.info("Buzzer OFF")

    _pwm.stop()
