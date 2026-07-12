import RPi.GPIO as GPIO

from logger import log


PIN = 4


GPIO.setmode(
    GPIO.BCM
)

GPIO.setup(
    PIN,
    GPIO.OUT
)


_pwm = GPIO.PWM(
    PIN,
    500
)



def start():

    log.info(
        "Buzzer ON"
    )

    _pwm.start(
        50
    )



def stop():

    log.info(
        "Buzzer OFF"
    )

    _pwm.stop()
