#!/usr/bin/python

from config import DEVELOPMENT_MODE
from lib.core import Event, Streamer, obtain_config
from lib.twitch import get_channel_info, id_from_nick


from typing import List, Optional, Any, Dict


from sys import argv
from threading import Thread
from time import sleep


CONF = obtain_config(DEVELOPMENT_MODE)

def main(args: List[str]):
    streamer = Streamer().from_name(CONF["STREAMER"])

    while True:
        sleep(120)
        streamer.check()


if __name__ == "__main__":
    main(argv)
