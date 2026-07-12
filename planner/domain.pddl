(define (domain smart-truck)

    (:requirements
        :strips
    )


    (:predicates

        (temperature_ok)
        (temperature_hot)
        (temperature_cold)

        (humidity_ok)
        (humidity_high)
        (humidity_low)

        (cargo_checked)
        (cargo_unchecked)

        (rear_clear)

        (driving_lights_on)
        (bright_enough)

        (fan_on)
        (heater_on)

    )


    ;
    ; Cooling
    ;

    (:action fan_on

        :precondition
            (temperature_hot)

        :effect
            (and
                (fan_on)
            )
    )


    (:action fan_off

        :precondition
            (temperature_ok)

        :effect
            (and
                (not (fan_on))
            )
    )



    ;
    ; Heating
    ;

    (:action heater_on

        :precondition
            (temperature_cold)

        :effect
            (and
                (heater_on)
            )
    )



    (:action heater_off

        :precondition
            (temperature_ok)

        :effect
            (and
                (not (heater_on))
            )
    )



    ;
    ; Humidity control
    ;

    (:action humidity_fan_on

        :precondition
            (or
                (humidity_high)
                (humidity_low)
            )

        :effect
            (fan_on)

    )



    ;
    ; Cargo
    ;

    (:action check_cargo

        :precondition
            (cargo_unchecked)

        :effect
            (and
                (cargo_checked)
                (not (cargo_unchecked))
            )
    )



    ;
    ; Driving lights
    ;

    (:action turn_lights_on

        :precondition
            (not
                (bright_enough)
            )

        :effect
            (driving_lights_on)
    )

)
