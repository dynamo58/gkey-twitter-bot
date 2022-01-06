import tweepy  # type: ignore

# Twitter API client with a some meta
class TwitterAPIClient:
    def __init__(self, CONF):
        auth = tweepy.OAuthHandler(
            CONF["TWITTER_API_KEY"], CONF["TWITTER_API_SECRET_KEY"])
        auth.set_access_token(
            CONF["TWITTER_ACCESS_TOKEN"], CONF["TWITTER_ACCESS_SECRET_TOKEN"])

        self.api = tweepy.API(auth)
        self.dummy = 1

    # tweets a message
    def tweet(self, message: str):
        try:
            for i in range(self.dummy):
                message += "⠀"

            self.dummy = (self.dummy + 1) % 5

            self.api.update_status(message)
            print("Tweeted message: ", message)
        except Exception as e:
            print("Couldn't tweet:")
            print(e)
