#!/usr/bin/env python3

# Copied example from https://pypi.org/project/SpeechRecognition/3.8.1/ examples and followed guide

import speech_recognition as sr
from configparser import ConfigParser


class MicrophoneImpl:
    r = sr.Recognizer()

    def __init__(self):
        # Raspberry Pi needs device_index to be set: see README from link above
        config = ConfigParser().read('../resources/doorbell.properties')
        port = config.get('USB_PORTS', 'microphone_port')
        self.m = sr.Microphone(device_index=port)

    def recognise_speech(self):
        with self.m as m:
            self.r.adjust_for_ambient_noise(m)
            print("Listening for audio input...")
            audio = self.r.listen(m)

        self.recognise_with_google_speech(audio)

    def recognise_with_google_speech(self, audio):
        print("Now trying to translate text")
        try:
            print("Google Speech Recognition thinks you said \n" + self.r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def recognise_stored_audio(self, audio_file_path):
        wf = sr.AudioFile(audio_file_path)
        with wf as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.record(source)
        self.recognise_with_google_speech(audio)
