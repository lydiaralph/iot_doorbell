#!/usr/bin/env python3
from doorbell.test.utils.MockTwitter import MockTwitter

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TwitterTest(unittest.TestCase):

    def setUp(self):
        self.under_test = MockTwitter('test_user_id')

    def test_get_statuses(self):
        self.under_test.get_statuses()
        self.under_test.api.GetUserTimeline.assert_called_once()

    def test_post_direct_message(self):
        self.under_test.post_direct_message("abc")
        self.under_test.api.PostDirectMessage.assert_called_once()
        self.under_test.api.PostDirectMessage.assert_called_with(text="abc", user_id="test_user_id")

    def test_post_to_profile(self):
        self.under_test.post_to_profile("abc")
        self.under_test.api.PostDirectMessage.assert_not_called()


if __name__ == 'main':
    unittest.main()
