#!/usr/bin/env python3

import logging
import os
from datetime import datetime
from shutil import copyfile
# from gpiozero import MotionSensor
from time import sleep

# from Camera import Camera
from doorbell.Microphone import SpeechRecogniser, AudioCapture
from doorbell.Resident import Resident
from doorbell.Speaker import Speaker
from doorbell.Twitter import TwitterImpl


class Doorbell:

    def __init__(self, residents, microphone, dictophone, speaker,
                 log='logging/smart_doorbell.full.log'):
        if log is None:
            log = self.set_up_logging()
        logging.basicConfig(filename=log, level=logging.DEBUG)

        self.residents = residents
        self.microphone = microphone
        self.dictophone = dictophone
        # self.motion_sensor = MotionSensor(4)
        # self.camera = Camera()
        self.speaker = speaker
        print("SmartDoorbell application is ready. Logs will now be located at ",
              log)

    @staticmethod
    def set_up_logging():
        log_directory = '../logging'
        logging_file_path = 'smart_doorbell.full.log'
        Doorbell.refresh_logs(log_directory, logging_file_path)
        logging_file_name = "{}/{}".format(log_directory, logging_file_path)
        return logging_file_name

    @staticmethod
    def refresh_logs(log_directory, logging_file_path):
        print("Refreshing logging files")
        date_now = datetime.now().date()
        time_now = datetime.now().time()

        print("time: ", time_now)
        archive_log_file_path = "archive-{}-{}-{}" \
            .format(date_now, time_now, logging_file_path)
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
    def run_doorbell_application(self):
        logging.info("Checking the door...")
        # doorbell.motion_sensor.wait_for_motion()
        try:
            logging.info("Somebody is at the door")
            self.speaker.speak_hello()
            resident_recognised = self.doorbell_response()

            # Try again
            if not resident_recognised:
                logging.info("Requested name was not recognised: trying again")
                self.speaker.speak_not_recognised()
                resident_recognised = self.doorbell_response()

            # Default: alert everyone
            if not resident_recognised:
                logging.info("Requested name was not recognised: "
                             "sending general alert")
                for resident in self.residents:
                    resident.request_answer_door()

        except Exception as e:
            logging.error(e)

        # Finished: don't want doorbell inactive if error occurs
        finally:
            # Avoid multiple triggers for same visitor
            sleep(10)

    def doorbell_response(self):
        logging.info("Asking visitor to identify the resident")
        self.speaker.speak_who_do_you_want_to_speak_to()
        resident_name_audio = \
            self.microphone.capture_and_persist_audio('resident-name')
        resident_name_audio_text = \
            self.dictophone.recognise_speech(resident_name_audio)
        if resident_name_audio_text == self.dictophone.UNRECOGNISED:
            logging.info("Resident's name was not recognised")
            return False

        logging.info("Visitor has asked for %s", resident_name_audio_text)
        logging.info("Asking visitor to identify themselves")
        self.speaker.speak_please_say_your_name()
        visitor_name_audio = \
            self.microphone.capture_and_persist_audio('visitor-name')
        visitor_name_audio_text = \
            self.dictophone.recognise_speech(visitor_name_audio)
        logging.info("Visitor's name seems to be %s", visitor_name_audio_text)
        resident_recognised = False
        for resident in self.residents:
            if resident.requested_name_matches_this_resident(resident_name_audio_text):
                resident_recognised = True
                logging.info(resident.text_name +
                             ' was requested by the visitor')

                if resident.is_at_home:
                    resident.request_answer_door()
                else:
                    self.speaker.speak_record_message()
                    recorded_message_text_audio = \
                        self.microphone.capture_and_persist_audio('message')
                    recorded_message_text = \
                        self.dictophone.recognise_speech(recorded_message_text_audio)

                    captured_image = None
                    try:
                        logging.info("Attempting to take photograph")
                        self.speaker.speak_capture_picture()
                        # captured_image = self.camera.capture_still()
                    finally:
                        resident.send_remote_notification(visitor_name_audio_text,
                                                          recorded_message_text,
                                                          captured_image)

        return resident_recognised

    @staticmethod
    def set_up_residents():
        resident_matt = Resident('Matt',
                                 ['matt', 'matty', 'matthew', 'mr ralph', 'matthew ralph'],
                                 TwitterImpl('matt'))
        resident_lydia = Resident('Lydia',
                                  ['Lydia', 'Lid', 'mrs ralph'],
                                  TwitterImpl('lydia'))
        residents = [resident_matt, resident_lydia]
        residents_list_string = ', '.join(str(x.text_name) for x in residents)
        logging.debug("Registered residents: " + residents_list_string)
        return residents


def main():
    residents = Doorbell.set_up_residents()
    microphone = AudioCapture()
    dictophone = SpeechRecogniser()
    # motion_sensor = MotionSensor(4)
    # camera = Camera()
    speaker = Speaker()

    doorbell = Doorbell(residents=residents, microphone=microphone,
                        dictophone=dictophone, speaker=speaker)

    while True:
        doorbell.run_doorbell_application()


if __name__ == "__main__":
    main()
