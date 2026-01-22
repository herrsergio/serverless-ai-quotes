import tweepy

class Twitter:
    """
    Wrapper class for Tweepy client to interact with Twitter API v2.
    """

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        """
        Initialize the Twitter client with credentials.
        """
        self.api = tweepy.Client(
                consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_key, access_token_secret=access_secret)


    def update_status(self, text):
        """
        Post a tweet with the given text.
        """
        return self.api.create_tweet(text=text)
