#!/usr/bin/env python3

from configparser import ConfigParser
import pyaudio
import wave


class Speaker:

    def __init__(self):
        self.config = ConfigParser().read("../resources/doorbell.properties")

    def speak_hello(self):
        self.speak_sound('soundfile_hello')

    def speak_goodbye(self):
        self.speak_sound('soundfile_goodbye')

    def speak_not_recognised(self):
        self.speak_sound('soundfile_not_recognised')

    def speak_record_message(self):
        self.speak_sound('soundfile_record_message')

    def speak_resident_name(self):
        self.speak_sound('soundfile_resident_name')

    def speak_visitor_name(self):
        self.speak_sound('soundfile_visitor_name')

    def speak_delivery(self):
        self.speak_sound('soundfile_delivery')

    def speak_sound(self, sound_config_property):
        try:
            soundfile = self.config.get('SOUNDS', sound_config_property)
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
