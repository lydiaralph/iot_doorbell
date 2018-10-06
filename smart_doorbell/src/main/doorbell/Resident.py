#!/usr/bin/env python3

import soundex

from doorbell.Microphone import MicrophoneImpl
from doorbell.Twitter import  TwitterImpl


class Resident:

    isAtHome = False
    s = soundex.getInstance()
    m = MicrophoneImpl()

    def __init__(self, text_name, name_sounds_file_paths):
        # A list of sound files containing pronunciations of this resident's name
        # Examples: 'Matthew', 'Matt', 'Matty' 'Mr. Smith'
        self.registered_audio_names = name_sounds_file_paths
        self.text_name = text_name
        self.t = TwitterImpl(text_name)

    def alert_visitor_at_door(self, visitor_name_audio):  # TODO
        if self.isAtHome:
            self.request_answer_door()
        else:
            self.send_remote_notification(visitor_name_audio)

    def request_answer_door(self):
        self.t.post_direct_message(self, "Please answer the door")

    def send_remote_notification(self, audio):
        self.t.post_direct_message(self, "Somebody visited the house and left a message:" + audio)

    def requested_name_matches_this_resident(self, input):
        for registered_name_file in self.registered_audio_names:
            # Recognise registered name with same recogniser as parsing the input

            registered_text = self.m.recognise_stored_audio(registered_name_file)

            if registered_text == input:
                return True
        return False
