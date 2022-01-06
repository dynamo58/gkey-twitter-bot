# About
A Twitter notifier regarding [Gisthekey](https://twitch.tv/Gisthekey)'s Twitch channel stationed at [@GisthekeyInfo](https://twitter.com/GisthekeyInfo).

# Features
Currently the bot will Tweet when
- streamer goes live
- streamer goes offline
- streamer changes title
- streamer changes category

# Running yourself

- install the requirements va `pip install -r requiremenets.txt`
- configure the `config.py` file

Now you either supply the API keys, etc. via a env. file
- rename `.env.example` to `.env`
- populate `.env` with your own keys
- run with `python main.py --dev`

The other way is to provide those via environmental variables - then you could just run it normally with `python main.py`