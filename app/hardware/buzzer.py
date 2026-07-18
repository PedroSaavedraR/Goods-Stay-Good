import RPi.GPIO as GPIO


PIN = 18
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
    _pwm.start(
        50  # duty cycle %
    )


def off():
    _pwm.stop()
