#!/usr/bin/env python3

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from unittest.mock import MagicMock

from doorbell import Speaker


class TestSpeaker(unittest.TestCase):

    def setUp(self):
        self.under_test = Speaker.Speaker(cfg='resources/doorbell.properties',
                                          log='doorbell/test/resources/logging/unittest.log')

        self.under_test.speak_sound = MagicMock()

    def test_basic_speaker_setup(self):
        assert self.under_test.config.sections() is not None
        assert self.under_test.config['SOUNDS'] is not None

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
        self.under_test.speak_sound.assert_called_once()


if __name__ == 'main':
    unittest.main()
