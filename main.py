#!/usr/bin/python


from lib.core import Streamer, obtain_config
from lib.twitter import TwitterAPIClient

from typing import List
from sys import argv
from time import sleep


CONF = obtain_config()
twitter_client = TwitterAPIClient(CONF)

def main(args: List[str]):
    streamer = Streamer().from_config(CONF)

    while True:
        sleep(CONF["PERIOD"])
        streamer.check(CONF, twitter_client)


if __name__ == "__main__":
    main(argv)
