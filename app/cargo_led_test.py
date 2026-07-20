import time

from hardware import hardware_manager as hardware


print("LED ON")
hardware.cargo_led_on()

time.sleep(5)

print("LED OFF")
hardware.cargo_led_off()
