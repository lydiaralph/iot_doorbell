import twitter

from configparser import ConfigParser


class TwitterImpl:

    def __init__(self, config_location, resident_name):
        config = ConfigParser()
        
        config.read(config_location + '/twitter.properties')

        con_key = config['APP']['twitter_consumer_api_key']
        con_sec_key = config.get('APP', 'twitter_consumer_api_secret_key')
        # TODO: Make it specific to each resident
        access_token = config.get(resident_name, 'twitter_access_token')
        access_token_secret = config.get(resident_name, 'twitter_access_token_secret')
        
        self.api = twitter.Api(consumer_key=con_key,
		  consumer_secret=con_sec_key,
		  access_token_key=access_token,
		  access_token_secret=access_token_secret)
        
        self.api.VerifyCredentials()

        self.user_id = config.get(resident_name, 'user_id')

    def get_statuses(self):
        statuses=self.api.GetUserTimeline(user_id=self.user_id)
        # TODO: Change to log
        print([s.text for s in statuses])

    def post_direct_message(self, message):
        self.api.PostDirectMessage(message,user_id=self.user_id)
        # TODO: Change to log
        print("Successfully sent message to Twitter user", self.user_id)

    def post_to_profile(self, message):
        pass


if __name__ == '__main__':
    config_location = '/home/pi/Dev/iot_doorbell/smart_doorbell/src/main/resources'
    t = TwitterImpl(config_location, 'LYDIA')
    t.get_statuses()
    t.post_direct_message('third test')
