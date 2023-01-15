import requests
import json
import time
from app import *
import os
from sqlalchemy import inspect
import pandas as pd


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


grubby_id = 849473199
grubby_steam = 76561198809738927
open_dota = "https://api.opendota.com/api"
dota_constants = "https://raw.githubusercontent.com/odota/dotaconstants/master/json"
dota_constants_build = (
    "https://raw.githubusercontent.com/odota/dotaconstants/master/build/"
)
raw_data = "data/grubby/matches/MatchDetails"

match_id = 6718329621

# This is goal gained by each minute. NOT networth.
players = open(
    f"data/grubby/matches/MatchDetails/{match_id}.json", encoding="utf-8"
)
players = json.load(players)
for player in players["players"]:
    new_player = {}
    new_player["player_id"] = player.pop("account_id")
    new_player["match_id"] = match_id
    if player['gold_t'] is not None:
        for i in player["gold_t"]:
            new_player["minute"] = player["gold_t"].index(i)
            new_player["gold"] = i
            new_player["last_hits"] = player["lh_t"][player["gold_t"].index(i)]
            new_networthtimings = NetworthTimings(**new_player)
            db.session.merge(new_networthtimings)
        db.session.commit()
