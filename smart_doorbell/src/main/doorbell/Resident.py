import logging

import soundex

from Microphone import SpeechRecogniser


class Resident:

    is_at_home = False
    s = soundex.getInstance()
    dictophone = SpeechRecogniser()

    def __init__(self, text_name, registered_names, twitter_impl,
                 log='../logging/smart_doorbell.full.log'):
        # A list of sound files containing pronunciations of this resident's name
        # Examples: 'Matthew', 'Matt', 'Matty' 'Mr. Smith'
        self.registered_names = registered_names
        self.text_name = text_name
        self.t = twitter_impl
        logging.basicConfig(filename=log, level=logging.DEBUG)

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
        self.t.post_direct_message_with_image(message__format, image_file_path)

    def requested_name_matches_this_resident(self, requested_name_text):
        logging.info("Trying to match audio against resident ", self.text_name)
        stripped = requested_name_text.lower().replace(" ", "")
        for registered_name in self.registered_names:
            if registered_name.lower().replace(" ", "") == stripped:
                return True
        return False

    def set_resident_at_home(self, at_home):
        self.is_at_home = at_home
