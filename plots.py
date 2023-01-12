import pandas as pd
import requests
import json
import time


retrieved_matches = open("data/grubby/retrieved/matches.txt").readlines()
retrieved_matches.extend([6889541725, 6785977108])
print(retrieved_matches)


wanted_fields = [
    'match_id',
    'barracks_status_dire',
    'barracks_status_radiant',
    'dire_score',
    'duration',
    'first_blood_time',
    'game_mode',
    'lobby_type',
    'negative_votes',
    'radiant_score',
    'radiant_win',
    'start_time',
    'patch',
    'region',
    'comeback',
    'loss'
]

df = pd.DataFrame()
for match in retrieved_matches:
    with open(f'data/grubby/matches/{match}.json','r', encoding='utf-8') as f:
        data = json.loads(f.read())
    df_temp = pd.json_normalize(data)
    print(df_temp.head())
    df = pd.concat([df, df_temp[wanted_fields]])

print(df.head())
