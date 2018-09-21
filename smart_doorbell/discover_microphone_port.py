#!/usr/bin/env python3
# From https://pypi.org/project/SpeechRecognition/3.8.1/

import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
