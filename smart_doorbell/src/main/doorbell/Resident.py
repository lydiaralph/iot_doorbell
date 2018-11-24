#!/usr/bin/env python3

import soundex

from doorbell.Microphone import SpeechRecogniser


class Resident:

    is_at_home = False
    s = soundex.getInstance()
    dictophone = SpeechRecogniser()

    def __init__(self, text_name, name_sounds_file_paths, twitter_impl):
        # A list of sound files containing pronunciations of this resident's name
        # Examples: 'Matthew', 'Matt', 'Matty' 'Mr. Smith'
        self.registered_audio_names = name_sounds_file_paths
        self.text_name = text_name
        self.t = twitter_impl

    def alert_visitor_at_door(self, visitor_name_audio):
        if self.is_at_home:
            self.request_answer_door()
        else:
            self.send_remote_notification(visitor_name_audio)

    def request_answer_door(self):
        self.t.post_direct_message("Please answer the door")

    def send_remote_notification(self, visitor_name_audio_text='Somebody',
                                 recorded_message_audio_text='(blank)',
                                 image_file_path=None):

        if visitor_name_audio_text is self.dictophone.UNRECOGNISED:
            visitor_name_audio_text = "Somebody"

        message__format = "{} visited the house and left a message: {}"\
            .format(visitor_name_audio_text, recorded_message_audio_text)
        self.t.post_direct_message(message__format, image_file_path)

    def requested_name_matches_this_resident(self, input_audio):
        print("Trying to match audio against resident ", self.text_name)
        for registered_name_file in self.registered_audio_names:
            # Recognise registered name with same recogniser as parsing the input
            registered_text = self.dictophone.recognise_stored_audio(registered_name_file)

            if registered_text == input_audio:
                return True
        return False

    def set_resident_at_home(self, at_home):
        self.is_at_home = at_home

    def get_resident_at_home(self):
        return self.is_at_home
