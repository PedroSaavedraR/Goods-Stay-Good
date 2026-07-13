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
        (sun_has_set)
        (fan_on)
        (heater_on)
        (buzzer_on)
        (status_led_on)

    )


    ;
    ; Cooling + humidity (fan serves both)
    ;

    (:action fan_on
        :precondition
            (or
                (temperature_hot)
                (humidity_high)
                (humidity_low)
            )
        :effect
            (fan_on)
    )

    (:action fan_off
        :precondition
            (and
                (temperature_ok)
                (humidity_ok)
            )
        :effect
            (not (fan_on))
    )
    ;
    ; Heating
    ;

    (:action heater_on
        :precondition
            (temperature_cold)
        :effect
            (heater_on)
    )

    (:action heater_off
        :precondition
            (temperature_ok)
        :effect
            (not (heater_on))
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
            (sun_has_set)
        :effect
            (driving_lights_on)
    )

    (:action turn_lights_off
        :precondition
            (not (sun_has_set))
        :effect
            (not (driving_lights_on))
    )


    ;
    ; Buzzer (rear alert)
    ;

    (:action buzzer_on
        :precondition
            (not (rear_clear))
        :effect
            (buzzer_on)
    )

    (:action buzzer_off
        :precondition
            (rear_clear)
        :effect
            (not (buzzer_on))
    )


    ;
    ; Status LED (cargo unchecked indicator)
    ;

    (:action status_led_on
        :precondition
            (cargo_unchecked)
        :effect
            (status_led_on)
    )

    (:action status_led_off
        :precondition
            (cargo_checked)
        :effect
            (not (status_led_on))
    )

)

