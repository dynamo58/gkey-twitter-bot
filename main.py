#!/usr/bin/python

from config import DEVELOPMENT_MODE
from lib.core import Event, Streamer, obtain_config
from lib.twitch import get_channel_info, id_from_nick
from lib.twitter import TwitterAPIClient

from typing import List, Optional, Any, Dict


from sys import argv
from threading import Thread
from time import sleep


CONF = obtain_config(DEVELOPMENT_MODE)
twitter_client = TwitterAPIClient(CONF)


def main(args: List[str]):
    streamer = Streamer().from_config(CONF)

    while True:
        sleep(120)
        streamer.check(CONF, twitter_client)


if __name__ == "__main__":
    main(argv)
