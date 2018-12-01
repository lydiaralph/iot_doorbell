#!/usr/bin/env python3

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from unittest.mock import MagicMock
from doorbell.test.utils import MockTwitter

from doorbell import Resident


class TestResident(unittest.TestCase):

    def setUp(self):
        self.mock_twitter = MockTwitter.MockTwitter('test')
        self.mock_twitter.post_direct_message = MagicMock()
        self.under_test = Resident.Resident('Test name', ['test'], self.mock_twitter,
                                            log='doorbell/test/resources/logging/unittest.log')
        self.under_test.dictophone = MagicMock

    def test_basic_resident_setup(self):
        assert self.under_test.text_name == 'Test name'
        assert self.under_test.registered_names == ['test']
        assert self.under_test.t == self.mock_twitter

    def test_alert_visitor_at_door_resident_not_at_home(self):
        # When
        self.under_test.dictophone.UNRECOGNISED = "Unrecognised"
        self.under_test.is_at_home = False
        self.under_test.alert_visitor_at_door("Hannah")
        # Then
        # self.under_test.t.post_direct_message_with_image.assert_called_once()
        # self.under_test.t.post_direct_message_with_image\
        #     .assert_called_once_with("Hannah visited the house and left a message: (blank)", None)

    def test_alert_visitor_at_door_resident_at_home(self):
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
        self.under_test.dictophone.UNRECOGNISED = "Unrecognised"
        # When
        self.under_test.send_remote_notification(visitor_name_audio_text="audio")
        # Then
        # self.under_test.t.post_direct_message_with_image.assert_called_once()

    def test_request_name_matches_this_resident(self):
        # When
        try:
            self.under_test.requested_name_matches_this_resident("audio")
        # Then
        except IsADirectoryError or TypeError:
            self.under_test.dictophone.recognise_stored_audio.assert_called_once()
            self.under_test.dictophone.recognise_stored_audio.assert_called_once_with("test")


if __name__ == 'main':
    unittest.main()
