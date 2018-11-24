#!/usr/bin/env python3

# Copied example from https://pypi.org/project/SpeechRecognition/3.8.1/ examples and followed guide

import speech_recognition as sr
from configparser import ConfigParser, ExtendedInterpolation
import logging


class AudioCapture:

    def __init__(self):
        self.r = sr.Recognizer()

        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read("../resources/doorbell.properties")
        # Raspberry Pi needs device_index to be set: see README from link above
        port = config.get('USB_PORTS', 'microphone_port')
        logging.debug("Microphone is on port " +  port)
        self.m = sr.Microphone(device_index=int(port))
        # self.m = sr.Microphone()

        self.captured_sounds_dir = config.get('SOUNDS', 'captured_sounds_dir')
        logging.debug("Captured sounds will be stored in: " + self.captured_sounds_dir)
        print("Captured sounds will be stored in: ", self.captured_sounds_dir)
        if '${' in self.captured_sounds_dir:
            logging.error("Microphone was not configured properly")
            raise RuntimeError("Microphone was not configured properly")

    def capture_audio(self):
        with self.m as m:
            #self.r.adjust_for_ambient_noise(m)
            print("Listening for audio input...")
            audio = self.r.listen(m)
            print("Heard something")
            return audio

    def capture_and_persist_audio(self, file_name='microphone-results'):
        audio = self.capture_audio()
        file_path = self.captured_sounds_dir + "/captured-" + file_name + ".wav"
        print("Trying to persist captured audio as ", file_path)
        with open(file_path, "wb") as f:
            f.write(audio.get_wav_data())
        return audio


class SpeechRecogniser:

    UNRECOGNISED = "Audio was not understood by speech recognition software"

    def __init__(self):
        self.r = sr.Recognizer()
       
    def recognise_speech(self, audio):
        print("Now trying to translate text")
        try:
            recognised_text = self.r.recognize_google(audio, language='en-GB')
            logging.info("Google Speech Recognition thinks you said \n" + recognised_text)
            print("Google Speech Recognition thinks you said \n", recognised_text)
            return recognised_text
        except sr.UnknownValueError:
            logging.error("Google Speech Recognition could not understand audio")
            print("Google Speech Recognition could not understand audio")
            return self.UNRECOGNISED
        except sr.RequestError as e:
            logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return self.UNRECOGNISED
        except Exception as e:
            print(e)
            return self.UNRECOGNISED

    def recognise_stored_audio(self, audio_file_path):
        wf = sr.AudioFile(audio_file_path)
        with wf as source:
            #self.r.adjust_for_ambient_noise(source)
            audio = self.r.record(source)
        self.recognise_speech(audio)
