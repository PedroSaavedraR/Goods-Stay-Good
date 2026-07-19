from . import buzzer
from . import relay


#
# Cargo status LED
#

def cargo_led_on():
    relay.cargo_led_on()
    print("HARDWARE: cargo LED ON")

def cargo_led_off():
    relay.cargo_led_off()


#
# Driving lights
#

def driving_lights_on():
    relay.driving_lights_on()


def driving_lights_off():
    relay.driving_lights_off()


#
# Fan
#

def fan_on():
    relay.fan_on()


def fan_off():
    relay.fan_off()


#
# Heating lamp
#

def heating_lamp_on():
    relay.heating_lamp_on()


def heating_lamp_off():
    relay.heating_lamp_off()


#
# Buzzer
#

def buzzer_on():
    buzzer.on()


def buzzer_off():
    buzzer.off()
