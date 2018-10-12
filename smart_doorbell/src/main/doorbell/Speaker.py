#!/usr/bin/env python3

from configparser import ConfigParser, ExtendedInterpolation
import pyaudio
import wave


class Speaker:
    project_path = "/Users/ralphl01/Dropbox/LYDIA/TECH/BBC-MSc/2018-07_IoT/iot_labs/smart_doorbell/src/main"

    logging.basicConfig(
        filename='/Users/ralphl01/Dropbox/LYDIA/TECH/BBC-MSc/2018-07_IoT/iot_labs/smart_doorbell/src/main/logging/smart_doorbell.full.log',
        level=logging.DEBUG)

    def __init__(self):
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read("%s/resources/doorbell.properties" % self.project_path)

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

    def speak_sound(self, sound_config_property):
        try:
            sound_file_path = self.config.get('SOUNDS', sound_config_property)
            chunk = 1024
            wf = wave.open(soundfile, 'rb')
            p = pyaudio.PyAudio()

            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

            data = wf.readframes(chunk)

            while data != '':
                stream.write(data)
                data = wf.readframes(chunk)

            stream.close()
            p.terminate()

        except IOError:
            print("ERROR: Couldn't open sound file {}", sound_config_property)
