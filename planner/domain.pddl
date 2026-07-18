(define (domain heating-cooling)

    (:requirements
        :strips
        :negative-preconditions
    )


    (:predicates
        (fan_on)
        (heater_on)

        (temperature_hot)
        (temperature_ok)
        (temperature_cold)
    )


    (:action turn_fan_on
        :precondition
            (and
                (temperature_hot)
                (not (fan_on))
            )

        :effect
            (and
                (fan_on)
            )
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


    (:action turn_fan_off
        :precondition
            (and
                (temperature_ok)
                (fan_on)
            )

        :effect
            (and
                (not (fan_on))
            )
    )


    (:action turn_heater_on
        :precondition
            (and
                (temperature_cold)
                (not (heater_on))
            )

        :effect
            (and
                (heater_on)
            )
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
            (and
                (not (heater_on))
            )
    )
)
