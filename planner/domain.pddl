(define (domain smart-truck)

    (:requirements
        :strips
        :negative-preconditions
    )


    (:predicates

        ;; ============================
        ;; ENVIRONMENT
        ;; ============================

        (temperature_hot)
        (temperature_ok)
        (temperature_cold)

        (humidity_high)
        (humidity_ok)
        (humidity_low)

        (cargo_stable)
        (cargo_unstable)

        (rear_clear)

        (sun_has_set)


        ;; ============================
        ;; ACTUATORS
        ;; ============================

        (fan_on)

        (heater_on)

        (status_led_on)

        (buzzer_on)

        (driving_lights_on)

    )


    ;; ==================================================
    ;; FAN
    ;; ==================================================

    (:action turn_fan_on

        :precondition
            (and
                (not (fan_on))

                (or
                    (temperature_hot)
                    (humidity_high)
                    (humidity_low)
                )
            )

        :effect
            (fan_on)

    )


    (:action turn_fan_off

        :precondition
            (and
                (fan_on)

                (temperature_ok)

                (humidity_ok)
            )

        :effect
            (not (fan_on))

    )


    ;; ==================================================
    ;; VIRTUAL COOLING EFFECT
    ;;
    ;; Not executed by hardware.
    ;; Represents physics happening.
    ;; ==================================================

    (:action cool_down

        :precondition
            (and
                (fan_on)
                (temperature_hot)
            )

        :effect
            (and
                (temperature_ok)
                (not (temperature_hot))
            )

    )


    ;; ==================================================
    ;; HEATER
    ;; ==================================================

    (:action turn_heater_on

        :precondition
            (and
                (temperature_cold)
                (not (heater_on))
            )

        :effect
            (heater_on)

    )


    (:action turn_heater_off

        :precondition
            (and
                (heater_on)
                (temperature_ok)
            )

        :effect
            (not (heater_on))

    )


    ;; Virtual heating

    (:action heat_up

        :precondition
            (and
                (heater_on)
                (temperature_cold)
            )

        :effect
            (and
                (temperature_ok)
                (not (temperature_cold))
            )

    )


    ;; ==================================================
    ;; HUMIDITY
    ;; ==================================================

    (:action dry_air

        :precondition
            (and
                (fan_on)
                (humidity_high)
            )

        :effect
            (and
                (humidity_ok)
                (not (humidity_high))
            )

    )


    (:action humidify_air

        :precondition
            (and
                (fan_on)
                (humidity_low)
            )

        :effect
            (and
                (humidity_ok)
                (not (humidity_low))
            )

    )


    ;; ==================================================
    ;; CARGO STATUS LED
    ;; ==================================================

    (:action turn_status_led_on

        :precondition
            (cargo_unstable)

        :effect
            (status_led_on)

    )


    (:action turn_status_led_off

        :precondition
            (cargo_stable)

        :effect
            (not (status_led_on))

    )


    ;; ==================================================
    ;; BUZZER
    ;; ==================================================

    (:action turn_buzzer_on

        :precondition
            (not (rear_clear))

        :effect
            (buzzer_on)

    )


    (:action turn_buzzer_off

        :precondition
            (rear_clear)

        :effect
            (not (buzzer_on))

    )


    ;; ==================================================
    ;; LIGHTS
    ;; ==================================================

    (:action turn_lights_on

        :precondition
            (and
                (sun_has_set)
                (not (driving_lights_on))
            )

        :effect
            (driving_lights_on)

    )


    (:action turn_lights_off

        :precondition
            (and
                (not (sun_has_set))
                (driving_lights_on)
            )

        :effect
            (not (driving_lights_on))

    )


)
