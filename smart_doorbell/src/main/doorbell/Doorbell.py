#!/usr/bin/env python3

# from gpiozero import Button, MotionSensor
from time import sleep
from doorbell.Speaker import Speaker
# from doorbell.Camera import Camera
from doorbell.Microphone import Microphone
from doorbell.Resident import Resident

import logging


def main():
    # GENERAL CONFIG
    logging.basicConfig(filename='../logging/smart_doorbell.full.log', level=logging.DEBUG)
    doorbell_active = False

    # COMPONENTS
    # doorbell_button = Button(4, pull_up=False)
    # motion_sensor = MotionSensor(8, pull_up=False)
    speaker = Speaker()
    microphone = Microphone()

    # RESIDENTS
    resident_matt = Resident('Matt', ['matt.wav', 'matthew.wav', 'mr_ralph.wav'])
    resident_lydia = Resident('Lydia', ['lydia.wav', 'mrs_ralph.wav'])
    resident_anyone = Resident('Anyone', ['anyone.wav', 'idontmind.wav'])
    residents = [resident_matt, resident_lydia, resident_anyone]
    logging.debug("Registered residents: ", residents)

    while not doorbell_active:
        logging.debug('Checking for activity... ')
        # if doorbell_button.is_pressed() \
        #         or motion_sensor.is_activated():
        #     doorbell_active = True

        if doorbell_active:
            try:
                logging.info("Pressed!")
                resident_recognised = False
                speaker.speak_hello()
                resident_recognised = doorbell_response(microphone, resident_recognised, residents, speaker)

                # Try again
                if not resident_recognised:
                    logging.warning("Requested name was not recognised: trying again")
                    speaker.speak_not_recognised()
                    resident_recognised = doorbell_response(microphone, resident_recognised, residents, speaker)

                # Default: alert everyone
                if not resident_recognised:
                    logging.warning("Requested name was not recognised: requesting anyone to answer the door")
                    resident_anyone.request_answer_door()

            # Finished: don't want doorbell inactive if error occurs
            finally:
                # Avoid multiple triggers for same visitor
                sleep(120)
                doorbell_active = False


def doorbell_response(microphone, resident_recognised, residents, speaker):
    speaker.speak_resident_name()
    resident_name_audio = microphone.listen()
    speaker.speak_visitor_name()
    visitor_name_audio = microphone.listen()
    for resident in residents:
        if resident.requested_name_matches_this_resident(resident_name_audio):
            resident_recognised = True
            logging.info(resident.text_name, ' was requested by the visitor')
            resident.alert_visitor_at_door(visitor_name_audio)

    return resident_recognised


if __name__ == "__main__":
    main()
