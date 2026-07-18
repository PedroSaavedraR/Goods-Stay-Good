import time

import RPi.GPIO as GPIO


TRIG = 22
ECHO = 27


GPIO.setmode(
    GPIO.BCM
)


GPIO.setup(
    TRIG,
    GPIO.OUT
)


GPIO.setup(
    ECHO,
    GPIO.IN
)


GPIO.output(
    TRIG,
    False
)



time.sleep(
    0.2
)



def get_distance():

    GPIO.output(
        TRIG,
        True
    )

    time.sleep(
        0.00001
    )

    GPIO.output(
        TRIG,
        False
    )


    start = time.time()
    stop = time.time()



    timeout = (
        time.time()
        +
        0.05
    )


    while GPIO.input(ECHO) == 0:

        start = time.time()

        if time.time() > timeout:

            return None



    timeout = (
        time.time()
        +
        0.05
    )


    while GPIO.input(ECHO) == 1:

        stop = time.time()

        if time.time() > timeout:

            return None



    elapsed = (
        stop - start
    )


    distance = (
        elapsed
        *
        34300
        /
        2
    )


    return round(
        distance,
        2
    )
