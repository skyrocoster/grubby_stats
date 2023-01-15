import streamlit as st
from app import *
import plotly_express as px

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grubby.db"
# db = SQLAlchemy(app)
app_context = app.app_context()
app_context.push()
app.secret_key = "1234567A"

st.set_page_config(layout="wide")
header = st.container()
dataset = st.container()
features = st.container()

player_matches = object_as_df(PlayerMatches().query.all())
player_matches["hero_name"] = player_matches["hero_id"].map(Heroes().hero_map())
player_matches_first_session = player_matches.sort_values(['start_time'], ascending=True).groupby('session_id').first().reset_index()
player_matches_first_session['day_of_week'] = player_matches_first_session['start_time_normal'].dt.day_name()
player_matches['session_day_of_week'] = player_matches['session_id'].map(dict(zip(player_matches_first_session['session_id'], player_matches_first_session['day_of_week'])))
player_matches['session_start'] = player_matches['session_id'].map(dict(zip(player_matches_first_session['session_id'], player_matches_first_session['start_time_normal'])))

st.sidebar.header("Grubby Data")

hero = st.sidebar.multiselect(
    "Select Hero:",
    options=player_matches["hero_name"].sort_values().unique(),
    default=player_matches["hero_name"].sort_values().unique(),
)
game_mode = st.sidebar.multiselect("Select Lobby Type", options=[0, 7], default=7)

player_matches_sel = player_matches.query("hero_name == @hero & lobby_type == @game_mode")

win_loss = str(player_matches_sel.loc[player_matches_sel['win'] == 1].count()['win']) + ' - ' + str(player_matches_sel.loc[player_matches_sel['win'] == 0].count()['win'])

day_info = player_matches_sel[['session_day_of_week', 'win']].groupby('session_day_of_week').mean().sort_values('win', ascending=False).reset_index()
fig = px.bar(day_info, x='session_day_of_week', y='win', labels=True, text_auto=True)

with dataset:
    st.text(win_loss)

st.dataframe(player_matches_sel)
st.plotly_chart(fig)


hero_wr = player_matches_sel[["hero_name", "win"]].copy()
hero_wr = hero_wr.groupby('hero_name').mean().reset_index()

player_matches_sel_hero_played = player_matches_sel[['hero_name']].value_counts().reset_index()
player_matches_sel_hero_played.columns = ['hero_name', 'times_played']
hero_wr = hero_wr.merge(player_matches_sel_hero_played, on='hero_name')
hero_wr = hero_wr.sort_values('times_played', ascending=False).head(10)

col1, col2 = st.columns(2)
fig = px.bar(hero_wr, x='hero_name', y='win', color='times_played')
with col1:
    st.plotly_chart(fig)
with col2:
    st.dataframe(hero_wr)