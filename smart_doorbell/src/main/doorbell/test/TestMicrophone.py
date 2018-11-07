#!/usr/bin/env python3

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from doorbell import Microphone
from unittest.mock import MagicMock


class TestMicrophone(unittest.TestCase):

    def setUp(self):
        self.under_test = Microphone.MicrophoneImpl()
        self.under_test.r = MagicMock()

    def test_basic_microphone_setup(self):
        assert self.under_test.r is not None
        assert self.under_test.sound_samples_dir is not None
        assert '${' not in self.under_test.sound_samples_dir

    def test_recognise_speech(self):
        self.under_test.recognise_speech()
        self.under_test.r.listen.assert_called_once()
        self.under_test.r.listen.assert_called_once_with(self.under_test.m)
        self.under_test.r.recognize_google.assert_called_once()

    def test_recognise_stored_audio(self):
        self.under_test.recognise_stored_audio(self.under_test.project_path + '/doorbell/test/resources/hello.wav')
        self.under_test.r.record.assert_called_once()
        self.under_test.r.recognize_google.assert_called_once()


if __name__ == 'main':
    unittest.main()
