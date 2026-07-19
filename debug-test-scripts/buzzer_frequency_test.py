import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
PIN = 18

GPIO.setup(PIN, GPIO.OUT)

try:
    print("Testing simple ON/OFF output on GPIO 18...")
    for i in range(3):
        GPIO.output(PIN, GPIO.HIGH)
        print(f"ON {i + 1}")
        time.sleep(1)
        GPIO.output(PIN, GPIO.LOW)
        print("OFF")
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted")
finally:
    GPIO.output(PIN, GPIO.LOW)
    GPIO.cleanup(PIN)
