#!/usr/bin/env python3

import soundex
import wave


class Resident:

    isAtHome = False
    s = soundex.getInstance()

    def __init__(self, text_name, name_sounds_file_paths):
        # A list of sound files containing pronunciations of this resident's name
        # Examples: 'Matthew', 'Matt', 'Matty' 'Mr. Smith'
        self.registered_audio_names = name_sounds_file_paths
        self.text_name = text_name

    def alert_visitor_at_door(self, visitor_name_audio):  # TODO
        if self.isAtHome:
            self.request_answer_door()
        else:
            self.send_remote_notification()

    def request_answer_door(self):
        pass  # TODO

    def send_remote_notification(self):
        pass  # TODO

    def requested_name_matches_this_resident(self, audio):
        for registered_name_file in self.registered_audio_names:
            # Try to open file
            with wave.open(registered_name_file, 'rb') as registered_name:
                s1 = self.s.soundex(registered_name)
                s2 = self.s.soundex(audio)
                if s1 == s2:
                    return True
        return False
