#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

from doorbell import Resident, Microphone
from doorbell.test.utils.MockTwitter import MockTwitter


class ResidentTest(unittest.TestCase):

    def setUp(self):
        mock_microphone = Microphone.MicrophoneImpl
        mock_microphone.__init__ = MagicMock()
        mock_microphone.recognise_stored_audio = MagicMock()

        self.mock_twitter = MockTwitter('test')
        self.mock_twitter.post_direct_message = MagicMock()
        self.under_test = Resident.Resident('Test name', ['../resources/test.wav'], self.mock_twitter)
        self.under_test.m = mock_microphone

    def test_basic_resident_setup(self):
        assert self.under_test.text_name == 'Test name'
        assert self.under_test.registered_audio_names == ['../resources/test.wav']
        assert self.under_test.t == self.mock_twitter

    def test_alert_visitor_at_door_resident_not_at_home(self):
        # When
        self.under_test.is_at_home = False
        self.under_test.alert_visitor_at_door("hannah")
        # Then
        self.under_test.t.post_direct_message.assert_called_once()
        self.under_test.t.post_direct_message\
            .assert_called_once_with("Somebody visited the house and left a message: hannah")

    def test_alert_visitor_at_door_resient_at_home(self):
        # When
        self.under_test.is_at_home = True
        self.under_test.alert_visitor_at_door("hannah")
        # Then
        self.under_test.t.post_direct_message.assert_called_once()
        self.under_test.t.post_direct_message \
            .assert_called_once_with("Please answer the door")

    def test_request_answer_door(self):
        # When
        self.under_test.request_answer_door()
        # Then
        self.under_test.t.post_direct_message.assert_called_once()

    def test_send_remote_notification(self):
        # When
        self.under_test.send_remote_notification("audio")
        # Then
        self.under_test.t.post_direct_message.assert_called_once()

    def test_request_name_matches_this_resident(self):
        # When
        try:
            self.under_test.requested_name_matches_this_resident("audio")
        # Then
        except IsADirectoryError or TypeError:
            self.under_test.m.recognise_stored_audio.assert_called_once()
            self.under_test.m.recognise_stored_audio.assert_called_once_with("../resources/test.wav")


if __name__ == 'main':
    unittest.main()
