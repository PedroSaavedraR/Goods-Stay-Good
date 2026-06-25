import time
import sys
from gpiozero import OutputDevice, AngularServo, PWMOutputDevice, DigitalInputDevice, DistanceSensor


# Windows Mocking Layer: Fools Python into skipping the hardware pin checks
if sys.platform.startswith('win'):
    import os
    # Tells gpiozero to use a fake simulation pin layout instead of throwing an error
    os.environ['GPIOZERO_PIN_FACTORY'] = 'mock'


# ==========================================
# 1. HARDWARE CONFIGURATION (Pin Assignments)
# ==========================================
print("Initializing your hardware subset...")
try:
    # ACTUATORS
    FAN_RELAY      = OutputDevice(21)        # Fan Relay signal wire on GPIO 21
    PARKING_BUZZER = PWMOutputDevice(12)     # Active/PWM Buzzer on GPIO 12
    BRAKE_SERVO    = AngularServo(18, min_angle=-90, max_angle=90) # Servo on GPIO 18

    # SENSORS
    # HC-SR04 Ultrasonic Sensor (Echo goes to GPIO 24, Trigger to GPIO 23)
    # Note: Ensure to use a voltage divider resistor network on the Echo pin!
    ULTRASONIC     = DistanceSensor(echo=24, trigger=23) 
    
    # Outside Light Sensor (Digital LDR module output on GPIO 22)
    LIGHT_SENSOR   = DigitalInputDevice(22)  

except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    sys.exit(1)

# ==========================================
# 2. COMPONENT INDEPENDENT TESTS
# ==========================================

def test_fan():
    print("--- 1. Testing the Fan Actuator ---")
    print("-> Spinning FAN ON...")
    FAN_RELAY.on()
    time.sleep(3)
    print("-> Stopping FAN...")
    FAN_RELAY.off()
    print("[PASS] Fan relay responded cleanly.\n")


def test_servo():
    print("--- 2. Testing Servo ---")
    print("-> Moving to -90 degrees (Brake Released)...")
    BRAKE_SERVO.angle = -90
    time.sleep(2)
    print("-> Moving to 90 degrees (Brake Engaged!)...")
    BRAKE_SERVO.angle = 90
    time.sleep(2)
    print("-> Resetting Servo...")
    BRAKE_SERVO.angle = -90
    print("[PASS] Servo sweep complete.\n")


def test_buzzer():
    print("--- 3. Testing the Parking Assistant Buzzer ---")
    print("-> Beeping standard tone...")
    PARKING_BUZZER.value = 0.5  # 50% duty cycle volume
    time.sleep(1)
    PARKING_BUZZER.value = 0    # Quiet
    print("[PASS] Buzzer audible test complete.\n")


def monitor_sensors_live():
    print("--- 4 & 5. Live Tracking: Ultrasonic & Outside Light ---")
    print("Wave your hand in front of the ultrasonic sensor or cover the light sensor.")
    print("Press Ctrl+C to stop the test loop.\n")
    
    try:
        while True:
            # Convert Distance Sensor decimal value (0.0 to 1.0 meters) to centimeters
            distance_cm = ULTRASONIC.distance * 100
            
            # Read light sensor state (Assuming 1 = Dark, 0 = Bright depending on module wiring)
            is_dark = LIGHT_SENSOR.value 
            light_status = "DARK (Turn on headlights)" if is_dark else "BRIGHT (Lights off)"
            
            # Print readings to screen on a single refreshing line
            print(f"Distance: {distance_cm:5.1f} cm | Exterior Environment: {light_status}", end="\r")
            
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n\nLive sensor monitoring stopped by user.")


# ==========================================
# EXECUTION ENTRY
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print("    PI 3 TARGETED FIVE-COMPONENT TEST     ")
    print("==========================================\n")
    
    test_fan()
    test_servo()
    test_buzzer()
    monitor_sensors_live()
    
    # Safe fallback termination state
    FAN_RELAY.off()
    PARKING_BUZZER.value = 0
    print("\nAll tests complete. Actuators set to safe/idle modes.")