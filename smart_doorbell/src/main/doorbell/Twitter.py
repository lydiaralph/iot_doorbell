import twitter
import logging

from configparser import ConfigParser


class TwitterImpl:

    def __init__(self, resident_name,
                 cfg='../resources/doorbell.properties',
                 twitter_cfg='../resources/twitter.%s.properties',
                 log='../logging/smart_doorbell.full.log'):

        logging.basicConfig(filename=log, level=logging.DEBUG)
        config = ConfigParser()
        
        config.read(cfg)
        config.read(twitter_cfg.format(resident_name))

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
        logging.info([s.text for s in statuses])

    def post_direct_message(self, message):
        self.api.PostDirectMessage(text=message, user_id=self.user_id)
        logging.info("Successfully sent message to Twitter user %s", self.user_id)

    def post_direct_message_with_image(self, message, image_path):
        if image_path is None:
            logging.info("Posting message with no image")
            self.api.PostDirectMessage(text=message, user_id=self.user_id)
        else:
            logging.info("Posting message with image")
            self.api.PostDirectMessage(text=message, user_id=self.user_id,
                                       media_file_path=image_path, media_type='dm_image')
        logging.info("Successfully sent message to Twitter user %s", self.user_id)

    def post_to_profile(self, message):
        logging.error("Method 'post_to_profile' not supported")
        pass


if __name__ == '__main__':
    t = TwitterImpl('LYDIA')
    t.get_statuses()
    t.post_direct_message('third test')
