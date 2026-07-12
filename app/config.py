from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    #
    # Environment thresholds
    #

    temperature_cold: float = 15.0
    temperature_hot: float = 28.0

    humidity_low: float = 40.0
    humidity_high: float = 60.0

    rear_distance_min: float = 10.0

    #
    # Timing
    #

    sensor_poll_interval: float = 0.5

    #
    # MQTT
    #

    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_topic: str = "zwave/#"

    #
    # GPIO
    #

    cargo_button_gpio: int = 17

    ultrasonic_trigger_gpio: int = 22
    ultrasonic_echo_gpio: int = 27

    buzzer_gpio: int = 4
    driving_light_gpio: int = 18

    #
    # Internet
    #

    timezone: str = "Europe/Berlin"

    #
    # I²C relay board
    #

    i2c_address: int = 0x20
    relay_count: int = 4


CONFIG = Config()