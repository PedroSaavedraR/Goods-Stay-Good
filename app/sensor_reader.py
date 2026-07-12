from world_state import Observation

from sensors.mqtt import mqtt_state

from sensors.ultrasonic import get_distance



def read():


    data = mqtt_state.snapshot()



    return Observation(

        temperature=
            data["temperature"],


        humidity=
            data["humidity"],


        illuminance=
            data["illuminance"],


        ultraviolet=
            data["ultraviolet"],


        motion=
            data["motion"],


        motion_timestamp=
            data["motion_timestamp"],


        rear_distance=
            get_distance()
    )
