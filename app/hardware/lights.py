import RPi.GPIO as GPIO

from logger import log


# GPIO17
DRIVING_LIGHT_PIN = 18


GPIO.setmode(
    GPIO.BCM
)


GPIO.setup(
    DRIVING_LIGHT_PIN,
    GPIO.OUT
)



def driving_lights_on():

    GPIO.output(
        DRIVING_LIGHT_PIN,
        GPIO.HIGH
    )

    log.info(
        "Driving lights ON"
    )



def driving_lights_off():

    GPIO.output(
        DRIVING_LIGHT_PIN,
        GPIO.LOW
    )

    log.info(
        "Driving lights OFF"
    )
