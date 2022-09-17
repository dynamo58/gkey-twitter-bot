from lib.twitch import id_from_nick, get_channel_info
import config as hard_config

from typing import List, Optional, Dict, Union, Any
from enum import Enum

from sys import argv
from datetime import datetime as dt

def log(uptime: int, message: str) -> None:
	print("{} | uptime: {}h  | {}".format(dt.now().isoformat()[:-3], round(uptime / 3600.0, 2), message), end="\r", flush=True)

# -> config based on the environment/run mode
def obtain_config() -> Dict[str, Any]:
	config: Dict[str, Optional[Any]] = {}

	if hard_config.DEVELOPMENT_MODE:
		from dotenv import dotenv_values  # type: ignore

		config = dotenv_values(".env")
	else:
		from os import environ

		for var in ["ID", "TOKEN", "TWITTER_API_KEY", "TWITTER_API_SECRET_KEY", "TWITTER_BEARER_TOKEN", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET_TOKEN"]:
			config[var] = environ[var]

	config["STREAMER"] = hard_config.STREAMER
	config["PERIOD"] = hard_config.PERIOD
	config["VERBOSE"] = hard_config.VERBOSE
	config["LOGGING"] = hard_config.LOGGING

	return config

# if config says so, report info
def handleFeedback(CONF, type, feedback: Union[str, Exception]) -> None:
	timestamp = dt.now().strftime("%d.%m.%y %H:%M:%S")
	out = "[{}]\t{}{}".format(timestamp, type.name, feedback)

	if CONF["LOGGING"]:
		with open(".log", 'a') as log:
			log.write("\n\n")
			log.write(out)

	if CONF["VERBOSE"]:
		print(out)

	pass

# all the possible info that can be reported
class Feedback(Enum):
	Initialized = 1
	Tweet = 2
	Error = 3

# All of the tracked Events + tweet templates
class Event(Enum):
	went_live = "{} just went live playing {} with title \"{}\""
	went_offline = "{} has just gone offline"
	changed_title = "{} just changed title to \"{}\""
	changed_game = "{} just started playing {}"

# Twitch streamer tracking instance
class Streamer():
	def __init__(self):
		self.name = None
		self.id = None
		self.is_live = None
		self.game = None
		self.title = None
		self._checkCount = 0

	def __str__(self):
		return "\n{} <-> {}\n\tlive:\t{}\n\tgame:\t{}\n\ttitle:\t{}".format(self.name, self.id, self.is_live, self.game, self.title)

	# create instance based on config
	def from_config(self, CONF):
		self.name = CONF["STREAMER"]
		id = id_from_nick(
			CONF["ID"],
			CONF["TOKEN"],
			CONF["STREAMER"]
		)

		if id == None:
			raise Exception("User does not exist or credentials expired")

		self.id = id
		info = get_channel_info(CONF["ID"], CONF["TOKEN"], id)  # type: ignore

		if info == None:
			self.is_live = False
		else:
			self.is_live = True
			self.game = info["game_name"]						# type: ignore
			self.title = info["title"]							# type: ignore

		handleFeedback(CONF, Feedback.Initialized, self)

		return self

	# check if streamer is live and compare with previous data
	def check(self, CONF, twitter_client):
		pending_events: List[Event] = []
		info = get_channel_info(CONF["ID"], CONF["TOKEN"], self.id)

		if info == None and self.is_live:
			pending_events.append(Event.went_offline)
			self.is_live = False

		if info != None and not self.is_live:
			pending_events.append(Event.went_live)
			self.is_live = True

		if info != None:
			if self.game != info["game_name"]:
				pending_events.append(Event.changed_game)
				self.game = info["game_name"]

			if self.title != info["title"]:
				pending_events.append(Event.changed_title)
				self.title = info["title"]

		self.handle_event(pending_events, CONF, twitter_client)

	# go through the event stack and decide what/what not to tweet
	def handle_event(self, event_stack: List[Event], CONF, twitter_client):
		self._checkCount += 1
		if len(event_stack) == 0:
			log(self._checkCount * CONF["PERIOD"], "nothing here")
		else:
			log(self._checkCount * CONF["PERIOD"], "thing happened, tweeting")
		
		if Event.went_live in event_stack:
			twitter_client.tweet(
				CONF,
				Event.went_live.value.format(
					self.name,
					self.game,
					self.title
				)
			)
			return

		if Event.went_offline in event_stack:
			twitter_client.tweet(
				CONF,
				Event.went_offline.value.format(self.name)
			)
			return

		if Event.changed_game in event_stack:
			twitter_client.tweet(
				CONF,
				Event.changed_game.value.format(
					self.name,
					self.game
				)
			)
			return

		if Event.changed_title in event_stack:
			twitter_client.tweet(
				CONF,
				Event.changed_title.value.format(
					self.name,
					self.title
				)
			)
			return
