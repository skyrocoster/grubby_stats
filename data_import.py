import json
from app import *
import os
import pandas as pd
from sqlalchemy import inspect

raw_data = "data"

matches = open(f"{raw_data}/grubby/matches/PlayerMatches/849473199.json")
matches = json.load(matches)
for match in matches:
    player_match = PlayerMatches(**match)
    player_match.start_time_normal = datetime.datetime.fromtimestamp(
        player_match.start_time
    )
    db.session.merge(player_match)
db.session.commit()

heroes = open(f"{raw_data}/heroes.json")
heroes = json.load(heroes)
for hero_id in heroes:
    hero = heroes[hero_id]
    hero["hero_id"] = hero.pop("id")
    roles = hero["roles"]
    for i in roles:
        hero[i.lower()] = 1
    del hero["roles"]
    new_hero = Heroes(**hero)
    db.session.merge(new_hero)
db.session.commit()

game_modes = open(f"{raw_data}/game_mode.json")
game_modes = json.load(game_modes)
for mode_id in game_modes:
    game_mode = game_modes[mode_id]
    game_mode["mode_id"] = game_mode.pop("id")
    game_mode["localised_name"] = (
        game_mode.get("name").replace("game_mode_", "").title()
    )
    new_mode = GameModes(**game_mode)
    db.session.merge(new_mode)
db.session.commit()

retrieved_matches = [
    int(x.replace(".json", "")) for x in os.listdir("data/grubby/matches/MatchDetails")
]
retrieved_matches.sort()
matches = MatchDetails().query.all()
stored_matches = [i.match_id for i in matches]
stored_matches = list(dict.fromkeys(stored_matches))
unretrieved_id = list(set(retrieved_matches).difference(stored_matches))
print(unretrieved_id)

match_detail_fields = [
    "match_id",
    "barracks_status_dire",
    "barracks_status_radiant",
    "dire_score",
    "duration",
    "first_blood_time",
    "game_mode",
    "lobby_type",
    "negative_votes",
    "radiant_score",
    "radiant_win",
    "start_time",
    "patch",
]

df = pd.DataFrame()
for match in unretrieved_id:
    try:
        with open(
            f"data/grubby/matches/MatchDetails/{match}.json", "r", encoding="utf-8"
        ) as f:
            data = json.loads(f.read())
        df_temp = pd.json_normalize(data)
        df = pd.concat([df, df_temp[match_detail_fields]])
    except:
        print(f"{match} failed 3")

match_details = df.to_dict(orient="records")

for match in match_details:
    new_match = MatchDetails(**match)
    db.session.merge(new_match)
db.session.commit()


match_player_fields = [
    "match_id",
    "player_id",
    "hero_id",
    "player_slot",
    "assists",
    "deaths",
    "denies",
    "firstblood_claimed",
    "gold_per_min",
    "hero_id",
    "kills",
    "last_hits",
    "level",
    "net_worth",
    "xp_per_min",
    "radiant_win",
    "start_time",
    "duration",
    "lobby_type",
    "game_mode",
    "patch",
    "isRadiant",
]


retrieved_matches = [
    int(x.replace(".json", "")) for x in os.listdir("data/grubby/matches/MatchDetails")
]
retrieved_matches.sort()
matches = MatchPlayers().query.all()
stored_matches = [i.match_id for i in matches]
stored_matches = list(dict.fromkeys(stored_matches))
stored_matches.sort()
unretrieved_id = list(set(retrieved_matches).difference(stored_matches))

for match_id in unretrieved_id:
    try:
        players = open(
            f"data/grubby/matches/MatchDetails/{match_id}.json", encoding="utf-8"
        )
        players = json.load(players)
        players_full = players["players"]
        for player_full in players_full:
            player_full["player_id"] = player_full.pop("account_id")
            player = {key: player_full[key] for key in match_player_fields}
            if "lane_role" in player_full:
                player["lane_role"] = player_full["lane_role"]
            if "lane" in player_full:
                player["lane"] = player_full["lane"]
            new_matchplayer = MatchPlayers(**player)
            db.session.merge(new_matchplayer)
            db.session.commit()
    except:
        print(f"{match_id} failed 4")


retrieved_matches = [
    int(x.replace(".json", "")) for x in os.listdir("data/grubby/matches/MatchDetails")
]
retrieved_matches.sort()
matches = PickBans().query.all()
stored_matches = [i.match_id for i in matches]
stored_matches = list(dict.fromkeys(stored_matches))
stored_matches.sort()
unretrieved_id = list(set(retrieved_matches).difference(stored_matches))

for match_id in unretrieved_id:
    try:
        picks_bans = open(
            f"data/grubby/matches/MatchDetails/{match_id}.json", encoding="utf-8"
        )
        picks_bans = json.load(picks_bans)
        picks_bans = picks_bans["picks_bans"]
        for pick in picks_bans:
            pick["match_id"] = match_id
            pick["order"] = int(pick["order"]) + 1
            pick["team"] = "radiant" if pick["team"] == 0 else "dire"
            new_pick = PickBans(**pick)
            db.session.merge(new_pick)
            db.session.commit()
    except:
        print(f"{match_id} failed 1")

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
            if player['gold_t'] is not None:
                for i in player["gold_t"]:
                    new_player["minute"] = player["gold_t"].index(i)
                    new_player["gold"] = i
                    new_player["last_hits"] = player["lh_t"][player["gold_t"].index(i)]
                    new_networthtimings = NetworthTimings(**new_player)
                    db.session.merge(new_networthtimings)
                db.session.commit()
        except:
            print(f"{match_id} failed 2")


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def win_loss(team, radiant_win):
    if team == "radiant" and radiant_win == 1:
        return 1
    elif team == "dire" and radiant_win == 0:
        return 1
    else:
        return 0


matches = PlayerMatches().query.all()

dict_result = []

for match in matches:
    dict_result.append(object_as_dict(match))


df = pd.DataFrame(dict_result).sort_values(by=["start_time"], ascending=True)

session_break = 60 * 60 * 4
df["difference"] = df["start_time"].diff()
df.loc[df["difference"] >= session_break, "session_start"] = 1
df.loc[df["difference"].isna(), "session_start"] = 1
df.loc[df["session_start"].isna(), "session_start"] = 0
df["session_id"] = df["session_start"].cumsum()
df = df.astype({"session_id": "int", "session_start": "int"})
df["session_counter"] = df.groupby("session_id").cumcount() + 1

df.loc[df["player_slot"] >= 128, "team"] = "dire"
df.loc[df["team"].isna(), "team"] = "radiant"
df["win"] = df.apply(lambda row: win_loss(row["team"], row["radiant_win"]), axis=1)

df_dict = df[
    ["player_id", "match_id", "team", "win", "session_id", "session_counter"]
].to_dict(orient="records")

for row in df_dict:
    new_fields = PlayerMatches(**row)
    db.session.merge(new_fields)
db.session.commit()


# match players

player_matches = MatchPlayers().query.all()

dict_result = []

for player_match in player_matches:
    dict_result.append(object_as_dict(player_match))


df = pd.DataFrame(dict_result)

df.loc[df["isRadiant"] == 1, "team"] = "radiant"
df.loc[df["team"].isna(), "team"] = "dire"

df["win"] = df.apply(lambda row: win_loss(row["team"], row["radiant_win"]), axis=1)

df_dict = df[["match_player_id", "team", "win"]].to_dict(orient="records")

for row in df_dict:
    new_fields = MatchPlayers(**row)
    db.session.merge(new_fields)
db.session.commit()

print(df.head())
