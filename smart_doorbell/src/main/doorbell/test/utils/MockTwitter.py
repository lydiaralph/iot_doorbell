from doorbell.Twitter import TwitterImpl

from unittest.mock import MagicMock


class MockTwitter(TwitterImpl):
    def __init__(self, resident_name):
        self.user_id = resident_name
        self.api = MagicMock()
