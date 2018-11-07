class MockTwitter:
    def __init__(self, resident_name):
        self.user_id = resident_name

    def get_statuses(self):
        print("Called 'get_statuses'")
        pass

    def post_direct_message(self, message):
        print("Successfully sent message to Twitter user (mock): ", self.user_id, message)
        pass

    def post_to_profile(self, message):
        pass
