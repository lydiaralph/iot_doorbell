#!/usr/bin/env python3

# Copied example from https://pypi.org/project/SpeechRecognition/3.8.1/ examples and followed guide

import speech_recognition as sr
from configparser import ConfigParser, ExtendedInterpolation
import logging

class MicrophoneImpl:
    r = sr.Recognizer()
    logger = logging.getLogger(__name__)
    log_directory = '../logging'
    logging_file_path = 'microphone.full.log'
    logging_file_name = "{}/{}".format(log_directory,logging_file_path)
    print(logging_file_name)

    def __init__(self, config_location):
        # Raspberry Pi needs device_index to be set: see README from link above
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(config_location + '/doorbell.properties')
        port = config.get('USB_PORTS', 'microphone_port')
        logging.debug("Microphone is on port ", port)
        self.m = sr.Microphone(device_index=int(port))
        self.sound_samples_dir = config.get('SOUNDS', 'soundfile_residents_dir')
        logging.debug("Sound samples directory: ", self.sound_samples_dir)
        print("Sound samples directory: ", self.sound_samples_dir)
        if '${' in self.sound_samples_dir:
          logging.error("Microphone was not configured properly")
          raise RuntimeError("Microphone was not configured properly")

    def recognise_speech(self):
        audio = self.capture_audio()
        self.recognise_with_google_speech(audio)

    def capture_audio(self):
        with self.m as m:
            self.r.adjust_for_ambient_noise(m)
            print("Listening for audio input...")
            audio = self.r.listen(m)
            return audio

    def capture_and_persist_audio(self):
        audio = self.capture_audio()
        logging.info("Trying to persist captured audio")
        with open(self.sound_samples_dir + "/microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())
        return audio

    def recognise_with_google_speech(self, audio):
        logging.info("Now trying to translate text")
        try:
            logging.info("Google Speech Recognition thinks you said \n" + self.r.recognize_google(audio))
        except sr.UnknownValueError:
            logging.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))

    def recognise_stored_audio(self, audio_file_path):
        wf = sr.AudioFile(audio_file_path)
        with wf as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.record(source)
        self.recognise_with_google_speech(audio)


if __name__ == "__main__":
    log_directory = '../logging'
    logging_file_path = 'microphone.full.log'
    logging_file_name = "{}/{}".format(log_directory,logging_file_path)
    print(logging_file_name)
    logging.basicConfig(filename=logging_file_name, level=logging.DEBUG)
    config_location = "/home/pi/Dev/iot_doorbell/smart_doorbell/" \
                      "src/main/resources"
    m = MicrophoneImpl(config_location)
    m.capture_and_persist_audio()
    print("Recognising")
    m.recognise_stored_audio(m.sounds_sample_dir + '/microphone-results.wav')
    m.recognise_speech()
