import streamlit as st
from app import *
import plotly_express as px  #
from datetime import datetime

app_context = app.app_context()
app_context.push()
app.secret_key = "1234567A"

st.set_page_config(layout="wide")
header = st.container()
dataset = st.container()
features = st.container()

player_matches = object_as_df(PlayerMatches().query.all())
player_matches["hero_name"] = player_matches["hero_id"].map(Heroes().hero_map())
player_matches_first_session = (
    player_matches.sort_values(["start_time"], ascending=True)
    .groupby("session_id")
    .first()
    .reset_index()
)
player_matches_first_session["day_of_week"] = player_matches_first_session[
    "start_time_normal"
].dt.day_name()
player_matches["session_day_of_week"] = player_matches["session_id"].map(
    dict(
        zip(
            player_matches_first_session["session_id"],
            player_matches_first_session["day_of_week"],
        )
    )
)
player_matches["session_start"] = player_matches["session_id"].map(
    dict(
        zip(
            player_matches_first_session["session_id"],
            player_matches_first_session["start_time_normal"],
        )
    )
)


st.sidebar.header("Grubby Data")

all = st.sidebar.checkbox("Select all")
if all:
    hero = st.sidebar.multiselect(
        "Select Heroes:",
        player_matches["hero_name"].sort_values().unique(),
        player_matches["hero_name"].sort_values().unique(),
    )
else:
    hero = st.sidebar.multiselect(
        "Select Heroes:",
        player_matches["hero_name"].sort_values().unique(),
    )

# st.sidebar.slider(
#     "Test",
#     value=[
#         player_matches["start_time_normal"].min(),
#         player_matches["start_time_normal"].max(),
#     ],
# )

game_mode = st.sidebar.multiselect("Select Lobby Type", options=[0, 7], default=7)

played_ranks = (
    player_matches["average_rank"].dropna().astype(int).sort_values().unique()
)
played_rank_ends = [int(played_ranks.min()), int(played_ranks.max())]

ranks = st.sidebar.slider(
    min_value=played_rank_ends[0],
    max_value=played_rank_ends[1],
    value=[int(played_ranks.min()), int(played_ranks.max())],
    label="game_rank",
)

# MAIN

player_matches_sel = player_matches.loc[
    (player_matches["hero_name"].isin(hero))
    & (player_matches["average_rank"] >= ranks[0])
    & (player_matches["average_rank"] <= ranks[1])
    & (player_matches["lobby_type"].isin(game_mode))
]


see_data = st.expander("Raw Data Here!")
with see_data:
    st.dataframe(data=player_matches_sel)

day_info = (
    player_matches_sel[["session_day_of_week", "win"]]
    .groupby("session_day_of_week")
    .mean()
    .sort_values("win", ascending=False)
    .reset_index()
)
fig = px.bar(day_info, x="session_day_of_week", y="win", labels=True, text_auto=True)

st.plotly_chart(fig)

hero_wr = player_matches_sel[["hero_name", "win"]].copy()
hero_wr = hero_wr.groupby("hero_name").mean().reset_index()

player_matches_sel_hero_played = (
    player_matches_sel[["hero_name"]].value_counts().reset_index()
)
player_matches_sel_hero_played.columns = ["hero_name", "times_played"]
hero_wr = hero_wr.merge(player_matches_sel_hero_played, on="hero_name")

win_loss = (
    str(player_matches_sel.loc[player_matches_sel["win"] == 1].count()["win"])
    + " Wins - "
    + str(player_matches_sel.loc[player_matches_sel["win"] == 0].count()["win"])
    + " Losses"
)

hero_wr_col1, hero_wr_col2 = st.columns(2)
fig = px.bar(hero_wr, x="hero_name", y="win", color="times_played")
with hero_wr_col1:
    st.title("Hero Win Rates")
    st.text(win_loss)
    st.plotly_chart(fig)
with hero_wr_col2:
    st.dataframe(hero_wr)
