import streamlit as st
from app import *

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grubby.db"
# db = SQLAlchemy(app)
app_context = app.app_context()
app_context.push()
app.secret_key = "1234567A"

header = st.container()
dataset = st.container()
features = st.container()

df = object_as_df(PlayerMatches().query.all())
df["hero_name"] = df["hero_id"].map(Heroes().hero_map())

st.sidebar.header("Grubby Data")
hero = st.sidebar.multiselect(
    "Select Hero:",
    options=df["hero_name"].sort_values().unique(),
    default=df["hero_name"].sort_values().unique(),
)
game_mode = st.sidebar.multiselect("Select Lobby Type", options=[0, 7], default=7)

df_sel = df.query("hero_name == @hero & lobby_type == @game_mode")

st.dataframe(df_sel)
