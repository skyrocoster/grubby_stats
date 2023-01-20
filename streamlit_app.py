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

grubby_matches = object_as_df(PlayerMatches().query.all())
grubby_matches["hero_name"] = grubby_matches["hero_id"].map(Heroes().hero_map())
grubby_matches_first_session = (
    grubby_matches.sort_values(["start_time"], ascending=True)
    .groupby("session_id")
    .first()
    .reset_index()
)
grubby_matches_first_session["day_of_week"] = grubby_matches_first_session[
    "start_time_normal"
].dt.day_name()
grubby_matches["session_day_of_week"] = grubby_matches["session_id"].map(
    dict(
        zip(
            grubby_matches_first_session["session_id"],
            grubby_matches_first_session["day_of_week"],
        )
    )
)
grubby_matches["session_start"] = grubby_matches["session_id"].map(
    dict(
        zip(
            grubby_matches_first_session["session_id"],
            grubby_matches_first_session["start_time_normal"],
        )
    )
)


st.sidebar.header("Grubby Data")

all = st.sidebar.checkbox("Select all")
if all:
    hero = st.sidebar.multiselect(
        "Select Heroes:",
        grubby_matches["hero_name"].sort_values().unique(),
        grubby_matches["hero_name"].sort_values().unique(),
    )
else:
    hero = st.sidebar.multiselect(
        "Select Heroes:",
        grubby_matches["hero_name"].sort_values().unique(),
    )


game_mode = st.sidebar.multiselect("Select Lobby Type", options=[0, 7], default=7)

played_ranks = (
    grubby_matches["average_rank"].dropna().astype(int).sort_values().unique()
)
played_rank_ends = [int(played_ranks.min()), int(played_ranks.max())]

ranks = st.sidebar.slider(
    min_value=played_rank_ends[0],
    max_value=played_rank_ends[1],
    value=[int(played_ranks.min()), int(played_ranks.max())],
    label="game_rank",
)

# MAIN

grubby_matches_sel = grubby_matches.loc[
    (grubby_matches["hero_name"].isin(hero))
    & (grubby_matches["average_rank"] >= ranks[0])
    & (grubby_matches["average_rank"] <= ranks[1])
    & (grubby_matches["lobby_type"].isin(game_mode))
]


see_data = st.expander("Raw Data Here!")
with see_data:
    st.dataframe(data=grubby_matches_sel)

day_info = (
    grubby_matches_sel[["session_day_of_week", "win"]]
    .groupby("session_day_of_week")
    .mean()
    .sort_values("session_day_of_week", ascending=False)
    .reset_index()
)
fig = px.bar(day_info, x="session_day_of_week", y="win", labels=True, text_auto=True)
pie = px.pie(
    grubby_matches_sel[["duration", "session_day_of_week"]],
    values="duration",
    names="session_day_of_week",
)

days_col1, days_col2 = st.columns(2)
with days_col1:
    st.title("Win Rate on Stream Days")
    st.plotly_chart(fig)
with days_col2:
    st.title("Time Played on Stream Days")
    st.plotly_chart(pie)

hero_wr = (
    grubby_matches_sel[["hero_name", "win"]].groupby("hero_name").mean().reset_index()
)
# hero_wr = hero_wr

grubby_matches_sel_hero_played = (
    grubby_matches_sel[["hero_name"]].value_counts().reset_index()
)
grubby_matches_sel_hero_played.columns = ["hero_name", "times_played"]
hero_wr = hero_wr.merge(grubby_matches_sel_hero_played, on="hero_name")

win_loss = (
    str(grubby_matches_sel.loc[grubby_matches_sel["win"] == 1].count()["win"])
    + " Wins - "
    + str(grubby_matches_sel.loc[grubby_matches_sel["win"] == 0].count()["win"])
    + " Losses"
)

overall_wr = grubby_matches["win"].mean()
sel_wr = grubby_matches_sel["win"].mean()

st.markdown("""---""")
hero_wr_col1, hero_wr_col2 = st.columns(2)
fig = px.bar(hero_wr, x="hero_name", y="win", color="times_played")
fig.add_hline(
    y=sel_wr,
    line_color="green",
    annotation_text="Selection Winrate",
    annotation_position="bottom right",
)
with hero_wr_col1:
    st.title("Hero Win Rates")
    st.plotly_chart(fig)
with hero_wr_col2:
    st.title("Win Rates Table")
    st.text(win_loss)
    st.dataframe(hero_wr)
