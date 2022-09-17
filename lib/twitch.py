from typing import Union, Dict

from requests import get  # type: ignore

# gets the user-id from nickname of specified Twitch user
def id_from_nick(id: str, token: str, nick: str) -> Union[str, None]:
    headers = {
        'Authorization': 'Bearer ' + token,
        'Client-ID': id
    }

    try:
        r = get(
            "https://api.twitch.tv/helix/users?login={}".format(nick), headers=headers)
        return r.json()["data"][0]["id"]
    except:
        return None

# gets twitch channel information
def get_channel_info(id: str, token: str, twitch_id: int) -> Union[Dict, None]:
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': id,
        'Authorization': 'Bearer ' + token
    }

    try:
        r = get(
            "https://api.twitch.tv/helix/streams?user_id={}".format(twitch_id), headers=headers)
        return r.json()["data"][0]
    except:
        return None
