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

retrieved_matches = [
    int(x.replace(".json", "")) for x in os.listdir("data/grubby/matches/MatchDetails")
]
retrieved_matches.sort()
matches = NetworthTimings().query.all()
stored_matches = [i.match_id for i in matches]
stored_matches = list(dict.fromkeys(stored_matches))
stored_matches.sort()
unretrieved_id = list(set(retrieved_matches).difference(stored_matches))

for match_id in unretrieved_id:
    # This is goal gained by each minute. NOT networth.
    players = open(
        f"data/grubby/matches/MatchDetails/{match_id}.json", encoding="utf-8"
    )
    players = json.load(players)
    for player in players["players"]:
        try:
            new_player = {}
            new_player["player_id"] = player.pop("account_id")
            new_player["match_id"] = match_id
            for i in player["gold_t"]:
                new_player["minute"] = player["gold_t"].index(i)
                new_player["gold"] = i
                new_player["last_hits"] = player["lh_t"][player["gold_t"].index(i)]
                new_networthtimings = NetworthTimings(**new_player)
                db.session.merge(new_networthtimings)
            db.session.commit()
        except:
            print(f"{match_id} failed")
