#!/usr/bin/env python3

# Copied example from https://pypi.org/project/SpeechRecognition/3.8.1/ examples and followed guide

import speech_recognition as sr
from configparser import ConfigParser, ExtendedInterpolation
import logging


class AudioCapture:
    project_path = "/Users/ralphl01/Dropbox/LYDIA/TECH/BBC-MSc/2018-07_IoT/iot_labs/smart_doorbell/src/main"

    def __init__(self):
        self.r = sr.Recognizer()

        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(self.project_path + "/resources/doorbell.properties")
        # Raspberry Pi needs device_index to be set: see README from link above
        # port = config.get('USB_PORTS', 'microphone_port')
        # logging.debug("Microphone is on port " +  port)
        # self.m = sr.Microphone(device_index=int(port))
        self.m = sr.Microphone()

        self.sound_samples_dir = config.get('SOUNDS', 'soundfile_doorbell_dir')
        logging.debug("Sound samples directory: " + self.sound_samples_dir)
        print("Sound samples directory: ", self.sound_samples_dir)
        if '${' in self.sound_samples_dir:
            logging.error("Microphone was not configured properly")
            raise RuntimeError("Microphone was not configured properly")

    def capture_audio(self):
        with self.m as m:
            self.r.adjust_for_ambient_noise(m)
            print("Listening for audio input...")
            audio = self.r.listen(m)
            print("Heard something")
            return audio

    def capture_and_persist_audio(self):
        audio = self.capture_audio()
        logging.info("Trying to persist captured audio")
        with open(self.sound_samples_dir + "/microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())
        return audio


class SpeechRecogniser:

    UNRECOGNISED = "Audio was not understood by speech recognition software"

    project_path = "/Users/ralphl01/Dropbox/LYDIA/TECH/BBC-MSc/2018-07_IoT/iot_labs/smart_doorbell/src/main"

    def __init__(self):
        self.r = sr.Recognizer()

        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(self.project_path + "/resources/doorbell.properties")

        self.sound_samples_dir = config.get('SOUNDS', 'soundfile_doorbell_dir')
        logging.debug("Sound samples directory: " + self.sound_samples_dir)
        print("Sound samples directory: ", self.sound_samples_dir)
        if '${' in self.sound_samples_dir:
            logging.error("Microphone was not configured properly")
            raise RuntimeError("Microphone was not configured properly")

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
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.record(source)
        self.recognise_speech(audio)
