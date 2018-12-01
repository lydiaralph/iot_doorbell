#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

from doorbell import Doorbell


class TestDoorbell(unittest.TestCase):

    def setUp(self):

        self.under_test = Doorbell.Doorbell(MagicMock(),
                                            MagicMock(),
                                            MagicMock(),
                                            MagicMock(),
                                            # log='resources/logging/unittest.log')
                                            log='doorbell/test/resources/logging/unittest.log')

    def test_doorbell_response(self):
        # When
        self.under_test.doorbell_response()

        # Then
        self.under_test.speaker.speak_who_do_you_want_to_speak_to.assert_called_once()
        assert self.under_test.microphone.capture_and_persist_audio.call_count == 2
        assert self.under_test.dictophone.recognise_speech.call_count == 2

        assert self.under_test.speaker.speak_please_say_your_name.call_count == 1

    def test_doorbell_response_with_unrecognised_resident(self):
        # Given
        self.under_test.dictophone.recognise_speech.return_value = self.under_test.dictophone.UNRECOGNISED

        # When
        self.under_test.doorbell_response()

        # Then
        self.under_test.speaker.speak_who_do_you_want_to_speak_to.assert_called_once()
        self.under_test.microphone.capture_and_persist_audio.assert_called_once_with('resident-name')
        self.under_test.dictophone.recognise_speech.assert_called_once()


if __name__ == 'main':
    unittest.main()
