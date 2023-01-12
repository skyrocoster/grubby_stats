import requests
import json
import time
import os

grubby_id = 849473199
grubby_steam = 76561198809738927
open_dota = "https://api.opendota.com/api"
dota_constants = "https://raw.githubusercontent.com/odota/dotaconstants/master/json"
dota_constants_build = (
    "https://raw.githubusercontent.com/odota/dotaconstants/master/build/"
)
raw_data = "data"

# Matches
grubby_match_ids = []
grubby_matches = requests.get(f"{open_dota}/players/{grubby_id}/matches").json()
for i in grubby_matches:
    i["player_id"] = grubby_id
    grubby_match_ids.append(i.get("match_id"))
with open(f"{raw_data}/grubby/matches/PlayerMatches/{grubby_id}.json", "w", encoding="utf-8") as f:
    json.dump(grubby_matches, f, ensure_ascii=False, indent=4)

retrieved_matches = [
    int(x.replace(".json", "")) for x in os.listdir("data/grubby/matches/MatchDetails")
]

grubby_match_ids.sort()
retrieved_matches.sort()
unretrieved_id = list(set(grubby_match_ids).difference(retrieved_matches))

for i in unretrieved_id:
    match = requests.get(f"{open_dota}/matches/{i}")
    if match.ok:
        match = match.json()
        with open(f"{raw_data}/grubby/matches/MatchDetails/{i}.json", "w", encoding="utf-8") as f:
            json.dump(match, f, ensure_ascii=False, indent=4)
    else:
        print(i)
    time.sleep(1.2)
