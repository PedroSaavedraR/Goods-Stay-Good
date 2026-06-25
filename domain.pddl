(define (domain room-temperature)

(:requirements :strips)

(:predicates
    (hot)
    (cold)
    (normal)
    (cooler-on)
    (heater-on)
)


(:action turn-on-cooler
    :precondition (hot)
    :effect (cooler-on)
)

(:action cool-room
    :precondition (and (hot) (cooler-on))
    :effect (and
        (normal)
        (not (hot))
    )
)

(:action turn-on-heater
    :precondition (cold)
    :effect (heater-on)
)

(:action heat-room
    :precondition (and (cold) (heater-on))
    :effect (and
        (normal)
        (not (cold))
    )
)

)