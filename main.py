#!/usr/bin/python

from lib.core import Event, Streamer
from lib.twitch import get_channel_info, id_from_nick


from typing import List, Optional, Any, Dict


from sys import argv
from threading import Thread
from time import sleep
from pprint import pprint

DEVELOPMENT_MODE = True

CONF: Dict[str, Optional[str]] = {"STREAMER": "Gisthekey"}

if DEVELOPMENT_MODE:
    from dotenv import dotenv_values

    CONF = dotenv_values(".env")
else:
    from os import environ

    for var in ["ID", "TOKEN", "TWITTER_API_KEY", "TWITTER_API_SECRET_KEY", "TWITTER_BEARER_TOKEN", "TWITTER_ACCEESS_TOKEN", "TWITTER_ACCESS_SECRET_TOKEN"]:
        CONF[var] = environ[var]


def main(args: List[str]):
    streamer = Streamer().from_name(CONF["STREAMER"])

    while True:
        sleep(120)
        streamer.check()


if __name__ == "__main__":
    main(argv)
