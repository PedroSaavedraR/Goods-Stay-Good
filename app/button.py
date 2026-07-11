from gpiozero import Button

from world_state import world


# GPIO17 = physical pin 11
button = Button(17)


last_pressed = False



def check_button():

    global last_pressed


    pressed = button.is_pressed


    # rising edge:
    # not pressed -> pressed
    if pressed and not last_pressed:

        print("Cargo checked!")

        world.acknowledge_cargo()


    last_pressed = pressed
