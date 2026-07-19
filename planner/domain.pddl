(define (domain smart-truck)

    (:requirements
        :strips
        :negative-preconditions
    )


    (:predicates
        (fan_on)
        (heater_on)

        (fan_needed_by_temperature)
        (fan_needed_by_air)

        (temperature_hot)
        (temperature_ok)
        (temperature_cold)

        (bad_air)

        (driving_lights_on)
        (outside_bright_enough)

        (buzzer_on)
        (rear_clear)
    )


    ; -------------------------
    ; Driving lights control
    ; -------------------------

    (:action turn_driving_lights_on

        :precondition
            (and
                (not (outside_bright_enough))
                (not (driving_lights_on))
            )

        :effect
            (driving_lights_on)
    )


    (:action turn_driving_lights_off

        :precondition
            (and
                (outside_bright_enough)
                (driving_lights_on)
            )

        :effect
            (not (driving_lights_on))
    )


    ; -------------------------
    ; Rear obstacle warning
    ; -------------------------

    (:action turn_buzzer_on

        :precondition
            (and
                (not (rear_clear))
                (not (buzzer_on))
            )

        :effect
            (buzzer_on)
    )


    (:action drive_away

        :precondition
            (and
                (not (rear_clear))
                (buzzer_on)
            )

        :effect
            (rear_clear)
    )


    (:action turn_buzzer_off

        :precondition
            (and
                (rear_clear)
                (buzzer_on)
            )

        :effect
            (not (buzzer_on))
    )

    ; -------------------------
    ; Fan control
    ; -------------------------

    (:action turn_fan_on_temperature

        :precondition
            (and
                (fan_needed_by_temperature)
                (not (fan_on))
            )

        :effect
            (fan_on)
    )


    (:action turn_fan_on_air

        :precondition
            (and
                (fan_needed_by_air)
                (not (fan_on))
            )

        :effect
            (fan_on)
    )


    (:action cool_down

        :precondition
            (and
                (fan_needed_by_temperature)
                (fan_on)
            )

        :effect
            (not (fan_needed_by_temperature))
    )


    (:action clean_air

        :precondition
            (and
                (fan_needed_by_air)
                (fan_on)
            )

        :effect
            (not (fan_needed_by_air))
    )


    (:action turn_fan_off

        :precondition
            (and
                (not (fan_needed_by_temperature))
                (not (fan_needed_by_air))
                (fan_on)
            )

        :effect
            (not (fan_on))
    )


    ; -------------------------
    ; Heater control
    ; -------------------------

    (:action turn_heater_on
        :precondition
            (and
                (temperature_cold)
                (not (heater_on))
            )

        :effect
            (heater_on)
    )


    (:action heat_up
        :precondition
            (and
                (temperature_cold)
                (heater_on)
            )

        :effect
            (and
                (temperature_ok)
                (not (temperature_cold))
            )
    )


    (:action turn_heater_off
        :precondition
            (and
                (temperature_ok)
                (heater_on)
            )

        :effect
            (not (heater_on))
    )

)
