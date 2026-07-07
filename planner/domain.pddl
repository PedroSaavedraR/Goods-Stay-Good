(define (domain cargo)

(:requirements :strips)

(:predicates
    ;; Temperature
    (high-temp)
    (low-temp)
    (normal-temp)

    ;; Sensors
    (vibration-detected)
    (load-shifted)

    ;; Actuators
    (cooler-on)
    (heater-on)
    (brakes-applied)

    ;; Notification
    (alert-sent)
)

;;Actions temperature based

(:action turn-on-cooler

    :precondition (high-temp)

    :effect (cooler-on)
)

(:action cool-cargo

    :precondition (and (high-temp) (cooler-on))

    :effect (and
        (normal-temp)
        (not (high-temp))
    )
)

(:action turn-off-cooler

    :precondition (and (normal-temp) (cooler-on))

    :effect (not (cooler-on))
)

(:action turn-on-heater

    :precondition (low-temp)

    :effect (heater-on)
)

(:action heat-cargo

    :precondition (and (low-temp) (heater-on))

    :effect (and
        (normal-temp)
        (not (low-temp))
    )
)

(:action turn-off-heater

    :precondition (and (normal-temp) (heater-on))

    :effect (not (heater-on))
)
;;actions safety based

(:action apply-brakes

    :precondition (vibration-detected)

    :effect (brakes-applied)
)

(:action apply-brakes-load

    :precondition (load-shifted)

    :effect (brakes-applied)
)

(:action send-alert

    :precondition (brakes-applied)

    :effect (alert-sent)
)


)