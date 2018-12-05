#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

from doorbell import Doorbell
from doorbell.Resident import Resident
from doorbell.test.utils.MockTwitter import MockTwitter


class TestDoorbell(unittest.TestCase):

    test_resident = Resident('test', ['test'], MockTwitter('test'))

    def setUp(self):
        self.under_test = Doorbell.Doorbell([self.test_resident],
                                            MagicMock(),
                                            MagicMock(),
                                            MagicMock(),
                                            log='doorbell/test/resources/logging/unittest.log')

    def test_setup_logging(self):
        self.under_test.set_up_logging()

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
        self.under_test.dictophone.recognise_speech.return_value = \
            self.under_test.dictophone.UNRECOGNISED

        # When
        self.under_test.doorbell_response()

        # Then
        self.under_test.speaker.speak_who_do_you_want_to_speak_to.assert_called_once()
        self.under_test.microphone.capture_and_persist_audio\
            .assert_called_once_with('resident-name')
        self.under_test.dictophone.recognise_speech.assert_called_once()

    def test_run_doorbell(self):
        # Given
        self.under_test.dictophone.recognise_speech.return_value = 'test'
        # self.under_test.motion_sensor.wait_for_motion.return_value = True

        # When
        self.under_test.run_doorbell_application()

        # Then
        self.under_test.speaker.speak_hello.assert_called_once()
        self.under_test.speaker.speak_not_recognised.assert_not_called()

    def test_run_doorbell_resident_not_at_home(self):
        # Given
        self.under_test.dictophone.recognise_speech.return_value = 'test'

        for resident in self.under_test.residents:
            resident.is_at_home = False

        # self.under_test.motion_sensor.wait_for_motion.return_value = True

        # When
        self.under_test.run_doorbell_application()

        # Then
        self.under_test.speaker.speak_hello.assert_called_once()
        self.under_test.speaker.speak_not_recognised.assert_not_called()
        self.under_test.speaker.speak_record_message.assert_called_once()

        self.under_test.microphone.capture_and_persist_audio.assert_called_with('message')
        self.under_test.dictophone.recognise_speech.assert_called()

        self.under_test.speaker.speak_capture_picture.assert_called_once()
        self.test_resident.t.api.PostDirectMessage.assert_called()

    def test_run_doorbell_with_unrecognised_resident(self):
        # Given
        self.under_test.dictophone.recognise_speech.return_value = self.under_test.dictophone.UNRECOGNISED
        # self.under_test.motion_sensor.wait_for_motion.return_value = True

        # When
        self.under_test.run_doorbell_application()

        # Then
        self.under_test.speaker.speak_hello.assert_called_once()
        self.under_test.speaker.speak_not_recognised.assert_called_once()

    def set_up_residents(self):
        residents = self.under_test.set_up_residents()
        assert residents.count() == 2
        assert residents[0].text_name == 'Matt'
        assert residents[0].registered_names[0] == 'matt'
        assert residents[1].t is not None
        assert residents[1].is_at_home == False


if __name__ == 'main':
    unittest.main()
