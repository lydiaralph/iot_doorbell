import logging
from pathlib import Path

import simpleaudio as sa


class Speaker:
    def __init__(self,
                 sounds_input_dir='../resources/sounds/doorbell',
                 log='../logging/smart_doorbell.full.log'):
        self.sounds_dir = Path(sounds_input_dir).resolve()
        if not self.sounds_dir.exists():
            raise RuntimeError("Could not find sound samples directory at ",
                               self.sounds_dir)

        logging.basicConfig(filename=log, level=logging.DEBUG)

    def speak_hello(self):
        self.speak_sound('hello')

    def speak_goodbye(self):
        self.speak_sound('goodbye')

    def speak_not_recognised(self):
        self.speak_sound('not_recognised')

    def speak_record_message(self):
        self.speak_sound('record_message')

    def speak_who_do_you_want_to_speak_to(self):
        self.speak_sound('request_name')

    def speak_please_say_your_name(self):
        self.speak_sound('visitor_name')

    def speak_delivery(self):
        # self.speak_sound('delivery')
        logging.debug("Delivery functionality not currently implemented")
        pass

    def speak_capture_picture(self):
        self.speak_sound('capture_photo')

    def speak_sound(self, sound_config_property):
        logging.debug("Trying to speak sound " + sound_config_property)

        file = (self.sounds_dir / sound_config_property).with_suffix('.wav')

        if not file.exists():
            raise RuntimeError("Attempted to play sound file that does not exist: " + str(file))

        wave_obj = sa.WaveObject.from_wave_file(str(file))
        play_obj = wave_obj.play()
        play_obj.wait_done()
        logging.info("Finished speaking sound")
