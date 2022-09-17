# About
A Twitter notifier regarding [Gisthekey](https://twitch.tv/Gisthekey)'s Twitch channel stationed at [@GisthekeyInfo](https://twitter.com/GisthekeyInfo).

# Features
Currently the bot will Tweet when
- streamer goes live
- streamer goes offline
- streamer changes title
- streamer changes category

# Running yourself

- install the requirements va `pip install -r requirements.txt`
- configure the `config.py` file

Setup via a .env file
- rename `.env.example` to `.env`
- populate `.env` with your own credentials
- run with `python main.py --dev`

Setup via environment variables
- run `python main.py` with environment variables specified by the `.env.example` file (with appropriate values)

All the possible CLI args are:
- `--dev` - read credentials from a `.env file` (normally takes in environment variables)
- `--verbose` - writes info to console
- `--log` - logs info to a .logs file