import tweepy	# type: ignore
from dotenv import dotenv_values

CONF = dotenv_values(".env")

auth = tweepy.OAuthHandler(CONF["TWITTER_API_KEY"], CONF["TWITTER_API_SECRET_KEY"])
auth.set_access_token(CONF["TWITTER_ACCESS_TOKEN"], CONF["TWITTER_ACCESS_SECRET_TOKEN"])

api = tweepy.API(auth)

def tweet(message: str):
    try:
        api.update_status(message)
        print("Tweeted message:\t", message)
    except:
        print("Couldn't tweet message")