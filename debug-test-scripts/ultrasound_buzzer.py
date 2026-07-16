import RPi.GPIO as GPIO
import time

# GPIO pins (BCM numbering)
TRIG = 22
ECHO = 27
BUZZER = 4

DISTANCE_LIMIT = 10  # cm
BUZZER_FREQ = 500  # Hz

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

# Create PWM buzzer signal
buzzer_pwm = GPIO.PWM(BUZZER, BUZZER_FREQ)

GPIO.output(TRIG, False)

print("Ultrasonic sensor starting...")
time.sleep(2)


def measure_distance():
    # Trigger ultrasonic pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    # Wait for echo start
    timeout = time.time() + 0.05
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        if time.time() > timeout:
            return None

    # Wait for echo end
    timeout = time.time() + 0.05
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        if time.time() > timeout:
            return None

    # Calculate distance
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2

    return round(distance, 2)


try:
    while True:
        distance = measure_distance()

        if distance is not None:
            if distance < DISTANCE_LIMIT:
                status = "TOO CLOSE - BUZZER ON"
                buzzer_pwm.start(50)  # 50% duty cycle
            else:
                status = "OK"
                buzzer_pwm.stop()

            print(f"Distance: {distance:6.2f} cm | {status}")

        else:
            print("No sensor reading")
            buzzer_pwm.stop()

        time.sleep(0.2)


except KeyboardInterrupt:
    print("\nStopping...")


finally:
    buzzer_pwm.stop()
    GPIO.cleanup()
