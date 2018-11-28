import logging
from configparser import ConfigParser, ExtendedInterpolation

import simpleaudio as sa


class Speaker:
    def __init__(self, cfg='../resources/doorbell.properties', log='../logging/smart_doorbell.full.log'):
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(cfg)
        logging.basicConfig(filename=log, level=logging.DEBUG)

    def speak_hello(self):
        self.speak_sound('soundfile_hello')

    def speak_goodbye(self):
        self.speak_sound('soundfile_goodbye')

    def speak_not_recognised(self):
        self.speak_sound('soundfile_not_recognised')

    def speak_record_message(self):
        self.speak_sound('soundfile_record_message')

    def speak_who_do_you_want_to_speak_to(self):
        self.speak_sound('soundfile_request_name')

    def speak_please_say_your_name(self):
        self.speak_sound('soundfile_visitor_name')

    def speak_delivery(self):
        self.speak_sound('soundfile_delivery')

    def speak_capture_picture(self):
        self.speak_sound('soundfile_capture_picture')

    def speak_sound(self, sound_config_property):
        sound_file_path = self.config.get('SOUNDS', sound_config_property)
        logging.info("Speaking sound " + sound_file_path)
        wave_obj = sa.WaveObject.from_wave_file(sound_file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        logging.info("Finished speaking sound")
