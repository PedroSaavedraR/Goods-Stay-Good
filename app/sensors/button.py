from gpiozero import Button

from world_state import world

from logger import log



PIN = 17



button = Button(
    PIN
)



def cargo_checked():

    log.info(
        "Driver confirmed cargo"
    )


    world.acknowledge_cargo()



button.when_pressed = (
    cargo_checked
)
