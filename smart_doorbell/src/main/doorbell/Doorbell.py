#!/usr/bin/env python3

#from gpiozero import MotionSensor
from time import sleep
from datetime import datetime
import os
from shutil import copyfile
from Speaker import Speaker
# from Camera import Camera
from Microphone import SpeechRecogniser, AudioCapture
from Resident import Resident

import logging

from Twitter import TwitterImpl


class Doorbell:

    #project_path = "/Users/ralphl01/Dropbox/LYDIA/TECH/BBC-MSc/2018-07_IoT/iot_labs/smart_doorbell/src/main"

    def __init__(self):
        logging_file_name = self.set_up_logging()
        logging.basicConfig(filename=logging_file_name, level=logging.DEBUG)
        self.residents = self.set_up_residents()
        self.microphone = AudioCapture()
        self.dictophone = SpeechRecogniser()
        self.motion_sensor = MotionSensor(14)
        self.speaker = Speaker()
        print("SmartDoorbell application is ready. Logs will now be located at ", logging.basicConfig())

    @staticmethod
    def set_up_logging():
        log_directory = '../logging'
        logging_file_path = 'smart_doorbell.full.log'
        Doorbell.refresh_logs(log_directory, logging_file_path)
        logging_file_name = "{}/{}".format(log_directory, logging_file_path)
        print(logging_file_name)
        return logging_file_name

    @staticmethod
    def set_up_residents():
        resident_matt = Resident('Matt', ['matt.wav', 'matthew.wav', 'mr_ralph.wav', 'matthew_ralph.wav'], TwitterImpl('matt'))
        resident_lydia = Resident('Lydia', ['lydia.wav', 'mrs_ralph.wav', 'lydia_ralph.wav'], TwitterImpl('lydia'))
        # resident_anyone = Resident('Anyone', ['anyone.wav', 'idontmind.wav'])
        residents = [resident_matt, resident_lydia]
        residents_list_string = ', '.join(str(x.text_name) for x in residents)
        logging.debug("Registered residents: " + residents_list_string)
        return residents

    @staticmethod
    def refresh_logs(log_directory, logging_file_path):
        print("Refreshing logging files")
        date_now = datetime.now().date()
        time_now = datetime.now().time()

        print("time: ", time_now)
        archive_log_file_path = "archive-{}-{}-{}".format(date_now, time_now, logging_file_path)
        if not os.path.exists(log_directory):
            print("Creating log directory")
            os.mkdir(log_directory)
        if os.path.exists("{}/{}".format(log_directory, logging_file_path)):
            print("Previous log file exists")
            full_path = "{}/{}".format(log_directory, logging_file_path)
            archive_path = "{}/{}".format(log_directory, archive_log_file_path)
            print("Archiving previous log file")
            copyfile(full_path, archive_path)
            os.remove(full_path)
            print("Finished archiving log file")
            print("Creating new log file...")
            with open(full_path, 'a'):
                os.utime(full_path, None)
            print("New log file is ready to be used")

    def doorbell_response(self):
        print("Asking visitor to identify the resident")
        self.speaker.speak_who_do_you_want_to_speak_to()
        resident_name_audio = self.microphone.capture_audio()
        resident_name_audio_text = self.dictophone.recognise_speech(resident_name_audio)
        if resident_name_audio_text == self.dictophone.UNRECOGNISED:
            print("Resident's name was not recognised")
            return False

        print("Visitor has asked for ", resident_name_audio_text)
        print("Asking visitor to identify themselves")
        self.speaker.speak_please_say_your_name()
        visitor_name_audio = self.microphone.capture_audio()
        visitor_name_audio_text = self.dictophone.recognise_speech(visitor_name_audio)
        print("Visitor's name seems to be ", visitor_name_audio_text)
        resident_recognised = False
        for resident in self.residents:
            if resident.requested_name_matches_this_resident(resident_name_audio_text):
                resident_recognised = True
                logging.info(resident.text_name, ' was requested by the visitor')

                if resident.is_at_home:
                    resident.request_answer_door(visitor_name_audio_text)
                else:
                    self.speaker.speak_record_message()
                    recorded_message_text_audio = self.microphone.capture_audio()
                    recorded_message_text = self.dictophone.recognise_speech(recorded_message_text_audio)
                    self.speaker.speak_capture_picture()
                    captured_image = self.camera.capture_still()

                    resident.send_remote_notification(visitor_name_audio_text,
                                                      recorded_message_text,
                                                      captured_image)

        return resident_recognised


def main():
    doorbell = Doorbell()
    
    print("SmartDoorbell application is ready. Logs will now be located at ", d.logging_file_name)
    while True:
        motion_sensor.wait_for_motion()
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
            logging.debug(e)

        # Finished: don't want doorbell inactive if error occurs
        finally:
            # Avoid multiple triggers for same visitor
            sleep(120)


if __name__ == "__main__":
    main()
