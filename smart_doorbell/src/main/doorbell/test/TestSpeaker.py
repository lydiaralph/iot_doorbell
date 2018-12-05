#!/usr/bin/env python3

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from unittest.mock import MagicMock

from doorbell import Speaker


class TestSpeaker(unittest.TestCase):

    def setUp(self):
        self.under_test = Speaker.Speaker(
            sounds_input_dir='resources/sounds/doorbell',
            log='doorbell/test/resources/logging/unittest.log')

        self.under_test.speak_sound = MagicMock()

    def test_basic_speaker_setup(self):
        assert self.under_test.sounds_dir.exists()

    def test_speak_hello(self):
        self.under_test.speak_hello()
        self.under_test.speak_sound.assert_called_once()

    def test_speak_goodbye(self):
        self.under_test.speak_goodbye()
        self.under_test.speak_sound.assert_called_once()

    def test_speak_not_recognised(self):
        self.under_test.speak_not_recognised()
        self.under_test.speak_sound.assert_called_once()

    def test_speak_record_message(self):
        self.under_test.speak_record_message()
        self.under_test.speak_sound.assert_called_once()

    def test_speak_who_do_you_want_to_speak_to(self):
        self.under_test.speak_who_do_you_want_to_speak_to()
        self.under_test.speak_sound.assert_called_once()

    def test_speak_please_say_your_name(self):
        self.under_test.speak_please_say_your_name()
        self.under_test.speak_sound.assert_called_once()

    def test_speak_delivery(self):
        self.under_test.speak_delivery()
        self.under_test.speak_sound.assert_not_called()

    def test_speak_capture_picture(self):
        self.under_test.speak_capture_picture()
        self.under_test.speak_sound.assert_called_once_with('capture_photo')


if __name__ == 'main':
    unittest.main()
