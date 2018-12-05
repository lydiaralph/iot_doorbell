#!/usr/bin/env python3
import speech_recognition
from speech_recognition import AudioData

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from unittest.mock import MagicMock

from doorbell.Microphone import SpeechRecogniser, AudioCapture


class TestMicrophone(unittest.TestCase):

    def setUp(self):
        self.ac = AudioCapture(cfg='resources/doorbell.properties',
                               sounds_dir='resources/captured/sounds',
                               log='doorbell/test/resources/logging/unittest.log')
        self.sr = SpeechRecogniser()
        self.sr.r = MagicMock()
        self.ac.r = MagicMock()

    def test_basic_microphone_setup(self):
        assert self.ac.r is not None
        assert self.ac.captured_sounds_dir is not None
        assert self.ac.captured_sounds_dir.exists()
        assert self.sr.r is not None

    def test_capture_audio(self):
        self.ac.capture_audio()
        self.ac.r.listen.assert_called_once()
        self.ac.r.listen.assert_called_once_with(self.ac.m)

    def test_capture_and_persist_audio(self):
        # Given
        fake_audio = MagicMock()
        fake_audio.get_wav_data.return_value = "abc".encode()
        self.ac.r.listen.return_value = fake_audio
        expected_audio_path = (self.ac.captured_sounds_dir / 'captured-microphone-results.wav')
        if expected_audio_path.exists():
            expected_audio_path.unlink()
        assert not expected_audio_path.exists()

        # When
        self.ac.capture_and_persist_audio()
        self.ac.r.listen.assert_called_once()
        self.ac.r.listen.assert_called_once_with(self.ac.m)

        # Then
        print(str(expected_audio_path))
        assert expected_audio_path.exists()

    def test_recognise_speech_value_exception(self):
        self.sr.r.recognize_google.return_value = speech_recognition.UnknownValueError

        result = self.sr.recognise_speech(audio="abc")
        self.sr.r.recognize_google.assert_called_once()
        assert result is self.sr.UNRECOGNISED

    def test_recognise_speech_request_exception(self):
        self.sr.r.recognize_google.return_value = speech_recognition.RequestError

        result = self.sr.recognise_speech(audio="abc")
        self.sr.r.recognize_google.assert_called_once()
        assert result is self.sr.UNRECOGNISED

    def test_recognise_speech_request_exception(self):
        self.sr.r.recognize_google.return_value = Exception

        result = self.sr.recognise_speech(audio="abc")
        self.sr.r.recognize_google.assert_called_once()
        assert result is self.sr.UNRECOGNISED

    def test_recognise_speech(self):
        self.sr.recognise_speech("abc")
        self.sr.r.recognize_google.assert_called_once()

    def test_recognise_stored_audio(self):
        self.sr.recognise_stored_audio('doorbell/test/resources/hello.wav')
        self.sr.r.record.assert_called_once()
        self.sr.r.recognize_google.assert_called_once()


if __name__ == 'main':
    unittest.main()
