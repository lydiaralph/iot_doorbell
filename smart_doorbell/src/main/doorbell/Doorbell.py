#!/usr/bin/env python3

from gpiozero import Button, MotionSensor
from time import sleep
from datetime import datetime
import os
from shutil import copyfile
from doorbell.Speaker import Speaker
# from Camera import Camera
from doorbell.Microphone import MicrophoneImpl
from doorbell.Resident import Resident

import logging


def main():
    # GENERAL CONFIG
    log_directory = '../logging'
    logging_file_path = 'smart_doorbell.full.log'
    refresh_logs(log_directory, logging_file_path)

    logging_file_name = "{}/{}".format(log_directory,logging_file_path)
    print(logging_file_name)
    logging.basicConfig(filename=logging_file_name, level=logging.DEBUG)

    # COMPONENTS
    # doorbell_button = Button(4, pull_up=False)
    motion_sensor = MotionSensor(4)
    speaker = Speaker()
    microphone = MicrophoneImpl()

    # RESIDENTS
    resident_matt = Resident('Matt', ['matt.wav', 'matthew.wav', 'mr_ralph.wav'])
    resident_lydia = Resident('Lydia', ['lydia.wav', 'mrs_ralph.wav'])
    resident_anyone = Resident('Anyone', ['anyone.wav', 'idontmind.wav'])
    residents = [resident_matt, resident_lydia, resident_anyone]
    residents_list_string = ', '.join(str(x.text_name) for x in residents)
    logging.debug("Registered residents: " + residents_list_string)

    print("SmartDoorbell application is ready. Logs will now be located at ", logging_file_name)
    while True:
        motion_sensor.wait_for_motion()
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

        # TODO: Decide what to do about exceptions.
        except Exception as e:
            print(e)

        # Finished: don't want doorbell inactive if error occurs
        finally:
        # Avoid multiple triggers for same visitor
            sleep(120)


def doorbell_response(microphone, resident_recognised, residents, speaker):
    speaker.speak_resident_name()
    resident_name_audio_text = microphone.recognise_speech()
    speaker.speak_visitor_name()
    visitor_name_audio_text = microphone.recognise_speech()
    for resident in residents:
        if resident.requested_name_matches_this_resident(resident_name_audio_text):
            resident_recognised = True
            logging.info(resident.text_name, ' was requested by the visitor')
            resident.alert_visitor_at_door(visitor_name_audio_text)

    return resident_recognised

def refresh_logs(log_directory, logging_file_path):
    print("Refreshing logging files")

    time_now = datetime.now().time()
    print("time: ", time_now)
    archive_log_file_path = "archive-{}-{}".format(time_now, logging_file_path)
    if os.path.exists("{}/{}".format(log_directory,logging_file_path)):
        print("Previous log file exists")
        full_path = "{}/{}".format(log_directory,logging_file_path)
        archive_path = "{}/{}".format(log_directory,archive_log_file_path)
        print("Archiving previous log file")
        copyfile(full_path, archive_path)
        print("Finished archiving log file")
        os.remove(full_path)
        print("Finished removing old log file")
    else:
        print("Creating log directory")
        os.mkdir(log_directory)
    

if __name__ == "__main__":
    main()