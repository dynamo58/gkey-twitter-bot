import tweepy  # type: ignore


class TwitterAPIClient:
    def __init__(self, CONF):
        auth = tweepy.OAuthHandler(
            CONF["TWITTER_API_KEY"], CONF["TWITTER_API_SECRET_KEY"])
        auth.set_access_token(
            CONF["TWITTER_ACCESS_TOKEN"], CONF["TWITTER_ACCESS_SECRET_TOKEN"])

        self.api = tweepy.API(auth)


def tweet(message: str, client: TwitterAPIClient):
    try:
        client.api.update_status(message)
        print("Tweeted message:\t", message)
    except:
        print("Couldn't tweet message")
