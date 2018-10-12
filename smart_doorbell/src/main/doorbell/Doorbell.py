#!/usr/bin/env python3

#from gpiozero import MotionSensor
from time import sleep
from datetime import datetime
import os
from shutil import copyfile
from doorbell.Speaker import Speaker
# from Camera import Camera
from doorbell.Microphone import MicrophoneImpl
from doorbell.Resident import Resident

import logging


class Doorbell:

    project_path = "/Users/ralphl01/Dropbox/LYDIA/TECH/BBC-MSc/2018-07_IoT/iot_labs/smart_doorbell/src/main"

    def __init__(self):
        self.log = self.set_up_logging()
        self.residents = self.set_up_residents()
        self.microphone = MicrophoneImpl()
        #self.motion_sensor = MotionSensor(4)
        self.speaker = Speaker()
        print("SmartDoorbell application is ready. Logs will now be located at ", self.log.basicConfig())

    @staticmethod
    def set_up_logging():
        log_directory = '../logging'
        logging_file_path = 'smart_doorbell.full.log'
        Doorbell.refresh_logs(log_directory, logging_file_path)
        logging_file_name = "{}/{}".format(log_directory, logging_file_path)
        print(logging_file_name)
        logging.basicConfig(filename=logging_file_name, level=logging.DEBUG)
        return logging

    @staticmethod
    def set_up_residents():
        resident_matt = Resident('Matt', ['matt.wav', 'matthew.wav', 'mr_ralph.wav', 'matthew_ralph.wav'])
        resident_lydia = Resident('Lydia', ['lydia.wav', 'mrs_ralph.wav', 'lydia_ralph.wav'])
        # resident_anyone = Resident('Anyone', ['anyone.wav', 'idontmind.wav'])
        residents = [resident_matt, resident_lydia]
        residents_list_string = ', '.join(str(x.text_name) for x in residents)
        logging.debug("Registered residents: " + residents_list_string)
        return residents

    @staticmethod
    def refresh_logs(log_directory, logging_file_path):
        print("Refreshing logging files")
        time_now = datetime.now().time()
        print("time: ", time_now)
        archive_log_file_path = "archive-{}-{}".format(time_now, logging_file_path)
        if not os.path.exists(log_directory):
            print("Creating log directory")
            os.mkdir(log_directory)
        if os.path.exists("{}/{}".format(log_directory, logging_file_path)):
            print("Previous log file exists")
            full_path = "{}/{}".format(log_directory, logging_file_path)
            archive_path = "{}/{}".format(log_directory, archive_log_file_path)
            print("Archiving previous log file")
            copyfile(full_path, archive_path)
            print("Finished archiving log file")
            os.remove(full_path)
            print("Finished removing old log file")

    def doorbell_response(self):
        self.speaker.speak_resident_name()
        resident_name_audio_text = self.microphone.recognise_speech()
        self.speaker.speak_visitor_name()
        visitor_name_audio_text = self.microphone.recognise_speech()
        resident_recognised = False
        for resident in self.residents:
            if resident.requested_name_matches_this_resident(resident_name_audio_text):
                resident_recognised = True
                logging.info(resident.text_name, ' was requested by the visitor')
                resident.alert_visitor_at_door(visitor_name_audio_text)

        return resident_recognised


def main():
    doorbell = Doorbell()

    while True:
        #doorbell.motion_sensor.wait_for_motion()
        sleep(10)
        try:
            logging.info("Somebody is at the door")
            doorbell.speaker.speak_hello()
            resident_recognised = doorbell.doorbell_response()

            # Try again
            if not resident_recognised:
                logging.warning("Requested name was not recognised: trying again")
                doorbell.speaker.speak_not_recognised()
                resident_recognised = doorbell.doorbell_response()

            # Default: alert everyone
            if not resident_recognised:
                logging.warning("Requested name was not recognised: sending general alert")
                for resident in doorbell.residents:
                    resident.request_answer_door()

        # TODO: Decide what to do about exceptions.
        except Exception as e:
            print(e)

        # Finished: don't want doorbell inactive if error occurs
        finally:
            # Avoid multiple triggers for same visitor
            sleep(120)


if __name__ == "__main__":
    main()
