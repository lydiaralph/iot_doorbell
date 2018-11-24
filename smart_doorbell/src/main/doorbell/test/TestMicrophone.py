#!/usr/bin/env python3
from doorbell.Microphone import AudioCapture

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from unittest.mock import MagicMock

from doorbell.Microphone import SpeechRecogniser


class TestMicrophone(unittest.TestCase):

    def setUp(self):
        self.ac = AudioCapture()
        self.sr = SpeechRecogniser()
        self.sr.r = MagicMock()
        self.ac.r = MagicMock()

    def test_basic_microphone_setup(self):
        assert self.ac.r is not None
        assert self.ac.sound_samples_dir is not None
        assert '${' not in self.ac.sound_samples_dir
        assert self.sr.r is not None
        assert self.sr.sound_samples_dir is not None
        assert '${' not in self.sr.sound_samples_dir

    def test_capture_audio(self):
        self.ac.capture_audio()
        self.ac.r.listen.assert_called_once()
        self.ac.r.listen.assert_called_once_with(self.ac.m)

    def test_capture_and_persist_audio(self):
        self.ac.capture_audio()
        self.ac.r.listen.assert_called_once()
        self.ac.r.listen.assert_called_once_with(self.ac.m)

    def test_recognise_speech(self):
        self.sr.recognise_speech("abc")
        self.sr.r.recognize_google.assert_called_once()

    def test_recognise_stored_audio(self):
        self.sr.recognise_stored_audio(self.sr.project_path + '/doorbell/test/resources/hello.wav')
        self.sr.r.record.assert_called_once()
        self.sr.r.recognize_google.assert_called_once()


if __name__ == 'main':
    unittest.main()
