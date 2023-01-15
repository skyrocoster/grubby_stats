import pandas as pd
from app import *
from sqlalchemy import inspect


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
