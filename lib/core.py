from lib.twitch import id_from_nick, get_channel_info
from lib.twitter import tweet

from typing import List, Optional
from enum import Enum

from dotenv import dotenv_values

CONF = dotenv_values(".env")

class Event(Enum):
    went_live     = "{} has just went live playing {} with title \"{}\""
    went_offline  = "{} has just went offline"
    changed_title = "{} has just changed title to \"{}\""
    changed_game  = "{} has just started playing {}"

class Streamer():
    def __init__(self):
        self.name      = None
        self.id        = None
        self.is_live   = None
        self.game      = None
        self.title     = None
    
    def __str__(self):
        return "\n{} <-> {}\nlive:\t{}\ngame:\t{}\ntitle:\t{}".format(self.name, self.id, self.is_live, self.game, self.title)

    def from_name(self, streamer: Optional[str]):
        self.name = streamer
        id = id_from_nick(CONF["ID"], CONF["TOKEN"], streamer)	# type: ignore

        if id == None:
            raise Exception("User does not exist")

        self.id = id
        info = get_channel_info(CONF["ID"], CONF["TOKEN"], id)	# type: ignore

        if info == None:
            self.is_live = False
        else:
            self.is_live   = True
            self.game      = info["game_name"]						# type: ignore
            self.title     = info["title"]							# type: ignore
        

        print("Initialized:\n", self)

        return self

    def check(self):
        pending_events: List[Event] = []
        info = get_channel_info(CONF["ID"], CONF["TOKEN"], self.id)

        if info == None and self.is_live:
            pending_events.append(Event.went_offline)
            self.is_live = False
        
        if info != None and not self.is_live:
            pending_events.append(Event.went_live)
            self.is_live = True

        if self.game != info["game_name"]:
            pending_events.append(Event.changed_game)
            self.game = info["game_name"]
        
        if self.title != info["title"]:
            pending_events.append(Event.changed_title)
            self.title = info["title"]

        self.handle_event(pending_events)
    
    def handle_event(self, event_stack: List[Event]):
        if Event.went_live in event_stack:
            tweet(Event.went_live.value.format(self.name, self.game, self.title))
            return
        
        if Event.went_offline in event_stack:
            tweet(Event.went_offline.value.format(self.name))
            return
        
        if Event.changed_game in event_stack:
            tweet(Event.changed_game.value.format(self.name, self.game))
            return
        
        if Event.changed_title in event_stack:
            tweet(Event.changed_title.value.format(self.name, self.title))
            return
        
        print("Nothing here ZULUL")
