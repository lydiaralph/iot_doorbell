import twitter

from configparser import ConfigParser


class TwitterImpl:

    # project_path = "/Users/ralphl01/Dropbox/LYDIA/TECH/BBC-MSc/2018-07_IoT/iot_labs/smart_doorbell/src/main"

    def __init__(self, resident_name):
        config = ConfigParser()
        
        #config.read(self.project_path + '/resources/twitter.properties')
        #config.read(self.project_path + '/resources/twitter.' + resident_name + '.properties')

        config.read('../resources/twitter.properties')
        config.read('../resources/twitter.' + resident_name + '.properties')


        access_token = config.get(resident_name.upper(), 'twitter_access_token')
        access_token_secret = config.get(resident_name.upper(), 'twitter_access_token_secret')
        con_key = config.get('APP', 'twitter_consumer_api_key')
        con_sec_key = config.get('APP', 'twitter_consumer_api_secret_key')

        self.api = twitter.Api(consumer_key=con_key,
                               consumer_secret=con_sec_key,
                               access_token_key=access_token,
                               access_token_secret=access_token_secret)
        
        self.api.VerifyCredentials()

        self.user_id = config.get(resident_name.upper(), 'user_id')

    def get_statuses(self):
        statuses = self.api.GetUserTimeline(user_id=self.user_id)
        # TODO: Change to log
        print([s.text for s in statuses])

    def post_direct_message(self, message):
        self.api.PostDirectMessage(text=message, user_id=self.user_id)
        # TODO: Change to log
        print("Successfully sent message to Twitter user", self.user_id)

    def post_direct_message_with_image(self, message, image_path):
        if image_path is None:
            self.api.PostDirectMessage(self, message)
        else:
            self.api.PostDirectMessage(text=message, user_id=self.user_id, media_file_path=image_path, media_type='dm_image')
        # TODO: Change to log
        print("Successfully sent message to Twitter user", self.user_id)

    def post_to_profile(self, message):
        # TODO: Change to log
        print("Method 'post_to_profile' not supported")
        pass


if __name__ == '__main__':
    t = TwitterImpl('LYDIA')
    t.get_statuses()
    t.post_direct_message('third test')
