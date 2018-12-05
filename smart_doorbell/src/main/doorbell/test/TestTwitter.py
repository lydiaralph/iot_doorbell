#!/usr/bin/env python3
import twitter

from doorbell.Twitter import TwitterImpl
from doorbell.test.utils.MockTwitter import MockTwitter

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestTwitter(unittest.TestCase):

    def setUp(self):
        self.under_test = MockTwitter('test_user_id')

    def test_get_statuses(self):
        self.under_test.get_statuses()
        self.under_test.api.GetUserTimeline.assert_called_once()

    def test_post_direct_message(self):
        self.under_test.post_direct_message("abc")
        self.under_test.api.PostDirectMessage.assert_called_once()
        self.under_test.api.PostDirectMessage.assert_called_with(text="abc",
                                                                 user_id="test_user_id")

    def test_post_direct_message_with_image(self):
        self.under_test.post_direct_message_with_image("abc", "test.jpg")
        self.under_test.api.PostDirectMessage.assert_called_once()
        self.under_test.api.PostDirectMessage.assert_called_with(text="abc",
                                                                 user_id="test_user_id",
                                                                 media_file_path="test.jpg",
                                                                 media_type='dm_image')

    def test_post_direct_message_with_none_image(self):
        self.under_test.post_direct_message_with_image("abc", None)
        self.under_test.api.PostDirectMessage.assert_called_once()
        self.under_test.api.PostDirectMessage.assert_called_with(text="abc",
                                                                 user_id="test_user_id")

    def test_post_to_profile(self):
        self.under_test.post_to_profile("abc")
        self.under_test.api.PostDirectMessage.assert_not_called()

    def test_setup_with_bad_twitter_id_is_rejected(self):
        with self.assertRaises(twitter.error.TwitterError):
            TwitterImpl('test',
                        twitter_standard_cfg='../main/resources/twitter.properties',
                        twitter_cfg='doorbell/test/resources/twitter.{}.properties',
                        log='doorbell/test/resources/logging/unittest.log')


if __name__ == 'main':
    unittest.main()
