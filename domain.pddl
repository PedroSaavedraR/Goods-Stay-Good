(define (domain cargo-truck)

    (:requirements
        :strips
        :negative-preconditions
    )


    (:predicates
        (fan_on)
        (heater_on)
	(obstacle_near)
        (buzzer_on)

        (temperature_hot)
        (temperature_ok)
        (temperature_cold)

        (bad_air)
    )


    ; -------------------------
    ; Fan control
    ; -------------------------

    (:action turn_fan_on_temperature
        :precondition
            (and
                (temperature_hot)
                (not (fan_on))
            )

        :effect
            (fan_on)
    )


    (:action turn_fan_on_air
        :precondition
            (and
                (bad_air)
                (not (fan_on))
            )

        :effect
            (fan_on)
    )


    (:action cool_down
        :precondition
            (and
                (temperature_hot)
                (fan_on)
            )

        :effect
            (and
                (temperature_ok)
                (not (temperature_hot))
            )
    )


    (:action clean_air
        :precondition
            (and
                (bad_air)
                (fan_on)
            )

        :effect
            (not (bad_air))
    )


    (:action turn_fan_off
        :precondition
            (and
                (temperature_ok)
                (not (bad_air))
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

    ; -------------------------
    ; Ultrasonic-sensor
    ; -------------------------
    
    (:action turn_buzzer_on
        :precondition
            (and
                (obstacle_near)
                (not (buzzer_on))
            )

        :effect
            (buzzer_on)
    )

)

